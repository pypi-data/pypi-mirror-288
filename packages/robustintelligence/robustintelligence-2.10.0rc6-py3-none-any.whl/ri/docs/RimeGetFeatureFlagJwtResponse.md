# RimeGetFeatureFlagJwtResponse

GetFeatureFlagJwtResponse is the response to get the Feature Flag JWT token that returns the signed JWT token of the customer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**signed_jwt_token_str** | **str** | The signed JWT token of the customer. | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_feature_flag_jwt_response import RimeGetFeatureFlagJwtResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetFeatureFlagJwtResponse from a JSON string
rime_get_feature_flag_jwt_response_instance = RimeGetFeatureFlagJwtResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetFeatureFlagJwtResponse.to_json())

# convert the object into a dict
rime_get_feature_flag_jwt_response_dict = rime_get_feature_flag_jwt_response_instance.to_dict()
# create an instance of RimeGetFeatureFlagJwtResponse from a dict
rime_get_feature_flag_jwt_response_from_dict = RimeGetFeatureFlagJwtResponse.from_dict(rime_get_feature_flag_jwt_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

