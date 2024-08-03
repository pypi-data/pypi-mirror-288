# RimeTestMetric


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metric** | **str** |  | [optional] 
**category** | [**RimeTestMetricCategory**](RimeTestMetricCategory.md) |  | [optional] 
**int_value** | **str** |  | [optional] 
**float_value** | **float** |  | [optional] 
**empty** | **object** |  | [optional] 
**str_value** | **str** |  | [optional] 
**int_list** | [**RimeIntList**](RimeIntList.md) |  | [optional] 
**float_list** | [**RimeFloatList**](RimeFloatList.md) |  | [optional] 
**str_list** | [**RimeStrList**](RimeStrList.md) |  | [optional] 
**test_case_monitor_info** | [**RimeTestCaseMonitorInfo**](RimeTestCaseMonitorInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_test_metric import RimeTestMetric

# TODO update the JSON string below
json = "{}"
# create an instance of RimeTestMetric from a JSON string
rime_test_metric_instance = RimeTestMetric.from_json(json)
# print the JSON string representation of the object
print(RimeTestMetric.to_json())

# convert the object into a dict
rime_test_metric_dict = rime_test_metric_instance.to_dict()
# create an instance of RimeTestMetric from a dict
rime_test_metric_from_dict = RimeTestMetric.from_dict(rime_test_metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

