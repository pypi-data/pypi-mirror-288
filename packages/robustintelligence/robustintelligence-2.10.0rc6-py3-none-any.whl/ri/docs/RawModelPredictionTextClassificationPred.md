# RawModelPredictionTextClassificationPred


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scores** | **List[float]** | Vector of scores, sorted by class index. | [optional] 

## Example

```python
from ri.fwclient.models.raw_model_prediction_text_classification_pred import RawModelPredictionTextClassificationPred

# TODO update the JSON string below
json = "{}"
# create an instance of RawModelPredictionTextClassificationPred from a JSON string
raw_model_prediction_text_classification_pred_instance = RawModelPredictionTextClassificationPred.from_json(json)
# print the JSON string representation of the object
print(RawModelPredictionTextClassificationPred.to_json())

# convert the object into a dict
raw_model_prediction_text_classification_pred_dict = raw_model_prediction_text_classification_pred_instance.to_dict()
# create an instance of RawModelPredictionTextClassificationPred from a dict
raw_model_prediction_text_classification_pred_from_dict = RawModelPredictionTextClassificationPred.from_dict(raw_model_prediction_text_classification_pred_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

