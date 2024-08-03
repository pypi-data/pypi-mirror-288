# TestrunModelProfiling

Specifies configuration values for profiling the model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**nrows_for_summary** | **str** | Number of rows to perform inference on the model if no predictions. | [optional] 
**nrows_for_feature_importance** | **str** | Number of rows to calculate feature importance over. | [optional] 
**metric_configs_json** | **str** | JSON map of metric API names to keyword arguments, which allows configuration of arbitrary metrics. | [optional] 
**impact_metric** | **str** | Default impact metric. | [optional] 
**impact_label_threshold** | **float** | Specifies the threshold for measuring model impact using labeled performance metrics instead of prediction metrics, assuming partial labels. | [optional] 
**drift_impact_metric** | **str** | Default drift impact metric. | [optional] 
**subset_summary_metric** | **str** | The subset performance degradation summary metric is calculated by taking the difference between the worst subset degradation and the overall degradation of the configured metric. | [optional] 
**num_feats_for_subset_summary** | **str** | Number of features over which the subset performance degradation summary metric is aggregated. | [optional] 
**custom_metrics** | [**List[TestrunCustomMetric]**](TestrunCustomMetric.md) | List of custom metrics. | [optional] 

## Example

```python
from ri.apiclient.models.testrun_model_profiling import TestrunModelProfiling

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunModelProfiling from a JSON string
testrun_model_profiling_instance = TestrunModelProfiling.from_json(json)
# print the JSON string representation of the object
print(TestrunModelProfiling.to_json())

# convert the object into a dict
testrun_model_profiling_dict = testrun_model_profiling_instance.to_dict()
# create an instance of TestrunModelProfiling from a dict
testrun_model_profiling_from_dict = TestrunModelProfiling.from_dict(testrun_model_profiling_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

