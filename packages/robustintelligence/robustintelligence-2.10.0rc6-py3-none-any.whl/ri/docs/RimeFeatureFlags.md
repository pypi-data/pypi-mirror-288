# RimeFeatureFlags

FeatureFlags defines all maintained flags/toggles. In DB storage, these are encoded in a JWT token to guarantee authenticity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**customer_name** | **str** | Customer Name. We maintain 1 set per customer. We need this for multi-tenancy (N customers in 1 cluster). | [optional] 
**subscription_expiration_time** | **datetime** | Subscription time. | [optional] 
**upload_size_bytes** | **str** | Upload data size. | [optional] 
**enable_model_cards** | **bool** | Compliance model cards feature. | [optional] 

## Example

```python
from ri.apiclient.models.rime_feature_flags import RimeFeatureFlags

# TODO update the JSON string below
json = "{}"
# create an instance of RimeFeatureFlags from a JSON string
rime_feature_flags_instance = RimeFeatureFlags.from_json(json)
# print the JSON string representation of the object
print(RimeFeatureFlags.to_json())

# convert the object into a dict
rime_feature_flags_dict = rime_feature_flags_instance.to_dict()
# create an instance of RimeFeatureFlags from a dict
rime_feature_flags_from_dict = RimeFeatureFlags.from_dict(rime_feature_flags_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

