# CreateAgentRequestAzureConfig

Configuration for Azure.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**azure_client_id** | **str** | Azure workload Identity Client ID. | [optional] 
**azure_tenant_id** | **str** | Azure workload Identity Tenant ID. | [optional] 

## Example

```python
from ri.apiclient.models.create_agent_request_azure_config import CreateAgentRequestAzureConfig

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAgentRequestAzureConfig from a JSON string
create_agent_request_azure_config_instance = CreateAgentRequestAzureConfig.from_json(json)
# print the JSON string representation of the object
print(CreateAgentRequestAzureConfig.to_json())

# convert the object into a dict
create_agent_request_azure_config_dict = create_agent_request_azure_config_instance.to_dict()
# create an instance of CreateAgentRequestAzureConfig from a dict
create_agent_request_azure_config_from_dict = CreateAgentRequestAzureConfig.from_dict(create_agent_request_azure_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

