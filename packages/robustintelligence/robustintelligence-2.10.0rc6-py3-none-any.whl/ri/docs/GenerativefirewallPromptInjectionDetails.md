# GenerativefirewallPromptInjectionDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**objectives** | [**List[RimeAttackObjective]**](RimeAttackObjective.md) | Objectives represent the attack objectives found in the text, such as privacy or abuse violations. | [optional] 
**techniques** | [**List[RimeAttackTechnique]**](RimeAttackTechnique.md) | Attack Techniques represent the technique used in a prompt injection for example: unicode obfuscation, base64 etc. These values may change between versions. | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_prompt_injection_details import GenerativefirewallPromptInjectionDetails

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallPromptInjectionDetails from a JSON string
generativefirewall_prompt_injection_details_instance = GenerativefirewallPromptInjectionDetails.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallPromptInjectionDetails.to_json())

# convert the object into a dict
generativefirewall_prompt_injection_details_dict = generativefirewall_prompt_injection_details_instance.to_dict()
# create an instance of GenerativefirewallPromptInjectionDetails from a dict
generativefirewall_prompt_injection_details_from_dict = GenerativefirewallPromptInjectionDetails.from_dict(generativefirewall_prompt_injection_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

