# RimeUpsertFirewallInstanceResponse

UpsertFirewallInstanceResponse is the response for UpsertFirewallInstance.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_instance_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_upsert_firewall_instance_response import RimeUpsertFirewallInstanceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUpsertFirewallInstanceResponse from a JSON string
rime_upsert_firewall_instance_response_instance = RimeUpsertFirewallInstanceResponse.from_json(json)
# print the JSON string representation of the object
print(RimeUpsertFirewallInstanceResponse.to_json())

# convert the object into a dict
rime_upsert_firewall_instance_response_dict = rime_upsert_firewall_instance_response_instance.to_dict()
# create an instance of RimeUpsertFirewallInstanceResponse from a dict
rime_upsert_firewall_instance_response_from_dict = RimeUpsertFirewallInstanceResponse.from_dict(rime_upsert_firewall_instance_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

