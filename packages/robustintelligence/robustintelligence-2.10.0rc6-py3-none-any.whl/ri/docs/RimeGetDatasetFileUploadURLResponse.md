# RimeGetDatasetFileUploadURLResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**upload_url** | **str** |  | [optional] 
**done_file_upload_url** | **str** |  | [optional] 
**destination_url** | **str** |  | [optional] 
**upload_limit** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_dataset_file_upload_url_response import RimeGetDatasetFileUploadURLResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetDatasetFileUploadURLResponse from a JSON string
rime_get_dataset_file_upload_url_response_instance = RimeGetDatasetFileUploadURLResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetDatasetFileUploadURLResponse.to_json())

# convert the object into a dict
rime_get_dataset_file_upload_url_response_dict = rime_get_dataset_file_upload_url_response_instance.to_dict()
# create an instance of RimeGetDatasetFileUploadURLResponse from a dict
rime_get_dataset_file_upload_url_response_from_dict = RimeGetDatasetFileUploadURLResponse.from_dict(rime_get_dataset_file_upload_url_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

