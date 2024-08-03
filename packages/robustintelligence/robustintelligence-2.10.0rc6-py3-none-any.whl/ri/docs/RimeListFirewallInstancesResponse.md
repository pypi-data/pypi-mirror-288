# RimeListFirewallInstancesResponse

ListFirewallInstancesResponse returns the list of firewall instance metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fw_instances** | [**List[GenerativefirewallFirewallInstanceInfo]**](GenerativefirewallFirewallInstanceInfo.md) |  | [optional] 
**next_page_token** | **str** | Use this page token in your next ListFirewallInstances call to access the next page of results. | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_firewall_instances_response import RimeListFirewallInstancesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListFirewallInstancesResponse from a JSON string
rime_list_firewall_instances_response_instance = RimeListFirewallInstancesResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListFirewallInstancesResponse.to_json())

# convert the object into a dict
rime_list_firewall_instances_response_dict = rime_list_firewall_instances_response_instance.to_dict()
# create an instance of RimeListFirewallInstancesResponse from a dict
rime_list_firewall_instances_response_from_dict = RimeListFirewallInstancesResponse.from_dict(rime_list_firewall_instances_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

