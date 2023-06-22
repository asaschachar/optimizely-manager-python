# Optimizely Manager Python
                                                                        
## Installation
```
pip install git+git://github.com/asaschachar/optimizely-manager-python.git#v2.0.0
```
 
## Setup 
At your application startup:
```python
from optimizely_manager import optimizely_manager
optimizely_manager.configure(
  sdk_key='C3666onUgdBu8gchQfqzva',
)
optimizely.fetch_configuration(timeout_ms=500) # Blocking fetch for feature configuration
optimizely.start_live_updates(update_interval_sec=1) # Non-blocking polling thread for feature configuration
```

## Usage
When you want to use a feature flag:
```
optimizely = optimizely_manager.get_client()
enabled = optimizely.is_feature_enabled("sale_price", user_id)
```                                                                     
                                                                        
If you are using a feature flag in another file, get the optimizely instance first                                                                        
```python
from optimizely_manager import optimizely_manager
optimizely = optimizely_manager.get_client();
enabled = optimizely.is_feature_enabled("sale_price", user_id)
```

## TODO
- Add some tests
