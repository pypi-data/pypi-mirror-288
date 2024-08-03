# RimeListModelSecurityReportsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_security_reports** | [**List[SecuritydbModelSecurityReport]**](SecuritydbModelSecurityReport.md) | The list of security reports for the models. | [optional] 
**next_page_token** | **str** | A token to retrieve the next page of results. | [optional] 
**has_more** | **bool** | A boolean flag that specifies whether there are more results to return. | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_model_security_reports_response import RimeListModelSecurityReportsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListModelSecurityReportsResponse from a JSON string
rime_list_model_security_reports_response_instance = RimeListModelSecurityReportsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListModelSecurityReportsResponse.to_json())

# convert the object into a dict
rime_list_model_security_reports_response_dict = rime_list_model_security_reports_response_instance.to_dict()
# create an instance of RimeListModelSecurityReportsResponse from a dict
rime_list_model_security_reports_response_from_dict = RimeListModelSecurityReportsResponse.from_dict(rime_list_model_security_reports_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

