# RimeGetFirewallResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall** | [**FirewallFirewall**](FirewallFirewall.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_firewall_response import RimeGetFirewallResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetFirewallResponse from a JSON string
rime_get_firewall_response_instance = RimeGetFirewallResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetFirewallResponse.to_json())

# convert the object into a dict
rime_get_firewall_response_dict = rime_get_firewall_response_instance.to_dict()
# create an instance of RimeGetFirewallResponse from a dict
rime_get_firewall_response_from_dict = RimeGetFirewallResponse.from_dict(rime_get_firewall_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

