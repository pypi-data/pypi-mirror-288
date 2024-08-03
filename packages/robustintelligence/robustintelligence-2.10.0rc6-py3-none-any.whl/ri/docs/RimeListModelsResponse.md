# RimeListModelsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**models** | [**List[RimeModelWithOwnerDetails]**](RimeModelWithOwnerDetails.md) |  | [optional] 
**next_page_token** | **str** |  | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_models_response import RimeListModelsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListModelsResponse from a JSON string
rime_list_models_response_instance = RimeListModelsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListModelsResponse.to_json())

# convert the object into a dict
rime_list_models_response_dict = rime_list_models_response_instance.to_dict()
# create an instance of RimeListModelsResponse from a dict
rime_list_models_response_from_dict = RimeListModelsResponse.from_dict(rime_list_models_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

