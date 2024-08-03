# SchemasecuritydbRepoMetadataReputation

Information about the \"reputation\" of the model repository.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**downloads** | **int** | The number of times the model repository has been downloaded. | [optional] 
**likes** | **int** | The number of times the model repository has been liked. | [optional] 
**stars** | **int** | The number of times the model repository has been starred. | [optional] 
**forks** | **int** | The number of times the model repository has been forked. | [optional] 

## Example

```python
from ri.apiclient.models.schemasecuritydb_repo_metadata_reputation import SchemasecuritydbRepoMetadataReputation

# TODO update the JSON string below
json = "{}"
# create an instance of SchemasecuritydbRepoMetadataReputation from a JSON string
schemasecuritydb_repo_metadata_reputation_instance = SchemasecuritydbRepoMetadataReputation.from_json(json)
# print the JSON string representation of the object
print(SchemasecuritydbRepoMetadataReputation.to_json())

# convert the object into a dict
schemasecuritydb_repo_metadata_reputation_dict = schemasecuritydb_repo_metadata_reputation_instance.to_dict()
# create an instance of SchemasecuritydbRepoMetadataReputation from a dict
schemasecuritydb_repo_metadata_reputation_from_dict = SchemasecuritydbRepoMetadataReputation.from_dict(schemasecuritydb_repo_metadata_reputation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

