# FileSecurityReportDependency


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**severity** | [**LibgenerativeSeverity**](LibgenerativeSeverity.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.file_security_report_dependency import FileSecurityReportDependency

# TODO update the JSON string below
json = "{}"
# create an instance of FileSecurityReportDependency from a JSON string
file_security_report_dependency_instance = FileSecurityReportDependency.from_json(json)
# print the JSON string representation of the object
print(FileSecurityReportDependency.to_json())

# convert the object into a dict
file_security_report_dependency_dict = file_security_report_dependency_instance.to_dict()
# create an instance of FileSecurityReportDependency from a dict
file_security_report_dependency_from_dict = FileSecurityReportDependency.from_dict(file_security_report_dependency_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

