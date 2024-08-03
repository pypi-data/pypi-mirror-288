# RimeGetValidatePredictionsTaskStatusResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resp** | [**ValidationValidatePredictionsResponse**](ValidationValidatePredictionsResponse.md) |  | [optional] 
**job_metadata** | [**RimeJobMetadata**](RimeJobMetadata.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_validate_predictions_task_status_response import RimeGetValidatePredictionsTaskStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetValidatePredictionsTaskStatusResponse from a JSON string
rime_get_validate_predictions_task_status_response_instance = RimeGetValidatePredictionsTaskStatusResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetValidatePredictionsTaskStatusResponse.to_json())

# convert the object into a dict
rime_get_validate_predictions_task_status_response_dict = rime_get_validate_predictions_task_status_response_instance.to_dict()
# create an instance of RimeGetValidatePredictionsTaskStatusResponse from a dict
rime_get_validate_predictions_task_status_response_from_dict = RimeGetValidatePredictionsTaskStatusResponse.from_dict(rime_get_validate_predictions_task_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

