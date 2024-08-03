# RimeListImagesRequest

Request and response for a ListImages RPC.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page_token** | **str** | Specifies a page of the list returned by a ListImages query. The ListImages query returns a pageToken when there is more than one page of results. | [optional] 
**page_size** | **str** | The maximum number of Image objects to return in a single page. | [optional] 
**pip_libraries** | [**List[ListImagesRequestPipLibraryFilter]**](ListImagesRequestPipLibraryFilter.md) | Optional. Filters the list for libraries that are installed on the Managed Image. The filter is only active when the list is not empty. When this filter is specified, do not include a pageToken field in the request. | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_images_request import RimeListImagesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListImagesRequest from a JSON string
rime_list_images_request_instance = RimeListImagesRequest.from_json(json)
# print the JSON string representation of the object
print(RimeListImagesRequest.to_json())

# convert the object into a dict
rime_list_images_request_dict = rime_list_images_request_instance.to_dict()
# create an instance of RimeListImagesRequest from a dict
rime_list_images_request_from_dict = RimeListImagesRequest.from_dict(rime_list_images_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

