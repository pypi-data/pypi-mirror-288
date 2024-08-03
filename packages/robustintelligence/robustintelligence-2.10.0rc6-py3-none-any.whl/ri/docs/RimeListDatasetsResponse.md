# RimeListDatasetsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**datasets** | [**List[DatasetDataset]**](DatasetDataset.md) |  | [optional] 
**next_page_token** | **str** |  | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_datasets_response import RimeListDatasetsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListDatasetsResponse from a JSON string
rime_list_datasets_response_instance = RimeListDatasetsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListDatasetsResponse.to_json())

# convert the object into a dict
rime_list_datasets_response_dict = rime_list_datasets_response_instance.to_dict()
# create an instance of RimeListDatasetsResponse from a dict
rime_list_datasets_response_from_dict = RimeListDatasetsResponse.from_dict(rime_list_datasets_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

