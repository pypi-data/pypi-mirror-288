# RimeListProjectTagsInWorkspaceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**tags** | **List[str]** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_project_tags_in_workspace_response import RimeListProjectTagsInWorkspaceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListProjectTagsInWorkspaceResponse from a JSON string
rime_list_project_tags_in_workspace_response_instance = RimeListProjectTagsInWorkspaceResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListProjectTagsInWorkspaceResponse.to_json())

# convert the object into a dict
rime_list_project_tags_in_workspace_response_dict = rime_list_project_tags_in_workspace_response_instance.to_dict()
# create an instance of RimeListProjectTagsInWorkspaceResponse from a dict
rime_list_project_tags_in_workspace_response_from_dict = RimeListProjectTagsInWorkspaceResponse.from_dict(rime_list_project_tags_in_workspace_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

