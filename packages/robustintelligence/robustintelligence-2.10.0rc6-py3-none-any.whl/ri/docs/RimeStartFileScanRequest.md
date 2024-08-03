# RimeStartFileScanRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**model_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**run_time_info** | [**RuntimeinfoRunTimeInfo**](RuntimeinfoRunTimeInfo.md) |  | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_start_file_scan_request import RimeStartFileScanRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeStartFileScanRequest from a JSON string
rime_start_file_scan_request_instance = RimeStartFileScanRequest.from_json(json)
# print the JSON string representation of the object
print(RimeStartFileScanRequest.to_json())

# convert the object into a dict
rime_start_file_scan_request_dict = rime_start_file_scan_request_instance.to_dict()
# create an instance of RimeStartFileScanRequest from a dict
rime_start_file_scan_request_from_dict = RimeStartFileScanRequest.from_dict(rime_start_file_scan_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

