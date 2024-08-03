# RimeGetPredictionSetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prediction** | [**RegistrypredictionPrediction**](RegistrypredictionPrediction.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_prediction_set_response import RimeGetPredictionSetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetPredictionSetResponse from a JSON string
rime_get_prediction_set_response_instance = RimeGetPredictionSetResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetPredictionSetResponse.to_json())

# convert the object into a dict
rime_get_prediction_set_response_dict = rime_get_prediction_set_response_instance.to_dict()
# create an instance of RimeGetPredictionSetResponse from a dict
rime_get_prediction_set_response_from_dict = RimeGetPredictionSetResponse.from_dict(rime_get_prediction_set_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

