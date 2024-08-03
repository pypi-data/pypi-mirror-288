# RimeListImagesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**images** | [**List[RimeManagedImage]**](RimeManagedImage.md) |  | [optional] 
**next_page_token** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_images_response import RimeListImagesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListImagesResponse from a JSON string
rime_list_images_response_instance = RimeListImagesResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListImagesResponse.to_json())

# convert the object into a dict
rime_list_images_response_dict = rime_list_images_response_instance.to_dict()
# create an instance of RimeListImagesResponse from a dict
rime_list_images_response_from_dict = RimeListImagesResponse.from_dict(rime_list_images_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

