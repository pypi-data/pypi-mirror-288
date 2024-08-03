# RegisterDatasetRequest

RegisterDatasetRequest registers a dataset for a given project with a source the data can be pulled from. Users can also specify metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **object** | Uniquely specifies a Project. | [optional] 
**name** | **str** | Unique name of the Dataset. | 
**metadata** | [**RegistryMetadata**](RegistryMetadata.md) |  | [optional] 
**integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**data_info** | [**RegistryDataInfo**](RegistryDataInfo.md) |  | [optional] 
**ct_info** | [**DatasetCTInfo**](DatasetCTInfo.md) |  | [optional] 
**skip_validation** | **bool** | The parameter is deprecated since 2.7, and does not have any effect. Will always validate the dataset you are registering. Validation ensures that the dataset is valid for Robust Intelligence&#39;s systems. | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.register_dataset_request import RegisterDatasetRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RegisterDatasetRequest from a JSON string
register_dataset_request_instance = RegisterDatasetRequest.from_json(json)
# print the JSON string representation of the object
print(RegisterDatasetRequest.to_json())

# convert the object into a dict
register_dataset_request_dict = register_dataset_request_instance.to_dict()
# create an instance of RegisterDatasetRequest from a dict
register_dataset_request_from_dict = RegisterDatasetRequest.from_dict(register_dataset_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

