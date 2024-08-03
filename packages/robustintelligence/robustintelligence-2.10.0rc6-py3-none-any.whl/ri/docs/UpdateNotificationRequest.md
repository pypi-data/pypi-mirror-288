# UpdateNotificationRequest

UpdateNotificationRequest is a request for updating a single notification in the backend. Only the fields specified in the mask will be used by the backend. Note: the ID field is necessary to find the given notification setting.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**notification** | [**UpdateNotificationRequestNotification**](UpdateNotificationRequestNotification.md) |  | [optional] 
**mask** | **str** | Mask for determining which fields of the notification setting should be written in the Update. Specify a mask as a &#x60;.&#x60; separated path of field names e.g. &#x60;foo.bar&#x60; for nested field &#x60;bar&#x60; in submessage &#x60;foo&#x60;. Note: some fields are marked immutable and cannot be changed. | [optional] 

## Example

```python
from ri.apiclient.models.update_notification_request import UpdateNotificationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateNotificationRequest from a JSON string
update_notification_request_instance = UpdateNotificationRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateNotificationRequest.to_json())

# convert the object into a dict
update_notification_request_dict = update_notification_request_instance.to_dict()
# create an instance of UpdateNotificationRequest from a dict
update_notification_request_from_dict = UpdateNotificationRequest.from_dict(update_notification_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

