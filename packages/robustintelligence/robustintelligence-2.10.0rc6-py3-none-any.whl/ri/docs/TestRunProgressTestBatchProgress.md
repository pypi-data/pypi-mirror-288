# TestRunProgressTestBatchProgress


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | (test run ID, test batch type) are a unique ID of the test batch. | [optional] 
**status** | [**RimeTestTaskStatus**](RimeTestTaskStatus.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.test_run_progress_test_batch_progress import TestRunProgressTestBatchProgress

# TODO update the JSON string below
json = "{}"
# create an instance of TestRunProgressTestBatchProgress from a JSON string
test_run_progress_test_batch_progress_instance = TestRunProgressTestBatchProgress.from_json(json)
# print the JSON string representation of the object
print(TestRunProgressTestBatchProgress.to_json())

# convert the object into a dict
test_run_progress_test_batch_progress_dict = test_run_progress_test_batch_progress_instance.to_dict()
# create an instance of TestRunProgressTestBatchProgress from a dict
test_run_progress_test_batch_progress_from_dict = TestRunProgressTestBatchProgress.from_dict(test_run_progress_test_batch_progress_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

