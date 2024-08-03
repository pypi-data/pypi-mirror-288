# RimeTestRunProgress

TestRunProgress is a shared message for representing the progress of a single test run.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_run_id** | **str** |  | [optional] 
**status** | [**RimeTestTaskStatus**](RimeTestTaskStatus.md) |  | [optional] 
**test_batches** | [**List[TestRunProgressTestBatchProgress]**](TestRunProgressTestBatchProgress.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_test_run_progress import RimeTestRunProgress

# TODO update the JSON string below
json = "{}"
# create an instance of RimeTestRunProgress from a JSON string
rime_test_run_progress_instance = RimeTestRunProgress.from_json(json)
# print the JSON string representation of the object
print(RimeTestRunProgress.to_json())

# convert the object into a dict
rime_test_run_progress_dict = rime_test_run_progress_instance.to_dict()
# create an instance of RimeTestRunProgress from a dict
rime_test_run_progress_from_dict = RimeTestRunProgress.from_dict(rime_test_run_progress_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

