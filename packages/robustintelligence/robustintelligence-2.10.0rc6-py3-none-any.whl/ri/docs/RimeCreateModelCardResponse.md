# RimeCreateModelCardResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_card_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_model_card_response import RimeCreateModelCardResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateModelCardResponse from a JSON string
rime_create_model_card_response_instance = RimeCreateModelCardResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateModelCardResponse.to_json())

# convert the object into a dict
rime_create_model_card_response_dict = rime_create_model_card_response_instance.to_dict()
# create an instance of RimeCreateModelCardResponse from a dict
rime_create_model_card_response_from_dict = RimeCreateModelCardResponse.from_dict(rime_create_model_card_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

