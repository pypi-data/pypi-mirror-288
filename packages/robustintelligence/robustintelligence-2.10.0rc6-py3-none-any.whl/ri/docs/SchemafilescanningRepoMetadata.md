# SchemafilescanningRepoMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purl** | [**FilescanningPackageURL**](FilescanningPackageURL.md) |  | [optional] 
**repo_last_modified_time** | **datetime** | The time when the model repository was last modified, inferred from the git history. | [optional] 
**tags** | **List[str]** | The tags associated with the model repository. | [optional] 
**reputation** | [**SchemafilescanningRepoMetadataReputation**](SchemafilescanningRepoMetadataReputation.md) |  | [optional] 
**license** | [**SchemafilescanningRepoMetadataLicense**](SchemafilescanningRepoMetadataLicense.md) |  | [optional] 
**author** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.schemafilescanning_repo_metadata import SchemafilescanningRepoMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of SchemafilescanningRepoMetadata from a JSON string
schemafilescanning_repo_metadata_instance = SchemafilescanningRepoMetadata.from_json(json)
# print the JSON string representation of the object
print(SchemafilescanningRepoMetadata.to_json())

# convert the object into a dict
schemafilescanning_repo_metadata_dict = schemafilescanning_repo_metadata_instance.to_dict()
# create an instance of SchemafilescanningRepoMetadata from a dict
schemafilescanning_repo_metadata_from_dict = SchemafilescanningRepoMetadata.from_dict(schemafilescanning_repo_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

