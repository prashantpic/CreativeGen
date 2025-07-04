import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { environment } from '../config/environments.js';

/**
 * Test options defining the soak test profile.
 * This test applies a moderate, sustained load over a long period
 * to identify memory leaks, resource exhaustion, or performance degradation.
 */
export const options = {
  scenarios: {
    soak_test: {
      executor: 'constant-vus',
      vus: 500,        // A moderate number of constant users
      duration: '4h',  // A long duration to observe stability
    },
  },
  thresholds: {
    // We care more about system stability than strict latency here, but a high
    // error rate is still a critical failure indicator.
    'http_req_failed': ['rate<0.05'], // Allow a slightly higher error rate (5%) over long duration
    'http_reqs': ['count>=1000000'], // Ensure the test runs a significant number of requests
  },
};

/**
 * Setup function: runs once to get a JWT for all VUs.
 */
export function setup() {
  const loginUrl = `${environment.baseUrl}/api/v1/auth/login`;
  const payload = JSON.stringify({
    email: environment.defaultUser.email,
    password: environment.defaultUser.password,
  });
  const res = http.post(loginUrl, payload, { headers: { 'Content-Type': 'application/json' } });
  check(res, { 'login successful': (r) => r.status === 200 });
  const jwt = res.json('accessToken');
  if (!jwt) throw new Error('Login failed in setup, aborting soak test.');
  return { jwt: jwt };
}

/**
 * Default function: Simulates a mix of typical user actions.
 * The goal is to keep a sustained, mixed load on the system.
 * The primary validation occurs by monitoring external dashboards (Grafana, etc.)
 * for memory leaks, CPU creep, or increasing error rates over the 4-hour duration.
 * @param {object} data - Data from the setup function.
 */
export default function (data) {
  const params = {
    headers: {
      'Authorization': `Bearer ${data.jwt}`,
      'Content-Type': 'application/json',
    },
  };

  group('Sustained User Activity', function () {
    // Action 1: Browse dashboard (e.g., get projects)
    const projectsRes = http.get(`${environment.baseUrl}/api/v1/projects`, params);
    check(projectsRes, { 'get projects list status 200': (r) => r.status === 200 });
    sleep(Math.random() * 5 + 5); // Think time 5-10s

    // Action 2: View user settings/profile
    const profileRes = http.get(`${environment.baseUrl}/api/v1/profile`, params);
    check(profileRes, { 'get profile status 200': (r) => r.status === 200 });
    sleep(Math.random() * 5 + 2); // Think time 2-7s

    // Action 3: Start a generation (fire-and-forget to avoid long-held VUs)
    const generationPayload = JSON.stringify({ prompt: `soak test image ${__VU}-${__ITER}` });
    const genRes = http.post(`${environment.baseUrl}/api/v1/generations`, generationPayload, params);
    check(genRes, { 'submit generation status 202': (r) => r.status === 202 });
    sleep(Math.random() * 10 + 10); // Long think time 10-20s after a "heavy" action
  });
}