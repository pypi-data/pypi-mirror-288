# SchemafilescanningFileScanResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_scan_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**model_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**rime_agent_version** | **str** | The version of the RIME agent that was used to scan the model. | [optional] 
**upload_time** | **datetime** | The time when the file scan result was uploaded. | [optional] 
**file_security_reports** | [**List[SchemafilescanningFileSecurityReport]**](SchemafilescanningFileSecurityReport.md) | The security reports for the files that were scanned. | [optional] 
**repo_metadata** | [**SchemafilescanningRepoMetadata**](SchemafilescanningRepoMetadata.md) |  | [optional] 
**unscanned_file_paths** | **List[str]** | The list of files that were not scanned. | [optional] 
**severity** | [**RimeSeverity**](RimeSeverity.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.schemafilescanning_file_scan_result import SchemafilescanningFileScanResult

# TODO update the JSON string below
json = "{}"
# create an instance of SchemafilescanningFileScanResult from a JSON string
schemafilescanning_file_scan_result_instance = SchemafilescanningFileScanResult.from_json(json)
# print the JSON string representation of the object
print(SchemafilescanningFileScanResult.to_json())

# convert the object into a dict
schemafilescanning_file_scan_result_dict = schemafilescanning_file_scan_result_instance.to_dict()
# create an instance of SchemafilescanningFileScanResult from a dict
schemafilescanning_file_scan_result_from_dict = SchemafilescanningFileScanResult.from_dict(schemafilescanning_file_scan_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

