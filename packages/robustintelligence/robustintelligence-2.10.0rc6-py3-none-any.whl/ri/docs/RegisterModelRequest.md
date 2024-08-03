# RegisterModelRequest

RegisterModelRequest registers a model for a given project with a source the model can be pulled from. Users can also specify metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **object** | Uniquely specifies a Project. | [optional] 
**name** | **str** | Unique name of the Model. | 
**metadata** | [**RegistryMetadata**](RegistryMetadata.md) |  | [optional] 
**external_id** | **str** | External ID that can be used to identify the model. | [optional] 
**model_info** | [**RegistryModelInfo**](RegistryModelInfo.md) |  | [optional] 
**integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**skip_validation** | **bool** | The parameter is deprecated since 2.7, and does not have any effect. Will always validate the model you are registering. Validation ensures that the model is valid for Robust Intelligence&#39;s systems. | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**model_endpoint_integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.register_model_request import RegisterModelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RegisterModelRequest from a JSON string
register_model_request_instance = RegisterModelRequest.from_json(json)
# print the JSON string representation of the object
print(RegisterModelRequest.to_json())

# convert the object into a dict
register_model_request_dict = register_model_request_instance.to_dict()
# create an instance of RegisterModelRequest from a dict
register_model_request_from_dict = RegisterModelRequest.from_dict(register_model_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

