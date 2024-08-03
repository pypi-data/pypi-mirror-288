# ConfigGenerationTestSuiteConfigGenerationServiceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_suite_config** | [**TestrunTestSuiteConfig**](TestrunTestSuiteConfig.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.config_generation_test_suite_config_generation_service_response import ConfigGenerationTestSuiteConfigGenerationServiceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigGenerationTestSuiteConfigGenerationServiceResponse from a JSON string
config_generation_test_suite_config_generation_service_response_instance = ConfigGenerationTestSuiteConfigGenerationServiceResponse.from_json(json)
# print the JSON string representation of the object
print(ConfigGenerationTestSuiteConfigGenerationServiceResponse.to_json())

# convert the object into a dict
config_generation_test_suite_config_generation_service_response_dict = config_generation_test_suite_config_generation_service_response_instance.to_dict()
# create an instance of ConfigGenerationTestSuiteConfigGenerationServiceResponse from a dict
config_generation_test_suite_config_generation_service_response_from_dict = ConfigGenerationTestSuiteConfigGenerationServiceResponse.from_dict(config_generation_test_suite_config_generation_service_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

