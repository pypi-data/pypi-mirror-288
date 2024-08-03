# RimeAgentDesiredState


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **str** | Desired agent release version. E.g., 2.7.1 This is always set to the current control plane version. | [optional] 
**custom_values** | **Dict[str, str]** | Example:   {     \&quot;rimeAgent.images.agentImage.registry\&quot;: \&quot;docker.io\&quot;,   } | [optional] 
**upgrade_status** | [**RimeDetailedUpgradeStatus**](RimeDetailedUpgradeStatus.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_agent_desired_state import RimeAgentDesiredState

# TODO update the JSON string below
json = "{}"
# create an instance of RimeAgentDesiredState from a JSON string
rime_agent_desired_state_instance = RimeAgentDesiredState.from_json(json)
# print the JSON string representation of the object
print(RimeAgentDesiredState.to_json())

# convert the object into a dict
rime_agent_desired_state_dict = rime_agent_desired_state_instance.to_dict()
# create an instance of RimeAgentDesiredState from a dict
rime_agent_desired_state_from_dict = RimeAgentDesiredState.from_dict(rime_agent_desired_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

