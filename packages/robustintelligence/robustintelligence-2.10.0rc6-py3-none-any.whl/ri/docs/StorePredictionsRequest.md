# StorePredictionsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_id** | **object** | Uniquely specifies a Model. | [optional] 
**predictions** | [**List[RimeStorePredictionsRequestPrediction]**](RimeStorePredictionsRequestPrediction.md) |  | 

## Example

```python
from ri.apiclient.models.store_predictions_request import StorePredictionsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of StorePredictionsRequest from a JSON string
store_predictions_request_instance = StorePredictionsRequest.from_json(json)
# print the JSON string representation of the object
print(StorePredictionsRequest.to_json())

# convert the object into a dict
store_predictions_request_dict = store_predictions_request_instance.to_dict()
# create an instance of StorePredictionsRequest from a dict
store_predictions_request_from_dict = StorePredictionsRequest.from_dict(store_predictions_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

