# GenerativevalidationGenerativeValidationTestRun

GenerativeValidationTestRun are the details about a generative validation test run.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**name** | **str** | A name of the test run. | [optional] 
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**config** | [**GenerativevalidationGenerativeTestingConfig**](GenerativevalidationGenerativeTestingConfig.md) |  | [optional] 
**total_attacks** | **int** | Total attacks run during the test. | [optional] 
**successful_attacks** | **int** | The number of successful attacks on the model. | [optional] 
**job_info** | [**GenerativevalidationJobInfo**](GenerativevalidationJobInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.generativevalidation_generative_validation_test_run import GenerativevalidationGenerativeValidationTestRun

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativevalidationGenerativeValidationTestRun from a JSON string
generativevalidation_generative_validation_test_run_instance = GenerativevalidationGenerativeValidationTestRun.from_json(json)
# print the JSON string representation of the object
print(GenerativevalidationGenerativeValidationTestRun.to_json())

# convert the object into a dict
generativevalidation_generative_validation_test_run_dict = generativevalidation_generative_validation_test_run_instance.to_dict()
# create an instance of GenerativevalidationGenerativeValidationTestRun from a dict
generativevalidation_generative_validation_test_run_from_dict = GenerativevalidationGenerativeValidationTestRun.from_dict(generativevalidation_generative_validation_test_run_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

