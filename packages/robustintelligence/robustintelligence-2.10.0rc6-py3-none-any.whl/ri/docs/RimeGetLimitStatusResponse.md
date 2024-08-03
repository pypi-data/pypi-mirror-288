# RimeGetLimitStatusResponse

GetLimitStatusResponse contains the limit status of a requested limit for a customer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**limit_status** | [**RimeLimitStatus**](RimeLimitStatus.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_limit_status_response import RimeGetLimitStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetLimitStatusResponse from a JSON string
rime_get_limit_status_response_instance = RimeGetLimitStatusResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetLimitStatusResponse.to_json())

# convert the object into a dict
rime_get_limit_status_response_dict = rime_get_limit_status_response_instance.to_dict()
# create an instance of RimeGetLimitStatusResponse from a dict
rime_get_limit_status_response_from_dict = RimeGetLimitStatusResponse.from_dict(rime_get_limit_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

