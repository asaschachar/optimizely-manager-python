# Optimizely Datafile Manager Python
                                                                        
## Installation
```
pip install git+git://github.com/asaschachar/optimizely-manager-python.git#v2.0.0
```
 
## Setup 
At your application startup:
```
from optimizely_manager import OptimizelyManager
optimizely = OptimizelyManager(
  sdk_key='XFjmGNFQK1snQExC1vgynY' # This is your real SDK Key.
)
optimizely.fetch_configuration(timeout_ms=500) # Blocking fetch for feature configuration
optimizely.start_live_updates(update_interval_sec=1) # Non-blocking polling thread for feature configuration
```

## Usage
When you want to use a feature flag:
```
enabled = optimizely.is_feature_enabled("sale_price")
```                                                                     
                                                                        
If you are using a feature flag in another file, get the optimizely instance first                                                                        
```
from optimizely_manager import OptimizelyManager
const optimizely = OptimizelyManager.instance.get_client();
enabled = optimizelyInstance.is_feature_enabled("sale_price")
```

## Other APIs
```
optimizely.start_polling_thread(update_interval_sec=1)
```
