# TestRunMetricsModelPerfMetric

ModelPerfMetric returns the model performance for a metric over the reference and evaluation datasets.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ref_metric** | **float** | Optional metric for the reference dataset. | [optional] 
**eval_metric** | **float** | Optional metric for the evaluation dataset. | [optional] 

## Example

```python
from ri.apiclient.models.test_run_metrics_model_perf_metric import TestRunMetricsModelPerfMetric

# TODO update the JSON string below
json = "{}"
# create an instance of TestRunMetricsModelPerfMetric from a JSON string
test_run_metrics_model_perf_metric_instance = TestRunMetricsModelPerfMetric.from_json(json)
# print the JSON string representation of the object
print(TestRunMetricsModelPerfMetric.to_json())

# convert the object into a dict
test_run_metrics_model_perf_metric_dict = test_run_metrics_model_perf_metric_instance.to_dict()
# create an instance of TestRunMetricsModelPerfMetric from a dict
test_run_metrics_model_perf_metric_from_dict = TestRunMetricsModelPerfMetric.from_dict(test_run_metrics_model_perf_metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

