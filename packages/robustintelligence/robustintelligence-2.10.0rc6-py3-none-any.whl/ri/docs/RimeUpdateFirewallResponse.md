# RimeUpdateFirewallResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall** | [**FirewallFirewall**](FirewallFirewall.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_update_firewall_response import RimeUpdateFirewallResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUpdateFirewallResponse from a JSON string
rime_update_firewall_response_instance = RimeUpdateFirewallResponse.from_json(json)
# print the JSON string representation of the object
print(RimeUpdateFirewallResponse.to_json())

# convert the object into a dict
rime_update_firewall_response_dict = rime_update_firewall_response_instance.to_dict()
# create an instance of RimeUpdateFirewallResponse from a dict
rime_update_firewall_response_from_dict = RimeUpdateFirewallResponse.from_dict(rime_update_firewall_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

