# ConfigGenerationCategoryConfigGenerationServiceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**stress_test_categories** | [**List[TestrunTestCategoryType]**](TestrunTestCategoryType.md) |  | [optional] 
**continuous_test_categories** | [**List[TestrunTestCategoryType]**](TestrunTestCategoryType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.config_generation_category_config_generation_service_response import ConfigGenerationCategoryConfigGenerationServiceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigGenerationCategoryConfigGenerationServiceResponse from a JSON string
config_generation_category_config_generation_service_response_instance = ConfigGenerationCategoryConfigGenerationServiceResponse.from_json(json)
# print the JSON string representation of the object
print(ConfigGenerationCategoryConfigGenerationServiceResponse.to_json())

# convert the object into a dict
config_generation_category_config_generation_service_response_dict = config_generation_category_config_generation_service_response_instance.to_dict()
# create an instance of ConfigGenerationCategoryConfigGenerationServiceResponse from a dict
config_generation_category_config_generation_service_response_from_dict = ConfigGenerationCategoryConfigGenerationServiceResponse.from_dict(config_generation_category_config_generation_service_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

