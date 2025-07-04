import { ReportHandler } from 'web-vitals';

/**
 * Measures and reports Core Web Vitals performance metrics.
 * This function uses the 'web-vitals' library to get metrics like
 * Largest Contentful Paint (LCP), First Input Delay (FID), and
 * Cumulative Layout Shift (CLS).
 *
 * @param onPerfEntry - A callback function that will be invoked with the performance metric.
 *                      This can be used to log the metric to the console or send it to an
 *                      analytics service.
 */
const reportWebVitals = (onPerfEntry?: ReportHandler): void => {
  if (onPerfEntry && typeof onPerfEntry === 'function') {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

export { reportWebVitals };