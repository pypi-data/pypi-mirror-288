# RimeTestCaseMonitorInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**threshold** | [**MonitorThreshold**](MonitorThreshold.md) |  | [optional] 
**is_subset_metric** | **bool** |  | [optional] 
**excluded_transforms** | [**MonitorExcludedTransforms**](MonitorExcludedTransforms.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_test_case_monitor_info import RimeTestCaseMonitorInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RimeTestCaseMonitorInfo from a JSON string
rime_test_case_monitor_info_instance = RimeTestCaseMonitorInfo.from_json(json)
# print the JSON string representation of the object
print(RimeTestCaseMonitorInfo.to_json())

# convert the object into a dict
rime_test_case_monitor_info_dict = rime_test_case_monitor_info_instance.to_dict()
# create an instance of RimeTestCaseMonitorInfo from a dict
rime_test_case_monitor_info_from_dict = RimeTestCaseMonitorInfo.from_dict(rime_test_case_monitor_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

