# RimeListFirewallInstancesRequest

ListFirewallInstancesRequest is the request to list firewall instance metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page_size** | **str** |  | [optional] 
**page_token** | **str** | Specifies a page of the list returned by a ListFirewallInstances query. The ListFirewallInstances query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageQuery field. | [optional] 
**first_page_query** | [**ListFirewallInstancesRequestListFirewallInstancesQuery**](ListFirewallInstancesRequestListFirewallInstancesQuery.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_firewall_instances_request import RimeListFirewallInstancesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListFirewallInstancesRequest from a JSON string
rime_list_firewall_instances_request_instance = RimeListFirewallInstancesRequest.from_json(json)
# print the JSON string representation of the object
print(RimeListFirewallInstancesRequest.to_json())

# convert the object into a dict
rime_list_firewall_instances_request_dict = rime_list_firewall_instances_request_instance.to_dict()
# create an instance of RimeListFirewallInstancesRequest from a dict
rime_list_firewall_instances_request_from_dict = RimeListFirewallInstancesRequest.from_dict(rime_list_firewall_instances_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

