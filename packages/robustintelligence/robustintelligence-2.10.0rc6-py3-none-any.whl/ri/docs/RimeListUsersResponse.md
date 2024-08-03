# RimeListUsersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**users** | [**List[UserUserDetail]**](UserUserDetail.md) |  | [optional] 
**next_page_token** | **str** |  | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_users_response import RimeListUsersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListUsersResponse from a JSON string
rime_list_users_response_instance = RimeListUsersResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListUsersResponse.to_json())

# convert the object into a dict
rime_list_users_response_dict = rime_list_users_response_instance.to_dict()
# create an instance of RimeListUsersResponse from a dict
rime_list_users_response_from_dict = RimeListUsersResponse.from_dict(rime_list_users_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

