# SchemadatacollectorPrediction

Prediction contains the prediction of a model for a datapoint.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**datapoint_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**model_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**data_stream_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**prediction** | **bytearray** |  | [optional] 
**timestamp** | **datetime** | The timestamp of the datapoint is stored in the prediction for fast querying. | [optional] 

## Example

```python
from ri.apiclient.models.schemadatacollector_prediction import SchemadatacollectorPrediction

# TODO update the JSON string below
json = "{}"
# create an instance of SchemadatacollectorPrediction from a JSON string
schemadatacollector_prediction_instance = SchemadatacollectorPrediction.from_json(json)
# print the JSON string representation of the object
print(SchemadatacollectorPrediction.to_json())

# convert the object into a dict
schemadatacollector_prediction_dict = schemadatacollector_prediction_instance.to_dict()
# create an instance of SchemadatacollectorPrediction from a dict
schemadatacollector_prediction_from_dict = SchemadatacollectorPrediction.from_dict(schemadatacollector_prediction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

