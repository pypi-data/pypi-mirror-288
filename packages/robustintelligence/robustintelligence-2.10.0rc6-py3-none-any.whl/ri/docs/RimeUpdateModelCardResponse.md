# RimeUpdateModelCardResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_card** | [**RimeModelCard**](RimeModelCard.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_update_model_card_response import RimeUpdateModelCardResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUpdateModelCardResponse from a JSON string
rime_update_model_card_response_instance = RimeUpdateModelCardResponse.from_json(json)
# print the JSON string representation of the object
print(RimeUpdateModelCardResponse.to_json())

# convert the object into a dict
rime_update_model_card_response_dict = rime_update_model_card_response_instance.to_dict()
# create an instance of RimeUpdateModelCardResponse from a dict
rime_update_model_card_response_from_dict = RimeUpdateModelCardResponse.from_dict(rime_update_model_card_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

