# GenerativefirewallRuleOutput

RuleOutput represents a single output from a firewall rule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rule_name** | **str** |  | [optional] 
**action** | [**GenerativefirewallFirewallAction**](GenerativefirewallFirewallAction.md) |  | [optional] 
**risk_category** | [**RiskscoreRiskCategoryType**](RiskscoreRiskCategoryType.md) |  | [optional] 
**pii_detection_details** | [**GenerativefirewallPiiDetectionDetails**](GenerativefirewallPiiDetectionDetails.md) |  | [optional] 
**language_detection_details** | [**GenerativefirewallLanguageDetectionDetails**](GenerativefirewallLanguageDetectionDetails.md) |  | [optional] 
**prompt_injection_details** | [**GenerativefirewallPromptInjectionDetails**](GenerativefirewallPromptInjectionDetails.md) |  | [optional] 
**toxicity_detection_details** | [**GenerativefirewallToxicityDetectionDetails**](GenerativefirewallToxicityDetectionDetails.md) |  | [optional] 
**code_detection_details** | [**GenerativefirewallCodeDetectionDetails**](GenerativefirewallCodeDetectionDetails.md) |  | [optional] 
**rule_eval_metadata** | [**RuleOutputRuleEvaluationMetadata**](RuleOutputRuleEvaluationMetadata.md) |  | [optional] 
**security_standards** | [**List[GenerativefirewallStandardInfo]**](GenerativefirewallStandardInfo.md) | Standards encodes which regulatory standards (MITRE, OWASP) are addressed by this firewall rule. | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_rule_output import GenerativefirewallRuleOutput

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallRuleOutput from a JSON string
generativefirewall_rule_output_instance = GenerativefirewallRuleOutput.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallRuleOutput.to_json())

# convert the object into a dict
generativefirewall_rule_output_dict = generativefirewall_rule_output_instance.to_dict()
# create an instance of GenerativefirewallRuleOutput from a dict
generativefirewall_rule_output_from_dict = GenerativefirewallRuleOutput.from_dict(generativefirewall_rule_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

