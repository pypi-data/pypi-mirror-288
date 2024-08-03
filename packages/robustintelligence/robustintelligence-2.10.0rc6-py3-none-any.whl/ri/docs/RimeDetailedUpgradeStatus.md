# RimeDetailedUpgradeStatus

DetailedUpgradeStatus is an UpgradeStatus with additional information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**RimeUpgradeStatus**](RimeUpgradeStatus.md) |  | [optional] 
**last_update_time** | **datetime** |  | 
**error_message** | **str** | The error message if the status is failed. | [optional] 

## Example

```python
from ri.apiclient.models.rime_detailed_upgrade_status import RimeDetailedUpgradeStatus

# TODO update the JSON string below
json = "{}"
# create an instance of RimeDetailedUpgradeStatus from a JSON string
rime_detailed_upgrade_status_instance = RimeDetailedUpgradeStatus.from_json(json)
# print the JSON string representation of the object
print(RimeDetailedUpgradeStatus.to_json())

# convert the object into a dict
rime_detailed_upgrade_status_dict = rime_detailed_upgrade_status_instance.to_dict()
# create an instance of RimeDetailedUpgradeStatus from a dict
rime_detailed_upgrade_status_from_dict = RimeDetailedUpgradeStatus.from_dict(rime_detailed_upgrade_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

