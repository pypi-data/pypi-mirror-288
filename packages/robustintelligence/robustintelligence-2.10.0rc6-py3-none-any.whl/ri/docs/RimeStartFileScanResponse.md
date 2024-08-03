# RimeStartFileScanResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job** | [**RimeJobMetadata**](RimeJobMetadata.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_start_file_scan_response import RimeStartFileScanResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeStartFileScanResponse from a JSON string
rime_start_file_scan_response_instance = RimeStartFileScanResponse.from_json(json)
# print the JSON string representation of the object
print(RimeStartFileScanResponse.to_json())

# convert the object into a dict
rime_start_file_scan_response_dict = rime_start_file_scan_response_instance.to_dict()
# create an instance of RimeStartFileScanResponse from a dict
rime_start_file_scan_response_from_dict = RimeStartFileScanResponse.from_dict(rime_start_file_scan_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

