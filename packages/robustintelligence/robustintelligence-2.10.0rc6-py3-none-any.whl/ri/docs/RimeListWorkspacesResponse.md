# RimeListWorkspacesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspaces** | [**List[RimeWorkspace]**](RimeWorkspace.md) |  | [optional] 
**next_page_token** | **str** |  | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_workspaces_response import RimeListWorkspacesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListWorkspacesResponse from a JSON string
rime_list_workspaces_response_instance = RimeListWorkspacesResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListWorkspacesResponse.to_json())

# convert the object into a dict
rime_list_workspaces_response_dict = rime_list_workspaces_response_instance.to_dict()
# create an instance of RimeListWorkspacesResponse from a dict
rime_list_workspaces_response_from_dict = RimeListWorkspacesResponse.from_dict(rime_list_workspaces_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

