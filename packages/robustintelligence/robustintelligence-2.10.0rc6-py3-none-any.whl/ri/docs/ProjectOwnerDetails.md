# ProjectOwnerDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**email** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.project_owner_details import ProjectOwnerDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectOwnerDetails from a JSON string
project_owner_details_instance = ProjectOwnerDetails.from_json(json)
# print the JSON string representation of the object
print(ProjectOwnerDetails.to_json())

# convert the object into a dict
project_owner_details_dict = project_owner_details_instance.to_dict()
# create an instance of ProjectOwnerDetails from a dict
project_owner_details_from_dict = ProjectOwnerDetails.from_dict(project_owner_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

