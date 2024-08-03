# TestrunresultListFeatureResultsResponse

ListFeatureResultsResponse returns a list of feature results as requested.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature_results** | [**List[TestrunresultTestFeatureResult]**](TestrunresultTestFeatureResult.md) | The list of feature results. | [optional] 
**next_page_token** | **str** | A token representing the next page from the list returned by a ListFeatureResults query. | [optional] 
**has_more** | **bool** | A Boolean flag that specifies whether there are more feature results to return. | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_list_feature_results_response import TestrunresultListFeatureResultsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultListFeatureResultsResponse from a JSON string
testrunresult_list_feature_results_response_instance = TestrunresultListFeatureResultsResponse.from_json(json)
# print the JSON string representation of the object
print(TestrunresultListFeatureResultsResponse.to_json())

# convert the object into a dict
testrunresult_list_feature_results_response_dict = testrunresult_list_feature_results_response_instance.to_dict()
# create an instance of TestrunresultListFeatureResultsResponse from a dict
testrunresult_list_feature_results_response_from_dict = TestrunresultListFeatureResultsResponse.from_dict(testrunresult_list_feature_results_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

