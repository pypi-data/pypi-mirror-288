# RimeGetProjectIDResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_project_id_response import RimeGetProjectIDResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetProjectIDResponse from a JSON string
rime_get_project_id_response_instance = RimeGetProjectIDResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetProjectIDResponse.to_json())

# convert the object into a dict
rime_get_project_id_response_dict = rime_get_project_id_response_instance.to_dict()
# create an instance of RimeGetProjectIDResponse from a dict
rime_get_project_id_response_from_dict = RimeGetProjectIDResponse.from_dict(rime_get_project_id_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

