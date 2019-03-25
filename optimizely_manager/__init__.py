name = "optimizely_manager"
__all__ = ['optimizely_manager']

import logging
import requests
import json
import random
from six import with_metaclass
from optimizely import optimizely, logger as optimizely_logging
from threading import Timer


class _Singleton(type):
  """ Singleton interface to ensure there is only one instance of the
  Optimizely Manager at once """
    _instances = {}
    def __call__(cls, *args, **kwargs):
      if cls not in cls._instances:
        cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _UinintializedClient():
  """ Dummy Optimizely Client for when the datafile has not been fetched yet."""
  def __init__(self, log_level=None):
    self.log_level = log_level or logging.DEBUG

  def is_feature_enabled(self, *args):
    logger = optimizely_logging.SimpleLogger(min_level=self.log_level)

    UNIINITIALIZED_ERROR = """Optimizely: is_feature_enabled called but Optimizely not yet initialized.

      If you just started a web application or app server, try the request again.

      OR use the optimizely.fetch_configuration(timeout_ms=500) method to block initialization until the application is ready
      OR try moving your OptimizelyManager initialization higher in your application startup code
      OR move your is_feature_enabled call later in your application lifecycle.

      If this error persists, contact Optimizely!

    """
    logger.log(logging.INFO, UNIINITIALIZED_ERROR)


class _OptimizelyManager(with_metaclass(_Singleton)):
  """ Convenience wrapper for the SDK that provides convenience methods for datafile management """
  def __init__(self, sdk_key=None, log_level=None, **kwargs):
    self._timer = None
    self.is_running = False

  def configure(self, sdk_key=None, log_level=None, **kwargs):
    """ Initialize the datafile manager with settings that are also passed to
    the core Optimizely SDK

    Parameters:
      sdk_key (string): Key specific to your Optimizely project and environment for fetching the correct datafile
      log_level (string): Log level for the SDK to log to console.
      **kwargs: See Optimizely SDK create_instance parameters

    """
    self.current_datafile = { 'revision': '0' }
    self.sdk_key = sdk_key
    self.log_level = log_level or logging.DEBUG
    self.sdkParameters = kwargs
    self.optimizely_client_instance = _UinintializedClient(log_level=log_level)
    self.logger = optimizely_logging.SimpleLogger(min_level=log_level)

  def request_datafile(self, timeout=None):
    DATAFILE_URL = 'https://cdn.optimizely.com/datafiles/%s.json' % self.sdk_key

    try:
      latest_datafile = requests.get(DATAFILE_URL, timeout=timeout).json()
    except:
      self.logger.log(logging.WARNING, 'Optimizely: Timeout hit while trying to fetch the datafile')
    else:
      if int(self.current_datafile['revision']) < int(latest_datafile['revision']):
        self.logger.log(logging.INFO, 'Optimizely: Received an updated datafile and is initializing')
        self.current_datafile = latest_datafile

        # TODO: Preserve the notification center
        # The datafile is different! Let's re-instantiate the client
        self.optimizely_client_instance = optimizely.Optimizely(
          datafile=json.dumps(latest_datafile),
          logger=self.logger,
          **self.sdkParameters
        )

  def _run(self):
    self.is_running = False
    self._start()
    self.request_datafile()

  def _start(self, interval=1):
    if not self.is_running:
      self._timer = Timer(interval, self._run)
      self._timer.start()
      self.is_running = True

  def _stop(self):
    self._timer.cancel()
    self.is_running = False

  def get_client(self):
    """ Returns an Optimizely client instance """
    return self.optimizely_client_instance

  def fetch_datafile(self, timeout_ms=500):
    """ Blocking request to fetch the datafile.

    Parameters:
      timeout_ms (int): Max number of milliseconds to block the main thread
    """
    self.logger.log(logging.INFO, 'Optimizely: Blocking fetch for feature configuration')
    self.request_datafile(timeout=(timeout_ms / 1000))

  def start_live_updates(self, update_interval_sec=1):
    """ Start a separate background thread that will poll for updates to the datafile on
    an interval of update_interval_sec seconds

    Parameters:
      update_interval_sec (int): Seconds to wait in between requesting the datafile on the polling thread
    """
    self.logger.log(logging.INFO, 'Optimizely: Starting background thread to poll for feature configuration updates')
    self._start(update_interval_sec)

  def stop_live_updates(self):
    """ Method to stop the background thread from requesting another datafile """
    self._stop();


optimizely_manager = _OptimizelyManager()
