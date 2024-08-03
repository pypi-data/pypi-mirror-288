# GenerativefirewallCustomPiiEntity


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the entity type. | [optional] 
**patterns** | **List[str]** | The regex patterns to match against for this entity. | [optional] 
**context_words** | **List[str]** | Words to use as context that will boost the score if detected around the matching entity. These words are case-insensitive. | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_custom_pii_entity import GenerativefirewallCustomPiiEntity

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallCustomPiiEntity from a JSON string
generativefirewall_custom_pii_entity_instance = GenerativefirewallCustomPiiEntity.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallCustomPiiEntity.to_json())

# convert the object into a dict
generativefirewall_custom_pii_entity_dict = generativefirewall_custom_pii_entity_instance.to_dict()
# create an instance of GenerativefirewallCustomPiiEntity from a dict
generativefirewall_custom_pii_entity_from_dict = GenerativefirewallCustomPiiEntity.from_dict(generativefirewall_custom_pii_entity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

