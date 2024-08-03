# GenerativefirewallValidateResponse

ValidateResponse is the response to a single validation request. Note: this does not follow the same RI API standards, because we want this to be easily consumed by security team's event frameworks.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**input_results** | [**Dict[str, GenerativefirewallRuleOutput]**](GenerativefirewallRuleOutput.md) | Results of the firewall for user input. The key is a rule name. | [optional] 
**output_results** | [**Dict[str, GenerativefirewallRuleOutput]**](GenerativefirewallRuleOutput.md) | Results of the firewall for model output. The key is a rule name. | [optional] 
**metadata** | [**ValidateResponseProductMetadata**](ValidateResponseProductMetadata.md) |  | [optional] 
**processed_req** | [**ValidateResponseProcessedRequest**](ValidateResponseProcessedRequest.md) |  | [optional] 
**api_schema_version** | **str** | API schema version is the version of the API response. This should be updated whenever we make semantic changes to the response. | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_validate_response import GenerativefirewallValidateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallValidateResponse from a JSON string
generativefirewall_validate_response_instance = GenerativefirewallValidateResponse.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallValidateResponse.to_json())

# convert the object into a dict
generativefirewall_validate_response_dict = generativefirewall_validate_response_instance.to_dict()
# create an instance of GenerativefirewallValidateResponse from a dict
generativefirewall_validate_response_from_dict = GenerativefirewallValidateResponse.from_dict(generativefirewall_validate_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

