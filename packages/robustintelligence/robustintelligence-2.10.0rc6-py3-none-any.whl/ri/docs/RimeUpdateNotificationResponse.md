# RimeUpdateNotificationResponse

UpdateNotificationResponse is returned after a successful update.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**notification** | [**NotificationNotification**](NotificationNotification.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_update_notification_response import RimeUpdateNotificationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUpdateNotificationResponse from a JSON string
rime_update_notification_response_instance = RimeUpdateNotificationResponse.from_json(json)
# print the JSON string representation of the object
print(RimeUpdateNotificationResponse.to_json())

# convert the object into a dict
rime_update_notification_response_dict = rime_update_notification_response_instance.to_dict()
# create an instance of RimeUpdateNotificationResponse from a dict
rime_update_notification_response_from_dict = RimeUpdateNotificationResponse.from_dict(rime_update_notification_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

