# RimeListUploadedFileURLsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_urls** | **List[str]** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_uploaded_file_urls_response import RimeListUploadedFileURLsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListUploadedFileURLsResponse from a JSON string
rime_list_uploaded_file_urls_response_instance = RimeListUploadedFileURLsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListUploadedFileURLsResponse.to_json())

# convert the object into a dict
rime_list_uploaded_file_urls_response_dict = rime_list_uploaded_file_urls_response_instance.to_dict()
# create an instance of RimeListUploadedFileURLsResponse from a dict
rime_list_uploaded_file_urls_response_from_dict = RimeListUploadedFileURLsResponse.from_dict(rime_list_uploaded_file_urls_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

