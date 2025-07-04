import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Trend } from 'k6/metrics';
import { environment } from '../config/environments.js';

const profileTrend = new Trend('p95_profile_response_time');
const projectsTrend = new Trend('p95_projects_response_time');

/**
 * Test options defining the load profile.
 * This test simulates a ramp-up to 10,000 virtual users to test
 * the performance of core, non-AI platform APIs.
 */
export const options = {
  stages: [
    { duration: '2m', target: 1000 },   // Ramp-up to 1,000 users over 2 minutes
    { duration: '5m', target: 1000 },   // Stay at 1,000 users for 5 minutes
    { duration: '2m', target: 10000 },  // Ramp-up to 10,000 users over 2 minutes
    { duration: '10m', target: 10000 }, // Sustain 10,000 users for 10 minutes
    { duration: '5m', target: 0 },      // Ramp-down to 0 users
  ],
  thresholds: {
    'http_req_failed': ['rate<0.01'], // Fail if error rate is > 1%
    'http_req_duration': ['p(95)<500'], // 95% of requests must complete below 500ms
    'p95_profile_response_time': ['p(95)<400'], // Custom metric for profile endpoint
    'p95_projects_response_time': ['p(95)<600'], // Custom metric for projects endpoint
  },
};

/**
 * Setup function: runs once before the test starts.
 * It logs in a single user to retrieve a JWT, which is then shared
 * among all virtual users (VUs). This is efficient for load tests
 * where the login endpoint is not the primary target.
 */
export function setup() {
  const loginUrl = `${environment.baseUrl}/api/v1/auth/login`;
  const payload = JSON.stringify({
    email: environment.defaultUser.email,
    password: environment.defaultUser.password,
  });
  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  const res = http.post(loginUrl, payload, params);
  check(res, { 'login successful': (r) => r.status === 200 });

  const jwt = res.json('accessToken');
  if (!jwt) {
    throw new Error('Login failed, could not retrieve JWT.');
  }
  return { jwt: jwt };
}

/**
 * Default function: the main test logic executed by each VU.
 * @param {object} data - Data returned from the setup() function.
 */
export default function (data) {
  const params = {
    headers: {
      'Authorization': `Bearer ${data.jwt}`,
      'Content-Type': 'application/json',
    },
  };

  group('User Core API Interactions', function () {
    // 1. Get user profile
    group('Get User Profile', function () {
      const profileRes = http.get(`${environment.baseUrl}/api/v1/profile`, params);
      check(profileRes, { 'profile retrieved successfully': (r) => r.status === 200 });
      profileTrend.add(profileRes.timings.duration);
    });

    sleep(1); // Simulate user think time between actions

    // 2. Get list of projects
    group('Get Projects List', function () {
      const projectsRes = http.get(`${environment.baseUrl}/api/v1/projects`, params);
      check(projectsRes, { 'projects retrieved successfully': (r) => r.status === 200 });
      projectsTrend.add(projectsRes.timings.duration);
    });
  });

  // Simulate think time before the VU repeats the loop
  sleep(Math.random() * 3 + 2); // Random sleep between 2s and 5s
}