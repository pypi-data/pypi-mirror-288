# ListFileScanResultsRequestFileScanQuery

Query message for selecting File Scan results.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**model_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.list_file_scan_results_request_file_scan_query import ListFileScanResultsRequestFileScanQuery

# TODO update the JSON string below
json = "{}"
# create an instance of ListFileScanResultsRequestFileScanQuery from a JSON string
list_file_scan_results_request_file_scan_query_instance = ListFileScanResultsRequestFileScanQuery.from_json(json)
# print the JSON string representation of the object
print(ListFileScanResultsRequestFileScanQuery.to_json())

# convert the object into a dict
list_file_scan_results_request_file_scan_query_dict = list_file_scan_results_request_file_scan_query_instance.to_dict()
# create an instance of ListFileScanResultsRequestFileScanQuery from a dict
list_file_scan_results_request_file_scan_query_from_dict = ListFileScanResultsRequestFileScanQuery.from_dict(list_file_scan_results_request_file_scan_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

