# RimeCreateFirewallRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**model_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**bin_size** | **str** | Duration of each bin size of continuous tests. | 
**ref_data_id** | **str** | Uniquely specifies a reference data set. | 
**scheduled_ct_parameters** | [**CreateFirewallRequestScheduledCTParameters**](CreateFirewallRequestScheduledCTParameters.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_firewall_request import RimeCreateFirewallRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateFirewallRequest from a JSON string
rime_create_firewall_request_instance = RimeCreateFirewallRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateFirewallRequest.to_json())

# convert the object into a dict
rime_create_firewall_request_dict = rime_create_firewall_request_instance.to_dict()
# create an instance of RimeCreateFirewallRequest from a dict
rime_create_firewall_request_from_dict = RimeCreateFirewallRequest.from_dict(rime_create_firewall_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

