# SchemanotificationConfig

Config is the configuration for a notification setting.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**digest_config** | [**NotificationDigestConfig**](NotificationDigestConfig.md) |  | [optional] 
**job_action_config** | **object** | JobActionConfig is a configuration for job action notifications. These notifications are helpful for tracking the status of jobs. | [optional] 
**monitoring_config** | [**NotificationMonitoringConfig**](NotificationMonitoringConfig.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.schemanotification_config import SchemanotificationConfig

# TODO update the JSON string below
json = "{}"
# create an instance of SchemanotificationConfig from a JSON string
schemanotification_config_instance = SchemanotificationConfig.from_json(json)
# print the JSON string representation of the object
print(SchemanotificationConfig.to_json())

# convert the object into a dict
schemanotification_config_dict = schemanotification_config_instance.to_dict()
# create an instance of SchemanotificationConfig from a dict
schemanotification_config_from_dict = SchemanotificationConfig.from_dict(schemanotification_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

