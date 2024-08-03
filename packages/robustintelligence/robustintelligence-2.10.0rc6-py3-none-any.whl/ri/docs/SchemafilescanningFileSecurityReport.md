# SchemafilescanningFileSecurityReport

The security report for a single file in the model repository.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filename** | **str** | The name of the file that was scanned. | 
**path** | **str** |  | [optional] 
**size** | **str** | The size of the file in bytes. | [optional] 
**sha256** | **str** |  | [optional] 
**creation_time** | **datetime** | The time when the file was created. | [optional] 
**last_modified_time** | **datetime** | The time when the file was last modified. | [optional] 
**dependencies** | **List[str]** | The list of all dependencies in the file. | [optional] 
**unexpected_dependencies** | **List[str]** | The list of unexpected dependencies. | [optional] 
**unsafe_dependencies** | **List[str]** | The list of unsafe dependencies. | [optional] 

## Example

```python
from ri.apiclient.models.schemafilescanning_file_security_report import SchemafilescanningFileSecurityReport

# TODO update the JSON string below
json = "{}"
# create an instance of SchemafilescanningFileSecurityReport from a JSON string
schemafilescanning_file_security_report_instance = SchemafilescanningFileSecurityReport.from_json(json)
# print the JSON string representation of the object
print(SchemafilescanningFileSecurityReport.to_json())

# convert the object into a dict
schemafilescanning_file_security_report_dict = schemafilescanning_file_security_report_instance.to_dict()
# create an instance of SchemafilescanningFileSecurityReport from a dict
schemafilescanning_file_security_report_from_dict = SchemafilescanningFileSecurityReport.from_dict(schemafilescanning_file_security_report_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

