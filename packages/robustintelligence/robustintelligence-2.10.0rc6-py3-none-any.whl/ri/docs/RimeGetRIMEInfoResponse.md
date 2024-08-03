# RimeGetRIMEInfoResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cluster_info_version** | **str** | Version of the Robust Intelligence cluster control plane. | [optional] 
**customer_name** | **str** | Name of the customer who owns the license. | [optional] 
**expiration_time** | **datetime** | Expiration time of the license. | [optional] 
**grace_period_end_time** | **datetime** | After a license is expired, there is a grace period to allow a user to continue to use and update the license. | [optional] 
**ri_plan** | [**RimeRIPlan**](RimeRIPlan.md) |  | [optional] 
**build_version** | **str** | Annotated version of the Robust Intelligence cluster control plane, including the timestamp corresponding to the build. | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_rime_info_response import RimeGetRIMEInfoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetRIMEInfoResponse from a JSON string
rime_get_rime_info_response_instance = RimeGetRIMEInfoResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetRIMEInfoResponse.to_json())

# convert the object into a dict
rime_get_rime_info_response_dict = rime_get_rime_info_response_instance.to_dict()
# create an instance of RimeGetRIMEInfoResponse from a dict
rime_get_rime_info_response_from_dict = RimeGetRIMEInfoResponse.from_dict(rime_get_rime_info_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

