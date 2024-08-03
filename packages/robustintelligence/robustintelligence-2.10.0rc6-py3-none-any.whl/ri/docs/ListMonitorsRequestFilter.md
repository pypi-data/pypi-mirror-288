# ListMonitorsRequestFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**included_monitor_types** | [**List[MonitorMonitorType]**](MonitorMonitorType.md) | Specifies a list of monitor types. Filters results to match the specified monitor types. | [optional] 
**included_risk_category_types** | [**List[RiskscoreRiskCategoryType]**](RiskscoreRiskCategoryType.md) | Specifies a list of risk category types. Filters results to match the specified risk category types. | [optional] 
**pinned_monitors_only** | **bool** | When the value of this Boolean is True, this endpoint returns a list of pinned Monitors. Otherwise, this endpoint does not filter Monitors by pinned status. | [optional] 

## Example

```python
from ri.apiclient.models.list_monitors_request_filter import ListMonitorsRequestFilter

# TODO update the JSON string below
json = "{}"
# create an instance of ListMonitorsRequestFilter from a JSON string
list_monitors_request_filter_instance = ListMonitorsRequestFilter.from_json(json)
# print the JSON string representation of the object
print(ListMonitorsRequestFilter.to_json())

# convert the object into a dict
list_monitors_request_filter_dict = list_monitors_request_filter_instance.to_dict()
# create an instance of ListMonitorsRequestFilter from a dict
list_monitors_request_filter_from_dict = ListMonitorsRequestFilter.from_dict(list_monitors_request_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

