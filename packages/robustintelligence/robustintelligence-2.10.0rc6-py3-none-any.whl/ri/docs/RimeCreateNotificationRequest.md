# RimeCreateNotificationRequest

CreateNotificationRequest is a request for creating a new notification setting in the backend.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object_type** | [**NotificationObjectType**](NotificationObjectType.md) |  | [optional] 
**object_id** | **str** | Uniquely specifies an object for the notification. This varies depending on the object type; for Projects, this should be the unique identifier of the project. | 
**emails** | **List[str]** | List of emails that notifications should be sent to - this can be empty. | [optional] 
**config** | [**SchemanotificationConfig**](SchemanotificationConfig.md) |  | [optional] 
**webhooks** | [**List[NotificationWebhookConfig]**](NotificationWebhookConfig.md) | List of webhooks that notifications should be sent to - this can be empty. | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_notification_request import RimeCreateNotificationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateNotificationRequest from a JSON string
rime_create_notification_request_instance = RimeCreateNotificationRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateNotificationRequest.to_json())

# convert the object into a dict
rime_create_notification_request_dict = rime_create_notification_request_instance.to_dict()
# create an instance of RimeCreateNotificationRequest from a dict
rime_create_notification_request_from_dict = RimeCreateNotificationRequest.from_dict(rime_create_notification_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

