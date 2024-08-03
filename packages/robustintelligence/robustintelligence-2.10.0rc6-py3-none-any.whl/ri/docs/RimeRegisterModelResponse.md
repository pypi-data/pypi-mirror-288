# RimeRegisterModelResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**registry_validation_job_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_register_model_response import RimeRegisterModelResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeRegisterModelResponse from a JSON string
rime_register_model_response_instance = RimeRegisterModelResponse.from_json(json)
# print the JSON string representation of the object
print(RimeRegisterModelResponse.to_json())

# convert the object into a dict
rime_register_model_response_dict = rime_register_model_response_instance.to_dict()
# create an instance of RimeRegisterModelResponse from a dict
rime_register_model_response_from_dict = RimeRegisterModelResponse.from_dict(rime_register_model_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

