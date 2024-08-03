# FileserverListObjectsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**paths** | **List[str]** |  | [optional] 

## Example

```python
from ri.apiclient.models.fileserver_list_objects_response import FileserverListObjectsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FileserverListObjectsResponse from a JSON string
fileserver_list_objects_response_instance = FileserverListObjectsResponse.from_json(json)
# print the JSON string representation of the object
print(FileserverListObjectsResponse.to_json())

# convert the object into a dict
fileserver_list_objects_response_dict = fileserver_list_objects_response_instance.to_dict()
# create an instance of FileserverListObjectsResponse from a dict
fileserver_list_objects_response_from_dict = FileserverListObjectsResponse.from_dict(fileserver_list_objects_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

