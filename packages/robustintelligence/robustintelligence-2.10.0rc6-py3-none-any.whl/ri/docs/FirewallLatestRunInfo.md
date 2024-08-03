# FirewallLatestRunInfo

LatestRunInfo tracks the latest run bin in the firewall.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bin** | [**RimeTimeInterval**](RimeTimeInterval.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.firewall_latest_run_info import FirewallLatestRunInfo

# TODO update the JSON string below
json = "{}"
# create an instance of FirewallLatestRunInfo from a JSON string
firewall_latest_run_info_instance = FirewallLatestRunInfo.from_json(json)
# print the JSON string representation of the object
print(FirewallLatestRunInfo.to_json())

# convert the object into a dict
firewall_latest_run_info_dict = firewall_latest_run_info_instance.to_dict()
# create an instance of FirewallLatestRunInfo from a dict
firewall_latest_run_info_from_dict = FirewallLatestRunInfo.from_dict(firewall_latest_run_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

