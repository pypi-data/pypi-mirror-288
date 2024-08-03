# RimeUserWriteMask

Mask for user fields to update.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**full_name** | **bool** | Specifies whether to update the full name of the user. | [optional] 
**show_tutorial** | **bool** | Specifies whether to update the tutorial status of the user. | [optional] 
**role** | **bool** | Specifies whether to update the role of the user. | [optional] 
**org_role** | **bool** | Specifies whether to update the organization role of the user. | [optional] 
**private_info** | **bool** | Specifies whether to update the private fields of the user. | [optional] 

## Example

```python
from ri.apiclient.models.rime_user_write_mask import RimeUserWriteMask

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUserWriteMask from a JSON string
rime_user_write_mask_instance = RimeUserWriteMask.from_json(json)
# print the JSON string representation of the object
print(RimeUserWriteMask.to_json())

# convert the object into a dict
rime_user_write_mask_dict = rime_user_write_mask_instance.to_dict()
# create an instance of RimeUserWriteMask from a dict
rime_user_write_mask_from_dict = RimeUserWriteMask.from_dict(rime_user_write_mask_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

