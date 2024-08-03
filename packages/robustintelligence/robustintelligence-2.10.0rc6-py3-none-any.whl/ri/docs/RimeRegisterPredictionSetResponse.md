# RimeRegisterPredictionSetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**registry_validation_job_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_register_prediction_set_response import RimeRegisterPredictionSetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeRegisterPredictionSetResponse from a JSON string
rime_register_prediction_set_response_instance = RimeRegisterPredictionSetResponse.from_json(json)
# print the JSON string representation of the object
print(RimeRegisterPredictionSetResponse.to_json())

# convert the object into a dict
rime_register_prediction_set_response_dict = rime_register_prediction_set_response_instance.to_dict()
# create an instance of RimeRegisterPredictionSetResponse from a dict
rime_register_prediction_set_response_from_dict = RimeRegisterPredictionSetResponse.from_dict(rime_register_prediction_set_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

