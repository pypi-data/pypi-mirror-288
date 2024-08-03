# RimeStressTestJobProgress


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_run** | [**RimeTestRunProgress**](RimeTestRunProgress.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_stress_test_job_progress import RimeStressTestJobProgress

# TODO update the JSON string below
json = "{}"
# create an instance of RimeStressTestJobProgress from a JSON string
rime_stress_test_job_progress_instance = RimeStressTestJobProgress.from_json(json)
# print the JSON string representation of the object
print(RimeStressTestJobProgress.to_json())

# convert the object into a dict
rime_stress_test_job_progress_dict = rime_stress_test_job_progress_instance.to_dict()
# create an instance of RimeStressTestJobProgress from a dict
rime_stress_test_job_progress_from_dict = RimeStressTestJobProgress.from_dict(rime_stress_test_job_progress_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

