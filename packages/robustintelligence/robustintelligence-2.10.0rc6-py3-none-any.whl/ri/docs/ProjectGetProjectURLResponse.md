# ProjectGetProjectURLResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | [**RimeSafeURL**](RimeSafeURL.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.project_get_project_url_response import ProjectGetProjectURLResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectGetProjectURLResponse from a JSON string
project_get_project_url_response_instance = ProjectGetProjectURLResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectGetProjectURLResponse.to_json())

# convert the object into a dict
project_get_project_url_response_dict = project_get_project_url_response_instance.to_dict()
# create an instance of ProjectGetProjectURLResponse from a dict
project_get_project_url_response_from_dict = ProjectGetProjectURLResponse.from_dict(project_get_project_url_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

