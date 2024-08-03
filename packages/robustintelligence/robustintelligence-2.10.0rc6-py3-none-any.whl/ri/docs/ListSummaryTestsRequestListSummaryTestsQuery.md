# ListSummaryTestsRequestListSummaryTestsQuery

The resulting query is the intersection of the following constraints.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_run_id** | **str** | The ID of the test run associated with summary tests. Specify exactly one of the page_token field or this field. | [optional] 

## Example

```python
from ri.apiclient.models.list_summary_tests_request_list_summary_tests_query import ListSummaryTestsRequestListSummaryTestsQuery

# TODO update the JSON string below
json = "{}"
# create an instance of ListSummaryTestsRequestListSummaryTestsQuery from a JSON string
list_summary_tests_request_list_summary_tests_query_instance = ListSummaryTestsRequestListSummaryTestsQuery.from_json(json)
# print the JSON string representation of the object
print(ListSummaryTestsRequestListSummaryTestsQuery.to_json())

# convert the object into a dict
list_summary_tests_request_list_summary_tests_query_dict = list_summary_tests_request_list_summary_tests_query_instance.to_dict()
# create an instance of ListSummaryTestsRequestListSummaryTestsQuery from a dict
list_summary_tests_request_list_summary_tests_query_from_dict = ListSummaryTestsRequestListSummaryTestsQuery.from_dict(list_summary_tests_request_list_summary_tests_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

