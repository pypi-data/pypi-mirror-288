# RimeCreateUserResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_user_response import RimeCreateUserResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateUserResponse from a JSON string
rime_create_user_response_instance = RimeCreateUserResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateUserResponse.to_json())

# convert the object into a dict
rime_create_user_response_dict = rime_create_user_response_instance.to_dict()
# create an instance of RimeCreateUserResponse from a dict
rime_create_user_response_from_dict = RimeCreateUserResponse.from_dict(rime_create_user_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

