# SchemasecuritydbFileScanResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result_update_time** | **datetime** | The time when the result was updated. | [optional] 
**file_security_reports** | [**List[SchemasecuritydbFileSecurityReport]**](SchemasecuritydbFileSecurityReport.md) | The security reports for the files that were scanned. | [optional] 
**scanned_file_paths** | **List[str]** | The list of files that were scanned. | [optional] 
**severity** | [**LibgenerativeSeverity**](LibgenerativeSeverity.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.schemasecuritydb_file_scan_result import SchemasecuritydbFileScanResult

# TODO update the JSON string below
json = "{}"
# create an instance of SchemasecuritydbFileScanResult from a JSON string
schemasecuritydb_file_scan_result_instance = SchemasecuritydbFileScanResult.from_json(json)
# print the JSON string representation of the object
print(SchemasecuritydbFileScanResult.to_json())

# convert the object into a dict
schemasecuritydb_file_scan_result_dict = schemasecuritydb_file_scan_result_instance.to_dict()
# create an instance of SchemasecuritydbFileScanResult from a dict
schemasecuritydb_file_scan_result_from_dict = SchemasecuritydbFileScanResult.from_dict(schemasecuritydb_file_scan_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

