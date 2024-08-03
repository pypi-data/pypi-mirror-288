# CreateAgentRequestAWSConfig

Configuration for AWS.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aws_role_arn** | **str** | AWS ARN of the the role to be attached to the service account of the model test jobs. | [optional] 

## Example

```python
from ri.apiclient.models.create_agent_request_aws_config import CreateAgentRequestAWSConfig

# TODO update the JSON string below
json = "{}"
# create an instance of CreateAgentRequestAWSConfig from a JSON string
create_agent_request_aws_config_instance = CreateAgentRequestAWSConfig.from_json(json)
# print the JSON string representation of the object
print(CreateAgentRequestAWSConfig.to_json())

# convert the object into a dict
create_agent_request_aws_config_dict = create_agent_request_aws_config_instance.to_dict()
# create an instance of CreateAgentRequestAWSConfig from a dict
create_agent_request_aws_config_from_dict = CreateAgentRequestAWSConfig.from_dict(create_agent_request_aws_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

