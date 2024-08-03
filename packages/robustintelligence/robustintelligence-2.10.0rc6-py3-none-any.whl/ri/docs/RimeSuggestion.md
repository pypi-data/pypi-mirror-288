# RimeSuggestion


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**details** | **bytearray** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_suggestion import RimeSuggestion

# TODO update the JSON string below
json = "{}"
# create an instance of RimeSuggestion from a JSON string
rime_suggestion_instance = RimeSuggestion.from_json(json)
# print the JSON string representation of the object
print(RimeSuggestion.to_json())

# convert the object into a dict
rime_suggestion_dict = rime_suggestion_instance.to_dict()
# create an instance of RimeSuggestion from a dict
rime_suggestion_from_dict = RimeSuggestion.from_dict(rime_suggestion_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

