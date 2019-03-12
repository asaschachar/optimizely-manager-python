# Optimizely Datafile Manager Python
                                                                        
## Installation
```
pip install git+git://github.com/asaschachar/optimizely-manager-python.git#v1.1.0
```
 
## Setup 
At your application startup:
```
from optimizely_manager import OptimizelyManager
optimizely = OptimizelyManager(
  sdk_key='C3666onUgdBu8gchQfqzva',
)
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
