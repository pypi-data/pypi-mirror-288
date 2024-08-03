# ArtifactIdentifierCategoryTestIdentifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_category** | [**TestrunTestCategoryType**](TestrunTestCategoryType.md) |  | [optional] 
**metric** | **str** | The metric name. | [optional] 

## Example

```python
from ri.apiclient.models.artifact_identifier_category_test_identifier import ArtifactIdentifierCategoryTestIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of ArtifactIdentifierCategoryTestIdentifier from a JSON string
artifact_identifier_category_test_identifier_instance = ArtifactIdentifierCategoryTestIdentifier.from_json(json)
# print the JSON string representation of the object
print(ArtifactIdentifierCategoryTestIdentifier.to_json())

# convert the object into a dict
artifact_identifier_category_test_identifier_dict = artifact_identifier_category_test_identifier_instance.to_dict()
# create an instance of ArtifactIdentifierCategoryTestIdentifier from a dict
artifact_identifier_category_test_identifier_from_dict = ArtifactIdentifierCategoryTestIdentifier.from_dict(artifact_identifier_category_test_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

