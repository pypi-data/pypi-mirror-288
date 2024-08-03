# MonitorMonitor


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**name** | **str** | The name of the monitor. | [optional] 
**firewall_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**monitor_type** | [**MonitorMonitorType**](MonitorMonitorType.md) |  | [optional] 
**risk_category_type** | [**RiskscoreRiskCategoryType**](RiskscoreRiskCategoryType.md) |  | [optional] 
**test_category** | [**TestrunTestCategoryType**](TestrunTestCategoryType.md) |  | [optional] 
**artifact_identifier** | [**MonitorArtifactIdentifier**](MonitorArtifactIdentifier.md) |  | [optional] 
**created_time** | **datetime** | The time at which the monitor was created. | [optional] 
**notify** | **bool** | This field indicates whether the system should send CT monitoring notifications when this monitor is triggered. For default monitors, after the RIME engine creates a Monitor, this field should only be modified directly by the user. i.e. when we upsert the monitor in the Result synthesizer, we must not overwrite the value configured by the user. | [optional] 
**config** | [**SchemamonitorConfig**](SchemamonitorConfig.md) |  | [optional] 
**excluded_transforms** | [**MonitorExcludedTransforms**](MonitorExcludedTransforms.md) |  | [optional] 
**pinned** | **bool** | Option to pin a monitor. Pinned monitors are pinned for all users visiting the monitor&#39;s project. | [optional] 

## Example

```python
from ri.apiclient.models.monitor_monitor import MonitorMonitor

# TODO update the JSON string below
json = "{}"
# create an instance of MonitorMonitor from a JSON string
monitor_monitor_instance = MonitorMonitor.from_json(json)
# print the JSON string representation of the object
print(MonitorMonitor.to_json())

# convert the object into a dict
monitor_monitor_dict = monitor_monitor_instance.to_dict()
# create an instance of MonitorMonitor from a dict
monitor_monitor_from_dict = MonitorMonitor.from_dict(monitor_monitor_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

