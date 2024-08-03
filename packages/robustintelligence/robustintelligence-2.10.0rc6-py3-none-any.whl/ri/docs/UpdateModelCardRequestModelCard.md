# UpdateModelCardRequestModelCard


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_card_id** | **object** |  | [optional] 
**details** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.update_model_card_request_model_card import UpdateModelCardRequestModelCard

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateModelCardRequestModelCard from a JSON string
update_model_card_request_model_card_instance = UpdateModelCardRequestModelCard.from_json(json)
# print the JSON string representation of the object
print(UpdateModelCardRequestModelCard.to_json())

# convert the object into a dict
update_model_card_request_model_card_dict = update_model_card_request_model_card_instance.to_dict()
# create an instance of UpdateModelCardRequestModelCard from a dict
update_model_card_request_model_card_from_dict = UpdateModelCardRequestModelCard.from_dict(update_model_card_request_model_card_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

