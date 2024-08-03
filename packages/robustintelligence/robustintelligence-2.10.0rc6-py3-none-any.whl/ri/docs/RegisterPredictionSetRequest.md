# RegisterPredictionSetRequest

RegisterPredictionRequest registers a prediction for a reference model/ dataset and a source of data for predictions provided. Users can also specify metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **object** | Uniquely specifies a Project. | [optional] 
**model_id** | **object** | Uniquely specifies a Model. | [optional] 
**metadata** | [**RegistryMetadata**](RegistryMetadata.md) |  | [optional] 
**integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**pred_info** | [**RegistryPredInfo**](RegistryPredInfo.md) |  | [optional] 
**skip_validation** | **bool** | The parameter is deprecated since 2.7, and does not have any effect. Will always validate the predictions you are registering. Validation ensures that the predictions is valid for Robust Intelligence&#39;s systems. | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.register_prediction_set_request import RegisterPredictionSetRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RegisterPredictionSetRequest from a JSON string
register_prediction_set_request_instance = RegisterPredictionSetRequest.from_json(json)
# print the JSON string representation of the object
print(RegisterPredictionSetRequest.to_json())

# convert the object into a dict
register_prediction_set_request_dict = register_prediction_set_request_instance.to_dict()
# create an instance of RegisterPredictionSetRequest from a dict
register_prediction_set_request_from_dict = RegisterPredictionSetRequest.from_dict(register_prediction_set_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

