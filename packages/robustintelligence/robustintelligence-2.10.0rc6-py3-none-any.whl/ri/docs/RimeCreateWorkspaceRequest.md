# RimeCreateWorkspaceRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the Workspace. | 
**agent_ids** | [**List[RimeUUID]**](RimeUUID.md) | List of Agent IDs to be added to the Workspace. | [optional] 
**default_agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**description** | **str** | Description of the Workspace. | [optional] 
**results_retention_in_days** | **int** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_workspace_request import RimeCreateWorkspaceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateWorkspaceRequest from a JSON string
rime_create_workspace_request_instance = RimeCreateWorkspaceRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateWorkspaceRequest.to_json())

# convert the object into a dict
rime_create_workspace_request_dict = rime_create_workspace_request_instance.to_dict()
# create an instance of RimeCreateWorkspaceRequest from a dict
rime_create_workspace_request_from_dict = RimeCreateWorkspaceRequest.from_dict(rime_create_workspace_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

