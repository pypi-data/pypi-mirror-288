# TestrunTestRunIncrementalConfig

TestRunIncrementalConfig contains the configuration necessary to run a Continuous Test.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**eval_dataset_id** | **str** | Uniquely specifies an evaluation Dataset. | [optional] 
**run_time_info** | [**RuntimeinfoRunTimeInfo**](RuntimeinfoRunTimeInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrun_test_run_incremental_config import TestrunTestRunIncrementalConfig

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunTestRunIncrementalConfig from a JSON string
testrun_test_run_incremental_config_instance = TestrunTestRunIncrementalConfig.from_json(json)
# print the JSON string representation of the object
print(TestrunTestRunIncrementalConfig.to_json())

# convert the object into a dict
testrun_test_run_incremental_config_dict = testrun_test_run_incremental_config_instance.to_dict()
# create an instance of TestrunTestRunIncrementalConfig from a dict
testrun_test_run_incremental_config_from_dict = TestrunTestRunIncrementalConfig.from_dict(testrun_test_run_incremental_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

