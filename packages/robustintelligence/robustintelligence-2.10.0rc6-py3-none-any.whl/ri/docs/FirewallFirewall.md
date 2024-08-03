# FirewallFirewall


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**model_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**bin_size** | **str** |  | [optional] 
**ref_data_id** | **str** | The semantic ID of the reference dataset. This should correspond with the primary key in the Dataset Registry. | [optional] 
**scheduled_ct_info** | [**FirewallScheduledCTInfo**](FirewallScheduledCTInfo.md) |  | [optional] 
**risk_scores** | [**List[RiskscoreRiskScore]**](RiskscoreRiskScore.md) |  | [optional] 
**test_category_severities** | [**List[FirewallTestCategorySeverity]**](FirewallTestCategorySeverity.md) |  | [optional] 
**latest_run_info** | [**FirewallLatestRunInfo**](FirewallLatestRunInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.firewall_firewall import FirewallFirewall

# TODO update the JSON string below
json = "{}"
# create an instance of FirewallFirewall from a JSON string
firewall_firewall_instance = FirewallFirewall.from_json(json)
# print the JSON string representation of the object
print(FirewallFirewall.to_json())

# convert the object into a dict
firewall_firewall_dict = firewall_firewall_instance.to_dict()
# create an instance of FirewallFirewall from a dict
firewall_firewall_from_dict = FirewallFirewall.from_dict(firewall_firewall_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

