# RimeStartValidateDatasetTaskResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_start_validate_dataset_task_response import RimeStartValidateDatasetTaskResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeStartValidateDatasetTaskResponse from a JSON string
rime_start_validate_dataset_task_response_instance = RimeStartValidateDatasetTaskResponse.from_json(json)
# print the JSON string representation of the object
print(RimeStartValidateDatasetTaskResponse.to_json())

# convert the object into a dict
rime_start_validate_dataset_task_response_dict = rime_start_validate_dataset_task_response_instance.to_dict()
# create an instance of RimeStartValidateDatasetTaskResponse from a dict
rime_start_validate_dataset_task_response_from_dict = RimeStartValidateDatasetTaskResponse.from_dict(rime_start_validate_dataset_task_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

