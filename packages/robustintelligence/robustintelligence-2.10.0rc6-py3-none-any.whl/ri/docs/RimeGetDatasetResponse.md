# RimeGetDatasetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset** | [**DatasetDataset**](DatasetDataset.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_dataset_response import RimeGetDatasetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetDatasetResponse from a JSON string
rime_get_dataset_response_instance = RimeGetDatasetResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetDatasetResponse.to_json())

# convert the object into a dict
rime_get_dataset_response_dict = rime_get_dataset_response_instance.to_dict()
# create an instance of RimeGetDatasetResponse from a dict
rime_get_dataset_response_from_dict = RimeGetDatasetResponse.from_dict(rime_get_dataset_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

