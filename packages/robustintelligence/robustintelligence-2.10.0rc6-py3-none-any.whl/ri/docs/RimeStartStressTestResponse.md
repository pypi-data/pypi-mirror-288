# RimeStartStressTestResponse

StartStressTestResponse is a response object returned from the StartStressTest call that contains the job information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job** | [**RimeJobMetadata**](RimeJobMetadata.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_start_stress_test_response import RimeStartStressTestResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeStartStressTestResponse from a JSON string
rime_start_stress_test_response_instance = RimeStartStressTestResponse.from_json(json)
# print the JSON string representation of the object
print(RimeStartStressTestResponse.to_json())

# convert the object into a dict
rime_start_stress_test_response_dict = rime_start_stress_test_response_instance.to_dict()
# create an instance of RimeStartStressTestResponse from a dict
rime_start_stress_test_response_from_dict = RimeStartStressTestResponse.from_dict(rime_start_stress_test_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

