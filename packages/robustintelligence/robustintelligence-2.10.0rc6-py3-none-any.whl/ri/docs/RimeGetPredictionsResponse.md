# RimeGetPredictionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**predictions** | [**List[SchemadatacollectorPrediction]**](SchemadatacollectorPrediction.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_predictions_response import RimeGetPredictionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetPredictionsResponse from a JSON string
rime_get_predictions_response_instance = RimeGetPredictionsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetPredictionsResponse.to_json())

# convert the object into a dict
rime_get_predictions_response_dict = rime_get_predictions_response_instance.to_dict()
# create an instance of RimeGetPredictionsResponse from a dict
rime_get_predictions_response_from_dict = RimeGetPredictionsResponse.from_dict(rime_get_predictions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

