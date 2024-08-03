# RimeStartContinuousTestResponse

StartContinuousTestResponse is the response object returned from StartContinuousTest that contains the job info.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job** | [**RimeJobMetadata**](RimeJobMetadata.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_start_continuous_test_response import RimeStartContinuousTestResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeStartContinuousTestResponse from a JSON string
rime_start_continuous_test_response_instance = RimeStartContinuousTestResponse.from_json(json)
# print the JSON string representation of the object
print(RimeStartContinuousTestResponse.to_json())

# convert the object into a dict
rime_start_continuous_test_response_dict = rime_start_continuous_test_response_instance.to_dict()
# create an instance of RimeStartContinuousTestResponse from a dict
rime_start_continuous_test_response_from_dict = RimeStartContinuousTestResponse.from_dict(rime_start_continuous_test_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

