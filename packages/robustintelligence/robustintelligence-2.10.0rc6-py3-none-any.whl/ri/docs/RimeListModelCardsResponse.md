# RimeListModelCardsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_card_map** | [**Dict[str, RimeModelCard]**](RimeModelCard.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_model_cards_response import RimeListModelCardsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListModelCardsResponse from a JSON string
rime_list_model_cards_response_instance = RimeListModelCardsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListModelCardsResponse.to_json())

# convert the object into a dict
rime_list_model_cards_response_dict = rime_list_model_cards_response_instance.to_dict()
# create an instance of RimeListModelCardsResponse from a dict
rime_list_model_cards_response_from_dict = RimeListModelCardsResponse.from_dict(rime_list_model_cards_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

