name = "optimizely_manager"
__all__ = ['OptimizelyManager']

import logging
import requests
import json
import random
from optimizely import optimizely, logger as optimizely_logging
from threading import Timer


class _UinintializedClient():
  def __init__(self, log_level=None):
    self.log_level = log_level or logging.DEBUG

  def is_feature_enabled(self, *args):
    logger = optimizely_logging.SimpleLogger(min_level=self.log_level)

    UNIINITIALIZED_ERROR = """MANAGER: is_feature_enabled called but Optimizely not yet initialized.

      If you just started a web application or app server, try the request again.

      OR try moving your OptimizelyManager initialization higher in your application startup code
      OR move your is_feature_enabled call later in your application lifecycle.

      If this error persists, contact Optimizely!

      TODO: Enable a blocking for Optimizely through the manager
    """
    logger.log(logging.DEBUG, UNIINITIALIZED_ERROR)


class _OptimizelyManagerSingleton:
  def __init__(self, sdk_key=None, log_level=None, **kwargs):
    self._timer = None
    self.interval = 1 # TODO: Provide configurability
    self.is_running = False
    self.start()
    self.current_datafile = {}
    self.sdk_key = sdk_key
    self.log_level = log_level or logging.DEBUG
    self.sdkParameters = kwargs
    self.optimizely_client_instance = _UinintializedClient(log_level=log_level)
    self.logger = optimizely_logging.SimpleLogger(min_level=log_level)

  def request_datafile(self):
    DATAFILE_URL = 'https://cdn.optimizely.com/datafiles/%s.json' % self.sdk_key

    latest_datafile = requests.get(DATAFILE_URL).text
    current_datafile_string = json.dumps(self.current_datafile, sort_keys=True)
    latest_datafile_string = json.dumps(latest_datafile, sort_keys=True)

    if current_datafile_string != latest_datafile_string:
      self.logger.log(logging.DEBUG, 'MANAGER: Received an updated datafile and is re-initializing')
      self.current_datafile = latest_datafile

      # The datafile is different! Let's re-instantiate the client
      self.optimizely_client_instance = optimizely.Optimizely(
        datafile=latest_datafile,
        logger=self.logger,
        **self.sdkParameters
      )

  def _run(self):
    self.is_running = False
    self.start()
    self.request_datafile()

  def start(self):
    if not self.is_running:
      self._timer = Timer(self.interval, self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False

  def is_feature_enabled(self, feature_key, user_id=None):
    if not user_id:
      self.logger.log(logging.DEBUG, 'MANAGER: No user_id supplied to is_feature_enabled, using random string instead.')
      user_id = user_id or str(random.randint(1, 100))

    result = self.optimizely_client_instance.is_feature_enabled(feature_key, user_id)
    return result

  def get_client(self):
    return self

  def fetchConfiguration(self, timeout=500):
    pass

  def startPollingThread(self, update_interval=1000):
    pass

  def startLiveUpdates(self, update_interval=1000):
    pass


class OptimizelyManager:

  instance = None

  def __init__(self, *args, **kwargs):
    if not OptimizelyManager.instance:
      OptimizelyManager.instance = _OptimizelyManagerSingleton(*args, **kwargs)

  def is_feature_enabled(self, feature_key, user_id=None):
    return OptimizelyManager.instance.is_feature_enabled(feature_key, user_id=user_id)

  def fetchConfiguration(self, timeout=500):
    pass

  def startPollingThread(self, update_interval=1000):
    pass

  def startLiveUpdates(self, update_interval=1000):
    pass

