# RimeStorePredictionsRequestPrediction


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**datapoint_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**prediction** | **bytearray** | A JSON-encoded prediction dictionary. | 

## Example

```python
from ri.apiclient.models.rime_store_predictions_request_prediction import RimeStorePredictionsRequestPrediction

# TODO update the JSON string below
json = "{}"
# create an instance of RimeStorePredictionsRequestPrediction from a JSON string
rime_store_predictions_request_prediction_instance = RimeStorePredictionsRequestPrediction.from_json(json)
# print the JSON string representation of the object
print(RimeStorePredictionsRequestPrediction.to_json())

# convert the object into a dict
rime_store_predictions_request_prediction_dict = rime_store_predictions_request_prediction_instance.to_dict()
# create an instance of RimeStorePredictionsRequestPrediction from a dict
rime_store_predictions_request_prediction_from_dict = RimeStorePredictionsRequestPrediction.from_dict(rime_store_predictions_request_prediction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

