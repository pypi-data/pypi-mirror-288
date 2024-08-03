# RimeGetFileScanResultResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_scan_result** | [**SchemafilescanningFileScanResult**](SchemafilescanningFileScanResult.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_file_scan_result_response import RimeGetFileScanResultResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetFileScanResultResponse from a JSON string
rime_get_file_scan_result_response_instance = RimeGetFileScanResultResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetFileScanResultResponse.to_json())

# convert the object into a dict
rime_get_file_scan_result_response_dict = rime_get_file_scan_result_response_instance.to_dict()
# create an instance of RimeGetFileScanResultResponse from a dict
rime_get_file_scan_result_response_from_dict = RimeGetFileScanResultResponse.from_dict(rime_get_file_scan_result_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

