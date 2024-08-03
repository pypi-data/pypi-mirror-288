# UpdateNotificationRequestNotification

Notification represents a single notification setting in the backend. It includes the configuration for when notifications should be sent as well as the list of receivers (emails, webhooks, etc.).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **object** | Uniquely specifies a Notification. | [optional] 
**object_type** | [**NotificationObjectType**](NotificationObjectType.md) |  | [optional] 
**object_id** | **str** | Uniquely specifies the object for the notification. | [optional] 
**notification_type** | [**NotificationNotificationType**](NotificationNotificationType.md) |  | [optional] 
**config** | [**SchemanotificationConfig**](SchemanotificationConfig.md) |  | [optional] 
**webhooks** | [**List[NotificationWebhookConfig]**](NotificationWebhookConfig.md) | Webhooks are a list of destination webhooks to which notifications will be sent. | [optional] 
**emails** | **List[str]** | Emails specify the list of emails to which notifications will be sent. | [optional] 
**last_send_time** | **datetime** | Last send time is the last time the notification was successfully sent. | [optional] 

## Example

```python
from ri.apiclient.models.update_notification_request_notification import UpdateNotificationRequestNotification

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateNotificationRequestNotification from a JSON string
update_notification_request_notification_instance = UpdateNotificationRequestNotification.from_json(json)
# print the JSON string representation of the object
print(UpdateNotificationRequestNotification.to_json())

# convert the object into a dict
update_notification_request_notification_dict = update_notification_request_notification_instance.to_dict()
# create an instance of UpdateNotificationRequestNotification from a dict
update_notification_request_notification_from_dict = UpdateNotificationRequestNotification.from_dict(update_notification_request_notification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

