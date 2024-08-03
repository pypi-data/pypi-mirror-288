# SchemafilescanningRepoMetadataReputation

Information about the \"reputation\" of the model repository.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**downloads** | **str** | The number of times the model repository has been downloaded. | [optional] 
**likes** | **str** | The number of times the model repository has been liked. | [optional] 
**stars** | **str** | The number of times the model repository has been starred. | [optional] 
**forks** | **str** | The number of times the model repository has been forked. | [optional] 

## Example

```python
from ri.apiclient.models.schemafilescanning_repo_metadata_reputation import SchemafilescanningRepoMetadataReputation

# TODO update the JSON string below
json = "{}"
# create an instance of SchemafilescanningRepoMetadataReputation from a JSON string
schemafilescanning_repo_metadata_reputation_instance = SchemafilescanningRepoMetadataReputation.from_json(json)
# print the JSON string representation of the object
print(SchemafilescanningRepoMetadataReputation.to_json())

# convert the object into a dict
schemafilescanning_repo_metadata_reputation_dict = schemafilescanning_repo_metadata_reputation_instance.to_dict()
# create an instance of SchemafilescanningRepoMetadataReputation from a dict
schemafilescanning_repo_metadata_reputation_from_dict = SchemafilescanningRepoMetadataReputation.from_dict(schemafilescanning_repo_metadata_reputation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

