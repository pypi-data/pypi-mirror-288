# RimeWorkspace


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the Workspace. | [optional] 
**agent_ids** | [**List[RimeUUID]**](RimeUUID.md) | List of Agent IDs that can be used by the Workspace. | [optional] 
**default_agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**description** | **str** | Description of the Workspace. | [optional] 
**results_retention_in_days** | **int** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_workspace import RimeWorkspace

# TODO update the JSON string below
json = "{}"
# create an instance of RimeWorkspace from a JSON string
rime_workspace_instance = RimeWorkspace.from_json(json)
# print the JSON string representation of the object
print(RimeWorkspace.to_json())

# convert the object into a dict
rime_workspace_dict = rime_workspace_instance.to_dict()
# create an instance of RimeWorkspace from a dict
rime_workspace_from_dict = RimeWorkspace.from_dict(rime_workspace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

