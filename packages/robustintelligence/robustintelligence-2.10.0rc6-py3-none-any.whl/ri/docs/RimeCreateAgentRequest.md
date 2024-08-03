# RimeCreateAgentRequest

CreateAgentRequest is the request for creating an agent.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Agent name given by the user. | [optional] 
**local_config** | **object** | Configuration for local machine. | [optional] 
**aws_config** | [**CreateAgentRequestAWSConfig**](CreateAgentRequestAWSConfig.md) |  | [optional] 
**gcp_config** | [**CreateAgentRequestGCPConfig**](CreateAgentRequestGCPConfig.md) |  | [optional] 
**azure_config** | [**CreateAgentRequestAzureConfig**](CreateAgentRequestAzureConfig.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_agent_request import RimeCreateAgentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateAgentRequest from a JSON string
rime_create_agent_request_instance = RimeCreateAgentRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateAgentRequest.to_json())

# convert the object into a dict
rime_create_agent_request_dict = rime_create_agent_request_instance.to_dict()
# create an instance of RimeCreateAgentRequest from a dict
rime_create_agent_request_from_dict = RimeCreateAgentRequest.from_dict(rime_create_agent_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

