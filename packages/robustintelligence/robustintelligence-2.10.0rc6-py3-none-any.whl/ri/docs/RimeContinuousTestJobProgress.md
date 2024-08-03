# RimeContinuousTestJobProgress


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_runs** | [**List[RimeContinuousTestRunProgress]**](RimeContinuousTestRunProgress.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_continuous_test_job_progress import RimeContinuousTestJobProgress

# TODO update the JSON string below
json = "{}"
# create an instance of RimeContinuousTestJobProgress from a JSON string
rime_continuous_test_job_progress_instance = RimeContinuousTestJobProgress.from_json(json)
# print the JSON string representation of the object
print(RimeContinuousTestJobProgress.to_json())

# convert the object into a dict
rime_continuous_test_job_progress_dict = rime_continuous_test_job_progress_instance.to_dict()
# create an instance of RimeContinuousTestJobProgress from a dict
rime_continuous_test_job_progress_from_dict = RimeContinuousTestJobProgress.from_dict(rime_continuous_test_job_progress_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

