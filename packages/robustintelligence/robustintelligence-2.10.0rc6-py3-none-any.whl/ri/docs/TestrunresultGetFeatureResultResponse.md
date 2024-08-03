# TestrunresultGetFeatureResultResponse

GetFeatureResultResponse returns the feature result as requested.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature_result** | [**TestrunresultTestFeatureResult**](TestrunresultTestFeatureResult.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_get_feature_result_response import TestrunresultGetFeatureResultResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultGetFeatureResultResponse from a JSON string
testrunresult_get_feature_result_response_instance = TestrunresultGetFeatureResultResponse.from_json(json)
# print the JSON string representation of the object
print(TestrunresultGetFeatureResultResponse.to_json())

# convert the object into a dict
testrunresult_get_feature_result_response_dict = testrunresult_get_feature_result_response_instance.to_dict()
# create an instance of TestrunresultGetFeatureResultResponse from a dict
testrunresult_get_feature_result_response_from_dict = TestrunresultGetFeatureResultResponse.from_dict(testrunresult_get_feature_result_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

