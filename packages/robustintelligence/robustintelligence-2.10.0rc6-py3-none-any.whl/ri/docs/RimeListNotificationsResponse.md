# RimeListNotificationsResponse

ListNotificationsResponse is a single page of notification settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**notifications** | [**List[NotificationNotification]**](NotificationNotification.md) | List of individual notification objects requested from the backend. | [optional] 
**next_page_token** | **str** | The page token to use in the next ListNotifications call. | [optional] 
**has_more** | **bool** | Whether or not there are more notification settings in the DB. | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_notifications_response import RimeListNotificationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListNotificationsResponse from a JSON string
rime_list_notifications_response_instance = RimeListNotificationsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListNotificationsResponse.to_json())

# convert the object into a dict
rime_list_notifications_response_dict = rime_list_notifications_response_instance.to_dict()
# create an instance of RimeListNotificationsResponse from a dict
rime_list_notifications_response_from_dict = RimeListNotificationsResponse.from_dict(rime_list_notifications_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

