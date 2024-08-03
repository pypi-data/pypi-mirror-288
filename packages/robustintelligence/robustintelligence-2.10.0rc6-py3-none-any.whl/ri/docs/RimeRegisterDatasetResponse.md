# RimeRegisterDatasetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **str** | dataset_id is a string as it contains semantic meaning and does not adhere to UUID standard. | [optional] 
**registry_validation_job_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_register_dataset_response import RimeRegisterDatasetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeRegisterDatasetResponse from a JSON string
rime_register_dataset_response_instance = RimeRegisterDatasetResponse.from_json(json)
# print the JSON string representation of the object
print(RimeRegisterDatasetResponse.to_json())

# convert the object into a dict
rime_register_dataset_response_dict = rime_register_dataset_response_instance.to_dict()
# create an instance of RimeRegisterDatasetResponse from a dict
rime_register_dataset_response_from_dict = RimeRegisterDatasetResponse.from_dict(rime_register_dataset_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

