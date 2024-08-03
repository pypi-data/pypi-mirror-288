# RimeGetEnabledFeatureResponse

GetEnabledFeatureResponse specifies if a feature is enabled for a customer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature** | [**RimeLicenseFeature**](RimeLicenseFeature.md) |  | [optional] 
**enabled** | **bool** | Whether the feature is enabled. | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_enabled_feature_response import RimeGetEnabledFeatureResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetEnabledFeatureResponse from a JSON string
rime_get_enabled_feature_response_instance = RimeGetEnabledFeatureResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetEnabledFeatureResponse.to_json())

# convert the object into a dict
rime_get_enabled_feature_response_dict = rime_get_enabled_feature_response_instance.to_dict()
# create an instance of RimeGetEnabledFeatureResponse from a dict
rime_get_enabled_feature_response_from_dict = RimeGetEnabledFeatureResponse.from_dict(rime_get_enabled_feature_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

