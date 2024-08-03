# RimeGetValidateDatasetTaskStatusResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resp** | [**ValidationValidateDatasetResponse**](ValidationValidateDatasetResponse.md) |  | [optional] 
**job_metadata** | [**RimeJobMetadata**](RimeJobMetadata.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_validate_dataset_task_status_response import RimeGetValidateDatasetTaskStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetValidateDatasetTaskStatusResponse from a JSON string
rime_get_validate_dataset_task_status_response_instance = RimeGetValidateDatasetTaskStatusResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetValidateDatasetTaskStatusResponse.to_json())

# convert the object into a dict
rime_get_validate_dataset_task_status_response_dict = rime_get_validate_dataset_task_status_response_instance.to_dict()
# create an instance of RimeGetValidateDatasetTaskStatusResponse from a dict
rime_get_validate_dataset_task_status_response_from_dict = RimeGetValidateDatasetTaskStatusResponse.from_dict(rime_get_validate_dataset_task_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

