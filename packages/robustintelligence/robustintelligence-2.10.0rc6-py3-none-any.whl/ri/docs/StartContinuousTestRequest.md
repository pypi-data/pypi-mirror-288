# StartContinuousTestRequest

StartContinuousTestRequest is the request object containing the firewall information and the configurations for the Continuous Test.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_id** | **object** | Uniquely specifies a Firewall. | [optional] 
**test_run_incremental_config** | [**TestrunTestRunIncrementalConfig**](TestrunTestRunIncrementalConfig.md) |  | [optional] 
**override_existing_bins** | **bool** |  | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**experimental_fields** | **Dict[str, object]** | Fields that enable experimental functionality.  WARNING: these fields are experimental; ie, their functionality may not be reliable or backwards-compatible. Do not use these fields in production. | [optional] 

## Example

```python
from ri.apiclient.models.start_continuous_test_request import StartContinuousTestRequest

# TODO update the JSON string below
json = "{}"
# create an instance of StartContinuousTestRequest from a JSON string
start_continuous_test_request_instance = StartContinuousTestRequest.from_json(json)
# print the JSON string representation of the object
print(StartContinuousTestRequest.to_json())

# convert the object into a dict
start_continuous_test_request_dict = start_continuous_test_request_instance.to_dict()
# create an instance of StartContinuousTestRequest from a dict
start_continuous_test_request_from_dict = StartContinuousTestRequest.from_dict(start_continuous_test_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

