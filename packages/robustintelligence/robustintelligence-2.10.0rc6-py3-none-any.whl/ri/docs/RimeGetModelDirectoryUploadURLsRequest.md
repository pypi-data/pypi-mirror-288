# RimeGetModelDirectoryUploadURLsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**directory_name** | **str** | Path of model directory on local file system. | 
**relative_file_paths** | **List[str]** | Array of relative paths from the model directory to model files. | 
**upload_path** | **str** | Specify a path in the blob store to which the model will be uploaded. | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_model_directory_upload_urls_request import RimeGetModelDirectoryUploadURLsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetModelDirectoryUploadURLsRequest from a JSON string
rime_get_model_directory_upload_urls_request_instance = RimeGetModelDirectoryUploadURLsRequest.from_json(json)
# print the JSON string representation of the object
print(RimeGetModelDirectoryUploadURLsRequest.to_json())

# convert the object into a dict
rime_get_model_directory_upload_urls_request_dict = rime_get_model_directory_upload_urls_request_instance.to_dict()
# create an instance of RimeGetModelDirectoryUploadURLsRequest from a dict
rime_get_model_directory_upload_urls_request_from_dict = RimeGetModelDirectoryUploadURLsRequest.from_dict(rime_get_model_directory_upload_urls_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

