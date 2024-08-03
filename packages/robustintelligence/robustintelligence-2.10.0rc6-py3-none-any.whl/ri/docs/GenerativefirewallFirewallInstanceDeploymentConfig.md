# GenerativefirewallFirewallInstanceDeploymentConfig

Configuration for the deployment spec of a Firewall Instance. The Pod Annotations are validated as valid k8s annotations. They cannot override pre-existing deployment annotations.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pod_annotations** | **Dict[str, str]** |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_firewall_instance_deployment_config import GenerativefirewallFirewallInstanceDeploymentConfig

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallFirewallInstanceDeploymentConfig from a JSON string
generativefirewall_firewall_instance_deployment_config_instance = GenerativefirewallFirewallInstanceDeploymentConfig.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallFirewallInstanceDeploymentConfig.to_json())

# convert the object into a dict
generativefirewall_firewall_instance_deployment_config_dict = generativefirewall_firewall_instance_deployment_config_instance.to_dict()
# create an instance of GenerativefirewallFirewallInstanceDeploymentConfig from a dict
generativefirewall_firewall_instance_deployment_config_from_dict = GenerativefirewallFirewallInstanceDeploymentConfig.from_dict(generativefirewall_firewall_instance_deployment_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

