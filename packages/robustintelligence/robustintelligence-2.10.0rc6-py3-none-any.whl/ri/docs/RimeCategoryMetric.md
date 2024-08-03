# RimeCategoryMetric


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**value** | **float** |  | [optional] 
**threshold** | [**MonitorThreshold**](MonitorThreshold.md) |  | [optional] 
**description** | **str** |  | [optional] 
**risk_category_type** | [**RiskscoreRiskCategoryType**](RiskscoreRiskCategoryType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_category_metric import RimeCategoryMetric

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCategoryMetric from a JSON string
rime_category_metric_instance = RimeCategoryMetric.from_json(json)
# print the JSON string representation of the object
print(RimeCategoryMetric.to_json())

# convert the object into a dict
rime_category_metric_dict = rime_category_metric_instance.to_dict()
# create an instance of RimeCategoryMetric from a dict
rime_category_metric_from_dict = RimeCategoryMetric.from_dict(rime_category_metric_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

