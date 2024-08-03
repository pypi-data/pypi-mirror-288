# DatasetCTInfo

CTInfo represents information about the dataset and its use in CT runs.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**start_time** | **datetime** | Start and end time are the start and end time of this dataset. | 
**end_time** | **datetime** |  | 
**ct_dataset_type** | [**DatasetCTDatasetType**](DatasetCTDatasetType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.dataset_ct_info import DatasetCTInfo

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetCTInfo from a JSON string
dataset_ct_info_instance = DatasetCTInfo.from_json(json)
# print the JSON string representation of the object
print(DatasetCTInfo.to_json())

# convert the object into a dict
dataset_ct_info_dict = dataset_ct_info_instance.to_dict()
# create an instance of DatasetCTInfo from a dict
dataset_ct_info_from_dict = DatasetCTInfo.from_dict(dataset_ct_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

