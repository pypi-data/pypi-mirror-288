# RimeCreateModelCardRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_card** | [**RimeModelCard**](RimeModelCard.md) |  | [optional] 
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_model_card_request import RimeCreateModelCardRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateModelCardRequest from a JSON string
rime_create_model_card_request_instance = RimeCreateModelCardRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateModelCardRequest.to_json())

# convert the object into a dict
rime_create_model_card_request_dict = rime_create_model_card_request_instance.to_dict()
# create an instance of RimeCreateModelCardRequest from a dict
rime_create_model_card_request_from_dict = RimeCreateModelCardRequest.from_dict(rime_create_model_card_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

