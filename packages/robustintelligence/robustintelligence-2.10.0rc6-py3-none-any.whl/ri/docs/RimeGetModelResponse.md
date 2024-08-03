# RimeGetModelResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | [**RimeModelWithOwnerDetails**](RimeModelWithOwnerDetails.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_model_response import RimeGetModelResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetModelResponse from a JSON string
rime_get_model_response_instance = RimeGetModelResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetModelResponse.to_json())

# convert the object into a dict
rime_get_model_response_dict = rime_get_model_response_instance.to_dict()
# create an instance of RimeGetModelResponse from a dict
rime_get_model_response_from_dict = RimeGetModelResponse.from_dict(rime_get_model_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

