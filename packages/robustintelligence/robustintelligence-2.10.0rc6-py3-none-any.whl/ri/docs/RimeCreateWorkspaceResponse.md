# RimeCreateWorkspaceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_workspace_response import RimeCreateWorkspaceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateWorkspaceResponse from a JSON string
rime_create_workspace_response_instance = RimeCreateWorkspaceResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateWorkspaceResponse.to_json())

# convert the object into a dict
rime_create_workspace_response_dict = rime_create_workspace_response_instance.to_dict()
# create an instance of RimeCreateWorkspaceResponse from a dict
rime_create_workspace_response_from_dict = RimeCreateWorkspaceResponse.from_dict(rime_create_workspace_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

