# ListImagesRequestPipLibraryFilter

Specification of a filter for a pip library.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the library. | [optional] 
**version** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.list_images_request_pip_library_filter import ListImagesRequestPipLibraryFilter

# TODO update the JSON string below
json = "{}"
# create an instance of ListImagesRequestPipLibraryFilter from a JSON string
list_images_request_pip_library_filter_instance = ListImagesRequestPipLibraryFilter.from_json(json)
# print the JSON string representation of the object
print(ListImagesRequestPipLibraryFilter.to_json())

# convert the object into a dict
list_images_request_pip_library_filter_dict = list_images_request_pip_library_filter_instance.to_dict()
# create an instance of ListImagesRequestPipLibraryFilter from a dict
list_images_request_pip_library_filter_from_dict = ListImagesRequestPipLibraryFilter.from_dict(list_images_request_pip_library_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

