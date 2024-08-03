# UpdateModelCardRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_card** | [**UpdateModelCardRequestModelCard**](UpdateModelCardRequestModelCard.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.update_model_card_request import UpdateModelCardRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateModelCardRequest from a JSON string
update_model_card_request_instance = UpdateModelCardRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateModelCardRequest.to_json())

# convert the object into a dict
update_model_card_request_dict = update_model_card_request_instance.to_dict()
# create an instance of UpdateModelCardRequest from a dict
update_model_card_request_from_dict = UpdateModelCardRequest.from_dict(update_model_card_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

