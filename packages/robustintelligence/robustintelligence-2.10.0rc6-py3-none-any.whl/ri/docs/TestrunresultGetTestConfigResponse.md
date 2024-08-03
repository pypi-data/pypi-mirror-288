# TestrunresultGetTestConfigResponse

GetTestConfigResponse returns the test config as requested.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**annotated_test_config** | [**TestrunAnnotatedTestConfig**](TestrunAnnotatedTestConfig.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_get_test_config_response import TestrunresultGetTestConfigResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultGetTestConfigResponse from a JSON string
testrunresult_get_test_config_response_instance = TestrunresultGetTestConfigResponse.from_json(json)
# print the JSON string representation of the object
print(TestrunresultGetTestConfigResponse.to_json())

# convert the object into a dict
testrunresult_get_test_config_response_dict = testrunresult_get_test_config_response_instance.to_dict()
# create an instance of TestrunresultGetTestConfigResponse from a dict
testrunresult_get_test_config_response_from_dict = TestrunresultGetTestConfigResponse.from_dict(testrunresult_get_test_config_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

