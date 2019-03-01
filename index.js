/**
 * Optimizely Datafile Manager Node
 *
 * USAGE - INSTALLATION
 *   // Save this file in a file named optimizely-manager.js
 *   const OptimizelyManager = require('./optimizely-manager');
 *   const optimizely = new OptimizelyManager({
 *     sdkKey: 'Ly8FQj6vSaDcZUjySoWnWz'
 *   })
 *
 * USAGE - USING A FEATURE FLAG
 *   const enabled = optimizely.isFeatureEnabled('sale_price', userId);
 *
 *   OR
 *
 *   const optimizely = OptimizelyManager.instance.getClient();
 *   const enabled = optimizely.isFeatureEnabled('sale_price', 'TEST_ID');
 */
const request = require('request-promise');
const assert = require('assert');
const optimizely = require('@optimizely/optimizely-sdk');
const defaultLogger = require('@optimizely/optimizely-sdk/lib/plugins/logger');
const LOG_LEVEL = require('@optimizely/optimizely-sdk/lib/utils/enums').LOG_LEVEL;

function OptimizelyManager({ sdkKey, debug, ...rest }) {
  let currentDatafile = {};
  let logLevel = debug ? LOG_LEVEL.DEBUG : LOG_LEVEL.WARNING;
  let logger = defaultLogger.createLogger({ logLevel })

  logger.log(LOG_LEVEL.DEBUG, 'MANAGER: Loading Optimizely Manager');
  let optimizelyClientInstance = {
    isFeatureEnabled() {
      const UNIINITIALIZED_ERROR = `MANAGER: isFeatureEnabled called but Optimizely not yet initialized.

        If you just started a web application or app server, try the request again.

        OR try moving your OptimizelyManager initialization higher in your application startup code
        OR move your isFeatureEnabled call later in your application lifecycle.

        If this error persists, contact Optimizely!

        TODO: Enable a blocking for Optimizely through the manager
      `;
      if (debug) {
        throw new Error(UNIINITIALIZED_ERROR)
      } else {
        logger.log(LOG_LEVEL.DEBUG, UNIINITIALIZED_ERROR)
      }
    }
  }

  function pollForDatafile() {
    // Request the datafile every second. If the datafile has changed
    // since the last time we've seen it, then re-instantiate the client
    const DATAFILE_URL = `https://cdn.optimizely.com/datafiles/${sdkKey}.json`;

    request(DATAFILE_URL)
      .then(async (latestDatafile) => {
        try {
          assert.deepEqual(currentDatafile, latestDatafile)
        } catch (err) {
          logger.log(LOG_LEVEL.DEBUG, 'MANAGER: Received an updated datafile and is re-initializing')
          // The datafile is different! Let's re-instantiate the client
          optimizelyClientInstance = optimizely.createInstance({
            datafile: latestDatafile,
            logger,
            ...rest
          });
          currentDatafile = latestDatafile;
        }
      })
  }

  setInterval(pollForDatafile, 1000);

  return {
    isFeatureEnabled(...args) {
      return optimizelyClientInstance.isFeatureEnabled(...args);
    },

    getClient() {
      return optimizelyClientInstance;
    }
  }
}


class Singleton {
  constructor(...args) {
    if (!Singleton.instance) {
      Singleton.instance = new OptimizelyManager(...args);
    }
  }

  isFeatureEnabled(...args) {
    return Singleton.instance.isFeatureEnabled(...args);
  }
}

module.exports = Singleton;
