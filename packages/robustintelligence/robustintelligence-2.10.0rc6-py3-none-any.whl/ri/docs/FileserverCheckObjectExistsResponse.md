# FileserverCheckObjectExistsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exists** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.fileserver_check_object_exists_response import FileserverCheckObjectExistsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FileserverCheckObjectExistsResponse from a JSON string
fileserver_check_object_exists_response_instance = FileserverCheckObjectExistsResponse.from_json(json)
# print the JSON string representation of the object
print(FileserverCheckObjectExistsResponse.to_json())

# convert the object into a dict
fileserver_check_object_exists_response_dict = fileserver_check_object_exists_response_instance.to_dict()
# create an instance of FileserverCheckObjectExistsResponse from a dict
fileserver_check_object_exists_response_from_dict = FileserverCheckObjectExistsResponse.from_dict(fileserver_check_object_exists_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

