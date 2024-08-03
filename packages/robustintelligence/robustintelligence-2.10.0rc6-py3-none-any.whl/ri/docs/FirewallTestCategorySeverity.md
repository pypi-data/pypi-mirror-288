# FirewallTestCategorySeverity


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_category** | [**TestrunTestCategoryType**](TestrunTestCategoryType.md) |  | [optional] 
**risk_category_type** | [**RiskscoreRiskCategoryType**](RiskscoreRiskCategoryType.md) |  | [optional] 
**severity** | [**RimeSeverity**](RimeSeverity.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.firewall_test_category_severity import FirewallTestCategorySeverity

# TODO update the JSON string below
json = "{}"
# create an instance of FirewallTestCategorySeverity from a JSON string
firewall_test_category_severity_instance = FirewallTestCategorySeverity.from_json(json)
# print the JSON string representation of the object
print(FirewallTestCategorySeverity.to_json())

# convert the object into a dict
firewall_test_category_severity_dict = firewall_test_category_severity_instance.to_dict()
# create an instance of FirewallTestCategorySeverity from a dict
firewall_test_category_severity_from_dict = FirewallTestCategorySeverity.from_dict(firewall_test_category_severity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

