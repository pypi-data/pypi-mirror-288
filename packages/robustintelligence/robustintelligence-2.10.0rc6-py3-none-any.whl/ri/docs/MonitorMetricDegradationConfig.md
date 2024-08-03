# MonitorMetricDegradationConfig

MetricDegradation Monitors track metrics over time.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregation** | [**MonitorAggregation**](MonitorAggregation.md) |  | [optional] 
**transform** | [**MonitorTransform**](MonitorTransform.md) |  | [optional] 
**threshold** | [**MonitorThreshold**](MonitorThreshold.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.monitor_metric_degradation_config import MonitorMetricDegradationConfig

# TODO update the JSON string below
json = "{}"
# create an instance of MonitorMetricDegradationConfig from a JSON string
monitor_metric_degradation_config_instance = MonitorMetricDegradationConfig.from_json(json)
# print the JSON string representation of the object
print(MonitorMetricDegradationConfig.to_json())

# convert the object into a dict
monitor_metric_degradation_config_dict = monitor_metric_degradation_config_instance.to_dict()
# create an instance of MonitorMetricDegradationConfig from a dict
monitor_metric_degradation_config_from_dict = MonitorMetricDegradationConfig.from_dict(monitor_metric_degradation_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

