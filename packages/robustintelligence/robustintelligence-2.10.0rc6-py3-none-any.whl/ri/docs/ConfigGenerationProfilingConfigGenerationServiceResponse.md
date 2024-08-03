# ConfigGenerationProfilingConfigGenerationServiceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**profiling_config** | [**TestrunProfilingConfig**](TestrunProfilingConfig.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.config_generation_profiling_config_generation_service_response import ConfigGenerationProfilingConfigGenerationServiceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigGenerationProfilingConfigGenerationServiceResponse from a JSON string
config_generation_profiling_config_generation_service_response_instance = ConfigGenerationProfilingConfigGenerationServiceResponse.from_json(json)
# print the JSON string representation of the object
print(ConfigGenerationProfilingConfigGenerationServiceResponse.to_json())

# convert the object into a dict
config_generation_profiling_config_generation_service_response_dict = config_generation_profiling_config_generation_service_response_instance.to_dict()
# create an instance of ConfigGenerationProfilingConfigGenerationServiceResponse from a dict
config_generation_profiling_config_generation_service_response_from_dict = ConfigGenerationProfilingConfigGenerationServiceResponse.from_dict(config_generation_profiling_config_generation_service_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

