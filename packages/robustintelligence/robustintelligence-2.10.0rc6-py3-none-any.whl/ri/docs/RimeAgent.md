# RimeAgent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**name** | **str** | The user specified name of the agent. | [optional] 
**creation_time** | **datetime** | The time of creation of the agent. | [optional] 
**status** | [**RimeAgentStatus**](RimeAgentStatus.md) |  | [optional] 
**internal** | **bool** | Specifies whether the agent is an internal agent. Internal agents come bundled with the deployment. | [optional] 
**last_heartbeat_time** | **datetime** | The time of the last heartbeat. | [optional] 
**version** | **str** | Agent version. | [optional] 
**desired_state** | [**RimeAgentDesiredState**](RimeAgentDesiredState.md) |  | [optional] 
**type** | [**RimeAgentType**](RimeAgentType.md) |  | [optional] 
**url** | **str** | The url of the agent. E.g., https://dev.my-firewall.rbst.io This is used for firewall agents, which can have a different URL than the control plane. | [optional] 

## Example

```python
from ri.apiclient.models.rime_agent import RimeAgent

# TODO update the JSON string below
json = "{}"
# create an instance of RimeAgent from a JSON string
rime_agent_instance = RimeAgent.from_json(json)
# print the JSON string representation of the object
print(RimeAgent.to_json())

# convert the object into a dict
rime_agent_dict = rime_agent_instance.to_dict()
# create an instance of RimeAgent from a dict
rime_agent_from_dict = RimeAgent.from_dict(rime_agent_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

