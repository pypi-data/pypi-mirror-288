# TestRunMetricsCategorySummaryMetric

CategorySummaryMetric returns a summary metric across test batches for a particular category, such as the average severity for all \"Drift\" tests.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_category** | [**TestrunTestCategoryType**](TestrunTestCategoryType.md) |  | [optional] 
**category_id** | **str** | The string field &#x60;category&#x60; is deprecated in v2.1 and will be removed in v2.3. Please use the enum field test_category instead, which provides the same info. | [optional] 
**name** | **str** | The name of the category. | [optional] 
**value** | **float** | The value of the metric over the specified category. | [optional] 

## Example

```python
from ri.apiclient.models.test_run_metrics_category_summary_metric import TestRunMetricsCategorySummaryMetric

# TODO update the JSON string below
json = "{}"
# create an instance of TestRunMetricsCategorySummaryMetric from a JSON string
test_run_metrics_category_summary_metric_instance = TestRunMetricsCategorySummaryMetric.from_json(json)
# print the JSON string representation of the object
print(TestRunMetricsCategorySummaryMetric.to_json())

# convert the object into a dict
test_run_metrics_category_summary_metric_dict = test_run_metrics_category_summary_metric_instance.to_dict()
# create an instance of TestRunMetricsCategorySummaryMetric from a dict
test_run_metrics_category_summary_metric_from_dict = TestRunMetricsCategorySummaryMetric.from_dict(test_run_metrics_category_summary_metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

