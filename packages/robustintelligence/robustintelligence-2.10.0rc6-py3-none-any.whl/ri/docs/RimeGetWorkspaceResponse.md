# RimeGetWorkspaceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace** | [**RimeWorkspace**](RimeWorkspace.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_workspace_response import RimeGetWorkspaceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetWorkspaceResponse from a JSON string
rime_get_workspace_response_instance = RimeGetWorkspaceResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetWorkspaceResponse.to_json())

# convert the object into a dict
rime_get_workspace_response_dict = rime_get_workspace_response_instance.to_dict()
# create an instance of RimeGetWorkspaceResponse from a dict
rime_get_workspace_response_from_dict = RimeGetWorkspaceResponse.from_dict(rime_get_workspace_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

