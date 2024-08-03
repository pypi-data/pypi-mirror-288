# RiskscoreRiskScore


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**RiskscoreRiskCategoryType**](RiskscoreRiskCategoryType.md) |  | [optional] 
**severity** | [**RimeSeverity**](RimeSeverity.md) |  | [optional] 
**score** | **float** | A risk score is a value between 0 and 1, where 0 is the lowest risk and 1 is the highest risk. | [optional] 

## Example

```python
from ri.apiclient.models.riskscore_risk_score import RiskscoreRiskScore

# TODO update the JSON string below
json = "{}"
# create an instance of RiskscoreRiskScore from a JSON string
riskscore_risk_score_instance = RiskscoreRiskScore.from_json(json)
# print the JSON string representation of the object
print(RiskscoreRiskScore.to_json())

# convert the object into a dict
riskscore_risk_score_dict = riskscore_risk_score_instance.to_dict()
# create an instance of RiskscoreRiskScore from a dict
riskscore_risk_score_from_dict = RiskscoreRiskScore.from_dict(riskscore_risk_score_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

