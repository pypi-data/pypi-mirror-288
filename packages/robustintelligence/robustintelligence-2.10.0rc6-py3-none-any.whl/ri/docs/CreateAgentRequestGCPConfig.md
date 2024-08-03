# CreateAgentRequestGCPConfig

Configuration for GCP.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**gcp_sa_email** | **str** | GCP service account email for the role to be attached to the service account of the model test jobs. | [optional] 

## Example

```python
from ri.apiclient.models.create_agent_request_gcp_config import CreateAgentRequestGCPConfig

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAgentRequestGCPConfig from a JSON string
create_agent_request_gcp_config_instance = CreateAgentRequestGCPConfig.from_json(json)
# print the JSON string representation of the object
print(CreateAgentRequestGCPConfig.to_json())

# convert the object into a dict
create_agent_request_gcp_config_dict = create_agent_request_gcp_config_instance.to_dict()
# create an instance of CreateAgentRequestGCPConfig from a dict
create_agent_request_gcp_config_from_dict = CreateAgentRequestGCPConfig.from_dict(create_agent_request_gcp_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

