# RimeWorkspaceWriteMask

Mask used to specify fields of Workspace for updates.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **bool** | Specifies whether to update name. | [optional] 
**agent_ids** | **bool** | Specifies whether to update list of Agent IDs. | [optional] 
**default_agent_id** | **bool** | Specifies whether to update default Agent ID. | [optional] 
**description** | **bool** | Specifies whether to update description. | [optional] 
**results_retention_in_days** | **bool** | Specifies whether to results retention in days. | [optional] 

## Example

```python
from ri.apiclient.models.rime_workspace_write_mask import RimeWorkspaceWriteMask

# TODO update the JSON string below
json = "{}"
# create an instance of RimeWorkspaceWriteMask from a JSON string
rime_workspace_write_mask_instance = RimeWorkspaceWriteMask.from_json(json)
# print the JSON string representation of the object
print(RimeWorkspaceWriteMask.to_json())

# convert the object into a dict
rime_workspace_write_mask_dict = rime_workspace_write_mask_instance.to_dict()
# create an instance of RimeWorkspaceWriteMask from a dict
rime_workspace_write_mask_from_dict = RimeWorkspaceWriteMask.from_dict(rime_workspace_write_mask_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

