# SchemasecuritydbFileSecurityReport

The security report for a single file in the model repository.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filepath** | **str** | The name of the file that was scanned. | 
**size** | **int** | The size of the file in bytes. | [optional] 
**sha256** | **str** | The sha256 of the file that was scanned. | [optional] 
**creation_time** | **datetime** | The time when the file was created. | [optional] 
**last_modified_time** | **datetime** | The time when the file was last modified. | [optional] 
**dependencies** | [**List[FileSecurityReportDependency]**](FileSecurityReportDependency.md) | The list of all dependencies in the file. | [optional] 
**unsafe_dependencies** | [**List[FileSecurityReportDependency]**](FileSecurityReportDependency.md) | The list of unsafe dependencies. | [optional] 

## Example

```python
from ri.apiclient.models.schemasecuritydb_file_security_report import SchemasecuritydbFileSecurityReport

# TODO update the JSON string below
json = "{}"
# create an instance of SchemasecuritydbFileSecurityReport from a JSON string
schemasecuritydb_file_security_report_instance = SchemasecuritydbFileSecurityReport.from_json(json)
# print the JSON string representation of the object
print(SchemasecuritydbFileSecurityReport.to_json())

# convert the object into a dict
schemasecuritydb_file_security_report_dict = schemasecuritydb_file_security_report_instance.to_dict()
# create an instance of SchemasecuritydbFileSecurityReport from a dict
schemasecuritydb_file_security_report_from_dict = SchemasecuritydbFileSecurityReport.from_dict(schemasecuritydb_file_security_report_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

