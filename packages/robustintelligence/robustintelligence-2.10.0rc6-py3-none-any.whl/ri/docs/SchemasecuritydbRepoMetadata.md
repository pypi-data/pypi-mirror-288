# SchemasecuritydbRepoMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version_info** | **str** | The version info of the model. | [optional] 
**repo_last_modified_time** | **datetime** | The time when the model repository was last modified, inferred from the git history. | [optional] 
**tags** | **List[str]** | The tags associated with the model repository. | [optional] 
**reputation** | [**SchemasecuritydbRepoMetadataReputation**](SchemasecuritydbRepoMetadataReputation.md) |  | [optional] 
**license** | [**SchemasecuritydbRepoMetadataLicense**](SchemasecuritydbRepoMetadataLicense.md) |  | [optional] 
**author** | **str** | The author of the model repository. | [optional] 

## Example

```python
from ri.apiclient.models.schemasecuritydb_repo_metadata import SchemasecuritydbRepoMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of SchemasecuritydbRepoMetadata from a JSON string
schemasecuritydb_repo_metadata_instance = SchemasecuritydbRepoMetadata.from_json(json)
# print the JSON string representation of the object
print(SchemasecuritydbRepoMetadata.to_json())

# convert the object into a dict
schemasecuritydb_repo_metadata_dict = schemasecuritydb_repo_metadata_instance.to_dict()
# create an instance of SchemasecuritydbRepoMetadata from a dict
schemasecuritydb_repo_metadata_from_dict = SchemasecuritydbRepoMetadata.from_dict(schemasecuritydb_repo_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

