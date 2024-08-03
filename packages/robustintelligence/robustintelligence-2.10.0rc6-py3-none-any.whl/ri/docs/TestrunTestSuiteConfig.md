# TestrunTestSuiteConfig

TestSuiteConfig contains configuration for specific RIME tests in the test suite, configures which test categories to run, and configures the overall test sensitivity settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**global_test_sensitivity** | [**TestrunTestSensitivity**](TestrunTestSensitivity.md) |  | [optional] 
**individual_tests_config** | **str** | A serialized JSON blob including a config for each test. | [optional] 
**custom_tests** | **List[str]** | A list of JSON custom test configurations. | [optional] 
**global_exclude_columns** | **List[str]** | Features to exclude from all tests. | [optional] 

## Example

```python
from ri.apiclient.models.testrun_test_suite_config import TestrunTestSuiteConfig

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunTestSuiteConfig from a JSON string
testrun_test_suite_config_instance = TestrunTestSuiteConfig.from_json(json)
# print the JSON string representation of the object
print(TestrunTestSuiteConfig.to_json())

# convert the object into a dict
testrun_test_suite_config_dict = testrun_test_suite_config_instance.to_dict()
# create an instance of TestrunTestSuiteConfig from a dict
testrun_test_suite_config_from_dict = TestrunTestSuiteConfig.from_dict(testrun_test_suite_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

