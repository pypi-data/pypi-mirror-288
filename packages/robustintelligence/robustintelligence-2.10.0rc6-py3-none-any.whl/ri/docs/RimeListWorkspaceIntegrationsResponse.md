# RimeListWorkspaceIntegrationsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**integration_infos** | [**List[RimeIntegrationInfo]**](RimeIntegrationInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_workspace_integrations_response import RimeListWorkspaceIntegrationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListWorkspaceIntegrationsResponse from a JSON string
rime_list_workspace_integrations_response_instance = RimeListWorkspaceIntegrationsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListWorkspaceIntegrationsResponse.to_json())

# convert the object into a dict
rime_list_workspace_integrations_response_dict = rime_list_workspace_integrations_response_instance.to_dict()
# create an instance of RimeListWorkspaceIntegrationsResponse from a dict
rime_list_workspace_integrations_response_from_dict = RimeListWorkspaceIntegrationsResponse.from_dict(rime_list_workspace_integrations_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

