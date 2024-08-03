# RimeCreateUserRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | The email address of the user. | 
**password** | **str** | The password of the user. This password will be changed on the first login. | 
**full_name** | **str** | The full name of the user. | 
**org_role** | [**RimeActorRole**](RimeActorRole.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_user_request import RimeCreateUserRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateUserRequest from a JSON string
rime_create_user_request_instance = RimeCreateUserRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateUserRequest.to_json())

# convert the object into a dict
rime_create_user_request_dict = rime_create_user_request_instance.to_dict()
# create an instance of RimeCreateUserRequest from a dict
rime_create_user_request_from_dict = RimeCreateUserRequest.from_dict(rime_create_user_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

