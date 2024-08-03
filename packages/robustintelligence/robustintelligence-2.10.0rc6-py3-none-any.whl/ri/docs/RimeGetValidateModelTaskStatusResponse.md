# RimeGetValidateModelTaskStatusResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resp** | [**ValidationValidateModelResponse**](ValidationValidateModelResponse.md) |  | [optional] 
**job_metadata** | [**RimeJobMetadata**](RimeJobMetadata.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_validate_model_task_status_response import RimeGetValidateModelTaskStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetValidateModelTaskStatusResponse from a JSON string
rime_get_validate_model_task_status_response_instance = RimeGetValidateModelTaskStatusResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetValidateModelTaskStatusResponse.to_json())

# convert the object into a dict
rime_get_validate_model_task_status_response_dict = rime_get_validate_model_task_status_response_instance.to_dict()
# create an instance of RimeGetValidateModelTaskStatusResponse from a dict
rime_get_validate_model_task_status_response_from_dict = RimeGetValidateModelTaskStatusResponse.from_dict(rime_get_validate_model_task_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

