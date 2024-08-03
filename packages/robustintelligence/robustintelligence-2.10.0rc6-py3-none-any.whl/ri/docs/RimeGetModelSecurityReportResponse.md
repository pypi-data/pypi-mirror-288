# RimeGetModelSecurityReportResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_security_report** | [**SecuritydbModelSecurityReport**](SecuritydbModelSecurityReport.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_model_security_report_response import RimeGetModelSecurityReportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetModelSecurityReportResponse from a JSON string
rime_get_model_security_report_response_instance = RimeGetModelSecurityReportResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetModelSecurityReportResponse.to_json())

# convert the object into a dict
rime_get_model_security_report_response_dict = rime_get_model_security_report_response_instance.to_dict()
# create an instance of RimeGetModelSecurityReportResponse from a dict
rime_get_model_security_report_response_from_dict = RimeGetModelSecurityReportResponse.from_dict(rime_get_model_security_report_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

