import {Trend} from "k6/metrics";

/**
 * This file centralizes environment-specific configurations for k6 tests.
 * It allows the same test logic to be executed against different target
 * environments (e.g., staging, pre-prod, production) by simply changing
 * an environment variable.
 */

// Load environment variables from a .env file if present
// Note: k6 does not directly support node's `dotenv` package.
// Environment variables must be passed via the command line, e.g.,
// k6 run -e STAGING_USER_EMAIL=... -e STAGING_USER_PASSWORD=... script.js
// Or using a Docker environment file.

export const environments = {
  staging: {
    baseUrl: 'https://staging-api.creativeflow.ai',
    defaultUser: {
      email: __ENV.STAGING_USER_EMAIL,
      password: __ENV.STAGING_USER_PASSWORD,
    },
  },
  // Example of another environment configuration
  // preprod: {
  //   baseUrl: 'https://preprod-api.creativeflow.ai',
  //   defaultUser: {
  //     email: __ENV.PREPROD_USER_EMAIL,
  //     password: __ENV.PREPROD_USER_PASSWORD,
  //   },
  // }
};

// Select the environment to use, defaulting to 'staging'
export const environment = environments[__ENV.TARGET_ENV || 'staging'];

if (!environment) {
  throw new Error(`Configuration for TARGET_ENV "${__ENV.TARGET_ENV}" not found.`);
}
if (!environment.defaultUser.email || !environment.defaultUser.password) {
  throw new Error('User credentials for the target environment are not provided. Please set STAGING_USER_EMAIL and STAGING_USER_PASSWORD environment variables.');
}