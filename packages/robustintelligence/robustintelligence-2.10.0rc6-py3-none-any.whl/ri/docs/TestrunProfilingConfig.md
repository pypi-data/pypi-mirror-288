# TestrunProfilingConfig

Specifies data and model profiling configurations.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_profiling** | [**TestrunDataProfiling**](TestrunDataProfiling.md) |  | [optional] 
**model_profiling** | [**TestrunModelProfiling**](TestrunModelProfiling.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrun_profiling_config import TestrunProfilingConfig

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunProfilingConfig from a JSON string
testrun_profiling_config_instance = TestrunProfilingConfig.from_json(json)
# print the JSON string representation of the object
print(TestrunProfilingConfig.to_json())

# convert the object into a dict
testrun_profiling_config_dict = testrun_profiling_config_instance.to_dict()
# create an instance of TestrunProfilingConfig from a dict
testrun_profiling_config_from_dict = TestrunProfilingConfig.from_dict(testrun_profiling_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

