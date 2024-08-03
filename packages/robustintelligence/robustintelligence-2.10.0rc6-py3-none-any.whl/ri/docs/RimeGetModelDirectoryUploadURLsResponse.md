# RimeGetModelDirectoryUploadURLsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**upload_path_map** | **Dict[str, str]** |  | [optional] 
**done_file_upload_url** | **str** |  | [optional] 
**destination_url** | **str** |  | [optional] 
**upload_limit** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_model_directory_upload_urls_response import RimeGetModelDirectoryUploadURLsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetModelDirectoryUploadURLsResponse from a JSON string
rime_get_model_directory_upload_urls_response_instance = RimeGetModelDirectoryUploadURLsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetModelDirectoryUploadURLsResponse.to_json())

# convert the object into a dict
rime_get_model_directory_upload_urls_response_dict = rime_get_model_directory_upload_urls_response_instance.to_dict()
# create an instance of RimeGetModelDirectoryUploadURLsResponse from a dict
rime_get_model_directory_upload_urls_response_from_dict = RimeGetModelDirectoryUploadURLsResponse.from_dict(rime_get_model_directory_upload_urls_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

