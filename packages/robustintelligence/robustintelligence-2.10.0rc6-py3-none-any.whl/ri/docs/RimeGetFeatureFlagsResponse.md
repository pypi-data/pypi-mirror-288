# RimeGetFeatureFlagsResponse

GetFeatureFlagsResponse contains the FeatureFlags of a customer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature_flags** | [**RimeFeatureFlags**](RimeFeatureFlags.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_feature_flags_response import RimeGetFeatureFlagsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetFeatureFlagsResponse from a JSON string
rime_get_feature_flags_response_instance = RimeGetFeatureFlagsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetFeatureFlagsResponse.to_json())

# convert the object into a dict
rime_get_feature_flags_response_dict = rime_get_feature_flags_response_instance.to_dict()
# create an instance of RimeGetFeatureFlagsResponse from a dict
rime_get_feature_flags_response_from_dict = RimeGetFeatureFlagsResponse.from_dict(rime_get_feature_flags_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

