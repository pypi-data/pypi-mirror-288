# TestrunCustomMetric

Specifies configuration values for a custom metric.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the custom metric. | 
**file_path** | **str** | Path to the file with metric definition. | 
**range_lower_bound** | **float** | Valid range lower bound. | [optional] 
**range_upper_bound** | **float** | Valid range upper bound. | [optional] 
**run_subset_performance** | **bool** | Should run subset performance. | [optional] 
**run_subset_performance_drift** | **bool** | Should run subset performance drift. | [optional] 
**run_overall_performance** | **bool** | Should run overall performance. | [optional] 
**metadata** | [**CustomMetricCustomMetricMetadata**](CustomMetricCustomMetricMetadata.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrun_custom_metric import TestrunCustomMetric

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunCustomMetric from a JSON string
testrun_custom_metric_instance = TestrunCustomMetric.from_json(json)
# print the JSON string representation of the object
print(TestrunCustomMetric.to_json())

# convert the object into a dict
testrun_custom_metric_dict = testrun_custom_metric_instance.to_dict()
# create an instance of TestrunCustomMetric from a dict
testrun_custom_metric_from_dict = TestrunCustomMetric.from_dict(testrun_custom_metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

