# RimeGetUserResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user** | [**UserUserDetail**](UserUserDetail.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_user_response import RimeGetUserResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetUserResponse from a JSON string
rime_get_user_response_instance = RimeGetUserResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetUserResponse.to_json())

# convert the object into a dict
rime_get_user_response_dict = rime_get_user_response_instance.to_dict()
# create an instance of RimeGetUserResponse from a dict
rime_get_user_response_from_dict = RimeGetUserResponse.from_dict(rime_get_user_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

