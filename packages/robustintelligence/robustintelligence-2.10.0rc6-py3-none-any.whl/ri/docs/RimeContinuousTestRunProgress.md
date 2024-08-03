# RimeContinuousTestRunProgress

ContinuousTestRunProgress is a wrapper around TestRunProgress with added metadata about the bins.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_run** | [**RimeTestRunProgress**](RimeTestRunProgress.md) |  | [optional] 
**bin_start_time** | **datetime** |  | [optional] 
**bin_end_time** | **datetime** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_continuous_test_run_progress import RimeContinuousTestRunProgress

# TODO update the JSON string below
json = "{}"
# create an instance of RimeContinuousTestRunProgress from a JSON string
rime_continuous_test_run_progress_instance = RimeContinuousTestRunProgress.from_json(json)
# print the JSON string representation of the object
print(RimeContinuousTestRunProgress.to_json())

# convert the object into a dict
rime_continuous_test_run_progress_dict = rime_continuous_test_run_progress_instance.to_dict()
# create an instance of RimeContinuousTestRunProgress from a dict
rime_continuous_test_run_progress_from_dict = RimeContinuousTestRunProgress.from_dict(rime_continuous_test_run_progress_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

