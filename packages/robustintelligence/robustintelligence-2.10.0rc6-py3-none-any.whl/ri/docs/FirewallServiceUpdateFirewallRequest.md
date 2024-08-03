# FirewallServiceUpdateFirewallRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**firewall** | [**FirewallServiceUpdateFirewallRequestFirewall**](FirewallServiceUpdateFirewallRequestFirewall.md) |  | [optional] 
**mask** | **str** | Field mask specifies which fields of the firewall to update. | [optional] 

## Example

```python
from ri.apiclient.models.firewall_service_update_firewall_request import FirewallServiceUpdateFirewallRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FirewallServiceUpdateFirewallRequest from a JSON string
firewall_service_update_firewall_request_instance = FirewallServiceUpdateFirewallRequest.from_json(json)
# print the JSON string representation of the object
print(FirewallServiceUpdateFirewallRequest.to_json())

# convert the object into a dict
firewall_service_update_firewall_request_dict = firewall_service_update_firewall_request_instance.to_dict()
# create an instance of FirewallServiceUpdateFirewallRequest from a dict
firewall_service_update_firewall_request_from_dict = FirewallServiceUpdateFirewallRequest.from_dict(firewall_service_update_firewall_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

