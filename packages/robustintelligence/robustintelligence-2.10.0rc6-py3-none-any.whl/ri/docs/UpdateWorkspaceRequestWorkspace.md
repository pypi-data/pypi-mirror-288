# UpdateWorkspaceRequestWorkspace


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the Workspace. | [optional] 
**agent_ids** | [**List[RimeUUID]**](RimeUUID.md) | List of Agent IDs that can be used by the Workspace. | [optional] 
**default_agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**workspace_id** | **object** | Unique ID of an object in RIME. | [optional] 
**description** | **str** | Description of the Workspace. | [optional] 
**results_retention_in_days** | **int** |  | [optional] 

## Example

```python
from ri.apiclient.models.update_workspace_request_workspace import UpdateWorkspaceRequestWorkspace

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateWorkspaceRequestWorkspace from a JSON string
update_workspace_request_workspace_instance = UpdateWorkspaceRequestWorkspace.from_json(json)
# print the JSON string representation of the object
print(UpdateWorkspaceRequestWorkspace.to_json())

# convert the object into a dict
update_workspace_request_workspace_dict = update_workspace_request_workspace_instance.to_dict()
# create an instance of UpdateWorkspaceRequestWorkspace from a dict
update_workspace_request_workspace_from_dict = UpdateWorkspaceRequestWorkspace.from_dict(update_workspace_request_workspace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

