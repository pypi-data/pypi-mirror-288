# NotificationMonitoringConfig

MonitoringConfig is a configuration for Continuous Testing notifications. These notifications are triggered when certain Monitors detect abnormalities. For instance, if a model performance Monitor fails, the system will send a notification after the job completes. Turn on and off notifications for Monitors in the web application or the SDK. Only a subset of Monitors will have notifications on by default.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**level** | [**MonitoringConfigAlertLevel**](MonitoringConfigAlertLevel.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.notification_monitoring_config import NotificationMonitoringConfig

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationMonitoringConfig from a JSON string
notification_monitoring_config_instance = NotificationMonitoringConfig.from_json(json)
# print the JSON string representation of the object
print(NotificationMonitoringConfig.to_json())

# convert the object into a dict
notification_monitoring_config_dict = notification_monitoring_config_instance.to_dict()
# create an instance of NotificationMonitoringConfig from a dict
notification_monitoring_config_from_dict = NotificationMonitoringConfig.from_dict(notification_monitoring_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

