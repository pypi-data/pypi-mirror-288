# RimeModelWithOwnerDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | [**ModelModel**](ModelModel.md) |  | [optional] 
**owner_details** | [**ProjectOwnerDetails**](ProjectOwnerDetails.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_model_with_owner_details import RimeModelWithOwnerDetails

# TODO update the JSON string below
json = "{}"
# create an instance of RimeModelWithOwnerDetails from a JSON string
rime_model_with_owner_details_instance = RimeModelWithOwnerDetails.from_json(json)
# print the JSON string representation of the object
print(RimeModelWithOwnerDetails.to_json())

# convert the object into a dict
rime_model_with_owner_details_dict = rime_model_with_owner_details_instance.to_dict()
# create an instance of RimeModelWithOwnerDetails from a dict
rime_model_with_owner_details_from_dict = RimeModelWithOwnerDetails.from_dict(rime_model_with_owner_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

