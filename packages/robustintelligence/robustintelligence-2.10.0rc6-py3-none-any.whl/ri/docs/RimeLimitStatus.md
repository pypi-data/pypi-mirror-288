# RimeLimitStatus

LimitStatus contains the status of a limit in this deployment's license.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**limit** | [**RimeLicenseLimit**](RimeLicenseLimit.md) |  | [optional] 
**limit_status** | [**RimeLimitStatusStatus**](RimeLimitStatusStatus.md) |  | [optional] 
**limit_value** | **str** |  | [optional] 
**current_value** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_limit_status import RimeLimitStatus

# TODO update the JSON string below
json = "{}"
# create an instance of RimeLimitStatus from a JSON string
rime_limit_status_instance = RimeLimitStatus.from_json(json)
# print the JSON string representation of the object
print(RimeLimitStatus.to_json())

# convert the object into a dict
rime_limit_status_dict = rime_limit_status_instance.to_dict()
# create an instance of RimeLimitStatus from a dict
rime_limit_status_from_dict = RimeLimitStatus.from_dict(rime_limit_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

