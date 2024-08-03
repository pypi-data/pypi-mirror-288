# SchemamonitorConfig

Config defines a configuration for a monitor. There are different varities of monitors, such as metric degradation monitors and anomaly monitors. Metric degradation monitors track metrics over time and make up the vast majority of monitors in our system. Anomaly monitors track discrete events such as Security infractions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**degradation** | [**MonitorMetricDegradationConfig**](MonitorMetricDegradationConfig.md) |  | [optional] 
**anomaly** | **object** | Anomaly Monitors track events over time that are not associated with metrics. For instance, attacks on a model constitute Anomalies. | [optional] 

## Example

```python
from ri.apiclient.models.schemamonitor_config import SchemamonitorConfig

# TODO update the JSON string below
json = "{}"
# create an instance of SchemamonitorConfig from a JSON string
schemamonitor_config_instance = SchemamonitorConfig.from_json(json)
# print the JSON string representation of the object
print(SchemamonitorConfig.to_json())

# convert the object into a dict
schemamonitor_config_dict = schemamonitor_config_instance.to_dict()
# create an instance of SchemamonitorConfig from a dict
schemamonitor_config_from_dict = SchemamonitorConfig.from_dict(schemamonitor_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

