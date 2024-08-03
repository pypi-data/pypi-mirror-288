# NotificationWebhookConfig

Configuration for an individual webhook.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**webhook** | **str** | The URL of the destination webhook. It is not a strict requirement, but it is recommended that webhooks be preauthenticated by including a secure token in the URL. | [optional] 

## Example

```python
from ri.apiclient.models.notification_webhook_config import NotificationWebhookConfig

# TODO update the JSON string below
json = "{}"
# create an instance of NotificationWebhookConfig from a JSON string
notification_webhook_config_instance = NotificationWebhookConfig.from_json(json)
# print the JSON string representation of the object
print(NotificationWebhookConfig.to_json())

# convert the object into a dict
notification_webhook_config_dict = notification_webhook_config_instance.to_dict()
# create an instance of NotificationWebhookConfig from a dict
notification_webhook_config_from_dict = NotificationWebhookConfig.from_dict(notification_webhook_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

