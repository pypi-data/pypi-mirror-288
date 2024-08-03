# TestrunresultListTestRunsRequestQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**testing_type** | [**RimeTestType**](RimeTestType.md) |  | [optional] 
**schedule_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_list_test_runs_request_query import TestrunresultListTestRunsRequestQuery

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultListTestRunsRequestQuery from a JSON string
testrunresult_list_test_runs_request_query_instance = TestrunresultListTestRunsRequestQuery.from_json(json)
# print the JSON string representation of the object
print(TestrunresultListTestRunsRequestQuery.to_json())

# convert the object into a dict
testrunresult_list_test_runs_request_query_dict = testrunresult_list_test_runs_request_query_instance.to_dict()
# create an instance of TestrunresultListTestRunsRequestQuery from a dict
testrunresult_list_test_runs_request_query_from_dict = TestrunresultListTestRunsRequestQuery.from_dict(testrunresult_list_test_runs_request_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

