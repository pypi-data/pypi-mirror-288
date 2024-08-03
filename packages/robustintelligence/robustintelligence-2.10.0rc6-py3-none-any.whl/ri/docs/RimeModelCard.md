# RimeModelCard


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_card_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**details** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_model_card import RimeModelCard

# TODO update the JSON string below
json = "{}"
# create an instance of RimeModelCard from a JSON string
rime_model_card_instance = RimeModelCard.from_json(json)
# print the JSON string representation of the object
print(RimeModelCard.to_json())

# convert the object into a dict
rime_model_card_dict = rime_model_card_instance.to_dict()
# create an instance of RimeModelCard from a dict
rime_model_card_from_dict = RimeModelCard.from_dict(rime_model_card_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

