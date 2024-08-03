# RimeCreateNotificationResponse

CreateNotificationResponse is the response from creating a notification.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_notification_response import RimeCreateNotificationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateNotificationResponse from a JSON string
rime_create_notification_response_instance = RimeCreateNotificationResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateNotificationResponse.to_json())

# convert the object into a dict
rime_create_notification_response_dict = rime_create_notification_response_instance.to_dict()
# create an instance of RimeCreateNotificationResponse from a dict
rime_create_notification_response_from_dict = RimeCreateNotificationResponse.from_dict(rime_create_notification_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

