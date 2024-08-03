# ModelModel

Model represents a full entry in the Model Registry, with info, metadata, and tags used to identify the model both internally and to an external user.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name and model_id are both enforced to be unique. Name is user specified. Model_id is internally generated. | [optional] 
**model_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**project_ids** | [**List[RimeUUID]**](RimeUUID.md) | For now, a model will only have one project_id associated with it. We make this an array to allow model&#39;s to be shared in the future. | [optional] 
**creator_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**creation_time** | **datetime** |  | [optional] 
**external_id** | **str** | external_id is an optional way for a user to identify the model with their own Model IDs. | [optional] 
**user_metadata** | [**RegistryMetadata**](RegistryMetadata.md) |  | [optional] 
**model_info** | [**RegistryModelInfo**](RegistryModelInfo.md) |  | [optional] 
**validity_status** | [**RegistryValidityStatus**](RegistryValidityStatus.md) |  | [optional] 
**integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**model_endpoint_integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**validity_status_message** | **str** | Information about the validity status of the model, such as why it is invalid. A Case where this would be populated is when the ValidityStatus is not explicitly set to valid by the XP validation task and additional details are required to convey to the user why the model is not valid. | [optional] 

## Example

```python
from ri.apiclient.models.model_model import ModelModel

# TODO update the JSON string below
json = "{}"
# create an instance of ModelModel from a JSON string
model_model_instance = ModelModel.from_json(json)
# print the JSON string representation of the object
print(ModelModel.to_json())

# convert the object into a dict
model_model_dict = model_model_instance.to_dict()
# create an instance of ModelModel from a dict
model_model_from_dict = ModelModel.from_dict(model_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

