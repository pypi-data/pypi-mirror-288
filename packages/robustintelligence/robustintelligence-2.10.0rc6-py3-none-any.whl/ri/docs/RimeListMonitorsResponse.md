# RimeListMonitorsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**monitors** | [**List[MonitorMonitor]**](MonitorMonitor.md) | The list of monitors. | [optional] 
**next_page_token** | **str** | The pagination token. | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_monitors_response import RimeListMonitorsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListMonitorsResponse from a JSON string
rime_list_monitors_response_instance = RimeListMonitorsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListMonitorsResponse.to_json())

# convert the object into a dict
rime_list_monitors_response_dict = rime_list_monitors_response_instance.to_dict()
# create an instance of RimeListMonitorsResponse from a dict
rime_list_monitors_response_from_dict = RimeListMonitorsResponse.from_dict(rime_list_monitors_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

