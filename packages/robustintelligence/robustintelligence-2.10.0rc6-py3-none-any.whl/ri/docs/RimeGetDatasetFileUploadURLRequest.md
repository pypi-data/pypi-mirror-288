# RimeGetDatasetFileUploadURLRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_name** | **str** | Path of dataset file on the local file system. | 
**upload_path** | **str** | Specify a path in the blob store to use for data uploads. | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_dataset_file_upload_url_request import RimeGetDatasetFileUploadURLRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetDatasetFileUploadURLRequest from a JSON string
rime_get_dataset_file_upload_url_request_instance = RimeGetDatasetFileUploadURLRequest.from_json(json)
# print the JSON string representation of the object
print(RimeGetDatasetFileUploadURLRequest.to_json())

# convert the object into a dict
rime_get_dataset_file_upload_url_request_dict = rime_get_dataset_file_upload_url_request_instance.to_dict()
# create an instance of RimeGetDatasetFileUploadURLRequest from a dict
rime_get_dataset_file_upload_url_request_from_dict = RimeGetDatasetFileUploadURLRequest.from_dict(rime_get_dataset_file_upload_url_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

