# RimeListEnabledFeaturesResponse

ListEnabledFeaturesResponse contains all enabled features for a customer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**customer_name** | **str** | Tthe customer to retrieve feature flags for. | [optional] 
**enabled_features** | [**List[RimeLicenseFeature]**](RimeLicenseFeature.md) | The set of enabled features. | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_enabled_features_response import RimeListEnabledFeaturesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListEnabledFeaturesResponse from a JSON string
rime_list_enabled_features_response_instance = RimeListEnabledFeaturesResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListEnabledFeaturesResponse.to_json())

# convert the object into a dict
rime_list_enabled_features_response_dict = rime_list_enabled_features_response_instance.to_dict()
# create an instance of RimeListEnabledFeaturesResponse from a dict
rime_list_enabled_features_response_from_dict = RimeListEnabledFeaturesResponse.from_dict(rime_list_enabled_features_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

