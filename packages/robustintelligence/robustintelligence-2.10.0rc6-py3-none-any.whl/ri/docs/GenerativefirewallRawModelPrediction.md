# GenerativefirewallRawModelPrediction

RawModelPrediction represents the results of a model evaluation for the firewall. This is used in firewall telemetry help us debug and understand firewall results.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**classification_pred** | [**RawModelPredictionTextClassificationPred**](RawModelPredictionTextClassificationPred.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_raw_model_prediction import GenerativefirewallRawModelPrediction

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallRawModelPrediction from a JSON string
generativefirewall_raw_model_prediction_instance = GenerativefirewallRawModelPrediction.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallRawModelPrediction.to_json())

# convert the object into a dict
generativefirewall_raw_model_prediction_dict = generativefirewall_raw_model_prediction_instance.to_dict()
# create an instance of GenerativefirewallRawModelPrediction from a dict
generativefirewall_raw_model_prediction_from_dict = GenerativefirewallRawModelPrediction.from_dict(generativefirewall_raw_model_prediction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

