# CreateFirewallRequestScheduledCTParameters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**eval_data_integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**eval_data_info** | [**RegistryDataInfo**](RegistryDataInfo.md) |  | [optional] 
**eval_pred_integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**eval_pred_info** | [**RegistryPredInfo**](RegistryPredInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.create_firewall_request_scheduled_ct_parameters import CreateFirewallRequestScheduledCTParameters

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFirewallRequestScheduledCTParameters from a JSON string
create_firewall_request_scheduled_ct_parameters_instance = CreateFirewallRequestScheduledCTParameters.from_json(json)
# print the JSON string representation of the object
print(CreateFirewallRequestScheduledCTParameters.to_json())

# convert the object into a dict
create_firewall_request_scheduled_ct_parameters_dict = create_firewall_request_scheduled_ct_parameters_instance.to_dict()
# create an instance of CreateFirewallRequestScheduledCTParameters from a dict
create_firewall_request_scheduled_ct_parameters_from_dict = CreateFirewallRequestScheduledCTParameters.from_dict(create_firewall_request_scheduled_ct_parameters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

