# RimeCreateFirewallResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_firewall_response import RimeCreateFirewallResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateFirewallResponse from a JSON string
rime_create_firewall_response_instance = RimeCreateFirewallResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateFirewallResponse.to_json())

# convert the object into a dict
rime_create_firewall_response_dict = rime_create_firewall_response_instance.to_dict()
# create an instance of RimeCreateFirewallResponse from a dict
rime_create_firewall_response_from_dict = RimeCreateFirewallResponse.from_dict(rime_create_firewall_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

