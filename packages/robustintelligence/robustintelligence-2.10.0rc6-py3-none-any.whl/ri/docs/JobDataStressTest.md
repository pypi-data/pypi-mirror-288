# JobDataStressTest

A stress test job runs a single test run over a model and dataset. This is also known as offline testing; it is run before production deployment of the model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**test_run_id** | **str** |  | [optional] 
**progress** | [**RimeStressTestJobProgress**](RimeStressTestJobProgress.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.job_data_stress_test import JobDataStressTest

# TODO update the JSON string below
json = "{}"
# create an instance of JobDataStressTest from a JSON string
job_data_stress_test_instance = JobDataStressTest.from_json(json)
# print the JSON string representation of the object
print(JobDataStressTest.to_json())

# convert the object into a dict
job_data_stress_test_dict = job_data_stress_test_instance.to_dict()
# create an instance of JobDataStressTest from a dict
job_data_stress_test_from_dict = JobDataStressTest.from_dict(job_data_stress_test_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

