# TestrunTestRunConfig

TestRunConfig contains the configuration necessary to run a Stress Test. model_id and data_info are required fields.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**run_name** | **str** | Name for this Test Run. | 
**model_id** | [**RimeUUID**](RimeUUID.md) |  | 
**data_info** | [**TestrunRefEvalDatasets**](TestrunRefEvalDatasets.md) |  | 
**run_time_info** | [**RuntimeinfoRunTimeInfo**](RuntimeinfoRunTimeInfo.md) |  | [optional] 
**profiling_config** | [**TestrunProfilingConfig**](TestrunProfilingConfig.md) |  | [optional] 
**test_suite_config** | [**TestrunTestSuiteConfig**](TestrunTestSuiteConfig.md) |  | [optional] 
**categories** | [**List[TestrunTestCategoryType]**](TestrunTestCategoryType.md) | List of test categories to be run. | [optional] 

## Example

```python
from ri.apiclient.models.testrun_test_run_config import TestrunTestRunConfig

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunTestRunConfig from a JSON string
testrun_test_run_config_instance = TestrunTestRunConfig.from_json(json)
# print the JSON string representation of the object
print(TestrunTestRunConfig.to_json())

# convert the object into a dict
testrun_test_run_config_dict = testrun_test_run_config_instance.to_dict()
# create an instance of TestrunTestRunConfig from a dict
testrun_test_run_config_from_dict = TestrunTestRunConfig.from_dict(testrun_test_run_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

