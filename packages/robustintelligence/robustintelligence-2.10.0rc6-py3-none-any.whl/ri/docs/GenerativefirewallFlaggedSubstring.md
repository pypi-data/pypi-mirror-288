# GenerativefirewallFlaggedSubstring


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_body_component** | [**FlaggedSubstringRequestBodyComponent**](FlaggedSubstringRequestBodyComponent.md) |  | [optional] 
**context_index** | **str** | Context index denotes which of the texts in the contexts provided in the validate request contains the substring. | [optional] 
**substring_start_index** | **str** |  | [optional] 
**substring_end_index** | **str** |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_flagged_substring import GenerativefirewallFlaggedSubstring

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallFlaggedSubstring from a JSON string
generativefirewall_flagged_substring_instance = GenerativefirewallFlaggedSubstring.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallFlaggedSubstring.to_json())

# convert the object into a dict
generativefirewall_flagged_substring_dict = generativefirewall_flagged_substring_instance.to_dict()
# create an instance of GenerativefirewallFlaggedSubstring from a dict
generativefirewall_flagged_substring_from_dict = GenerativefirewallFlaggedSubstring.from_dict(generativefirewall_flagged_substring_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

