# StartStressTestRequest

StartStressTestRequest is the request object containing the project information and the configurations for the Stress Test.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **object** | Uniquely specifies a Project. | [optional] 
**test_run_config** | [**TestrunTestRunConfig**](TestrunTestRunConfig.md) |  | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**experimental_fields** | **Dict[str, object]** | Fields that enable experimental functionality.  WARNING: these fields are experimental; ie, their functionality may not be reliable or backwards-compatible. Do not use these fields in production. | [optional] 

## Example

```python
from ri.apiclient.models.start_stress_test_request import StartStressTestRequest

# TODO update the JSON string below
json = "{}"
# create an instance of StartStressTestRequest from a JSON string
start_stress_test_request_instance = StartStressTestRequest.from_json(json)
# print the JSON string representation of the object
print(StartStressTestRequest.to_json())

# convert the object into a dict
start_stress_test_request_dict = start_stress_test_request_instance.to_dict()
# create an instance of StartStressTestRequest from a dict
start_stress_test_request_from_dict = StartStressTestRequest.from_dict(start_stress_test_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

