# RimeListFileScanResultsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[SchemafilescanningFileScanResult]**](SchemafilescanningFileScanResult.md) |  | [optional] 
**next_page_token** | **str** | A token representing the next page from the list returned by a ListFileScanResults query. | [optional] 
**has_more** | **bool** | A Boolean that specifies whether there are more File Scan results to return. | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_file_scan_results_response import RimeListFileScanResultsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListFileScanResultsResponse from a JSON string
rime_list_file_scan_results_response_instance = RimeListFileScanResultsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListFileScanResultsResponse.to_json())

# convert the object into a dict
rime_list_file_scan_results_response_dict = rime_list_file_scan_results_response_instance.to_dict()
# create an instance of RimeListFileScanResultsResponse from a dict
rime_list_file_scan_results_response_from_dict = RimeListFileScanResultsResponse.from_dict(rime_list_file_scan_results_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

