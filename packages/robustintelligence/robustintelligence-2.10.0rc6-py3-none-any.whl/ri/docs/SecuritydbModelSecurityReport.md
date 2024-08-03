# SecuritydbModelSecurityReport


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**repo_id** | **str** | The ID of the model repository on Hugging Face. | [optional] 
**description** | **str** | Description of the availability of the security report such as &#39;Scan completed&#39; or &#39;Scan in progress. Please check back later for results&#39;. | [optional] 
**repo_metadata** | [**SchemasecuritydbRepoMetadata**](SchemasecuritydbRepoMetadata.md) |  | [optional] 
**file_scan_result** | [**SchemasecuritydbFileScanResult**](SchemasecuritydbFileScanResult.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.securitydb_model_security_report import SecuritydbModelSecurityReport

# TODO update the JSON string below
json = "{}"
# create an instance of SecuritydbModelSecurityReport from a JSON string
securitydb_model_security_report_instance = SecuritydbModelSecurityReport.from_json(json)
# print the JSON string representation of the object
print(SecuritydbModelSecurityReport.to_json())

# convert the object into a dict
securitydb_model_security_report_dict = securitydb_model_security_report_instance.to_dict()
# create an instance of SecuritydbModelSecurityReport from a dict
securitydb_model_security_report_from_dict = SecuritydbModelSecurityReport.from_dict(securitydb_model_security_report_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

