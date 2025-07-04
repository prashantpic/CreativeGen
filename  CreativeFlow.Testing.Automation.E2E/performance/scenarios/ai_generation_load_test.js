import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend } from 'k6/metrics';
import { environment } from '../config/environments.js';

// Custom Trend metrics to track latency of different generation phases
const sampleGenerationLatency = new Trend('sample_generation_latency', true);
const finalGenerationLatency = new Trend('final_generation_latency', true);

/**
 * Test options defining the load profile.
 * This test uses a constant arrival rate to ensure a steady throughput
 * of 1000 requests per minute (approx 17 per second) to the AI pipeline.
 */
export const options = {
  scenarios: {
    ai_generation_throughput: {
      executor: 'constant-arrival-rate',
      rate: 1000, // 1000 iterations per minute
      timeUnit: '1m', // Corresponds to rate
      duration: '10m', // Test duration
      preAllocatedVUs: 50, // Initial number of VUs
      maxVUs: 400, // Max VUs to handle the load and polling
    },
  },
  thresholds: {
    'http_req_failed{api_tag:ai_generation}': ['rate<0.02'], // Fail if error rate on AI APIs is > 2%
    'sample_generation_latency': ['p(90)<30000'], // 90% of sample generations must be < 30s
    'final_generation_latency': ['p(90)<120000'], // 90% of final generations must be < 2m
  },
};

export function setup() {
  const loginUrl = `${environment.baseUrl}/api/v1/auth/login`;
  const payload = JSON.stringify({
    email: environment.defaultUser.email,
    password: environment.defaultUser.password,
  });
  const res = http.post(loginUrl, payload, { headers: { 'Content-Type': 'application/json' } });
  const jwt = res.json('accessToken');
  if (!jwt) throw new Error('Login failed, no JWT');
  return { jwt: jwt };
}

/**
 * Main test logic for a single AI generation workflow.
 */
export default function (data) {
  const params = {
    headers: { 'Authorization': `Bearer ${data.jwt}`, 'Content-Type': 'application/json' },
    tags: { api_tag: 'ai_generation' }
  };
  
  // --- Phase 1: Sample Generation ---
  let startTime = Date.now();
  const generationPayload = JSON.stringify({
    prompt: 'a stunning photograph of a futuristic car driving through a neon-lit city',
    parameters: { resolution: '1024x1024' }
  });

  const genRes = http.post(`${environment.baseUrl}/api/v1/generations`, generationPayload, params);
  check(genRes, { 'generation request submitted': (r) => r.status === 202 });
  
  if (genRes.status !== 202) return; // Abort this iteration if submission fails

  const generationId = genRes.json('generationId');
  if (!generationId) return;

  // Poll for sample completion
  let status;
  const pollLimit = 10; // Poll max 10 times (60s total)
  for (let i = 0; i < pollLimit; i++) {
    sleep(6); // Poll every 6 seconds
    const statusRes = http.get(`${environment.baseUrl}/api/v1/generations/${generationId}/status`, params);
    if (statusRes.status === 200) {
      status = statusRes.json('status');
      if (status === 'AwaitingSelection' || status === 'Failed' || status === 'Completed') {
        break;
      }
    }
  }

  if (status === 'AwaitingSelection') {
    sampleGenerationLatency.add(Date.now() - startTime);
  } else {
    // If it failed or timed out, don't proceed to finalization
    return; 
  }

  // --- Phase 2: Final Generation ---
  startTime = Date.now();
  const finalizationPayload = JSON.stringify({ selectedSampleId: 'sample_id_placeholder_0' }); // Use a placeholder

  const finalizeRes = http.post(`${environment.baseUrl}/api/v1/generations/${generationId}/finalize`, finalizationPayload, params);
  check(finalizeRes, { 'finalization request submitted': (r) => r.status === 202 });
  
  if(finalizeRes.status !== 202) return;

  // Poll for final completion
  for (let i = 0; i < pollLimit * 2; i++) { // Poll max 20 times (2m total)
    sleep(6);
    const statusRes = http.get(`${environment.baseUrl}/api/v1/generations/${generationId}/status`, params);
    if (statusRes.status === 200) {
      status = statusRes.json('status');
      if (status === 'Completed' || status === 'Failed') {
        break;
      }
    }
  }

  if (status === 'Completed') {
    finalGenerationLatency.add(Date.now() - startTime);
  }
}