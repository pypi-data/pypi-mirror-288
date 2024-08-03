# RimeGetCustomerManagedKeyResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cmk_config** | [**CustomermanagedkeyCustomerManagedKeyConfig**](CustomermanagedkeyCustomerManagedKeyConfig.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_customer_managed_key_response import RimeGetCustomerManagedKeyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetCustomerManagedKeyResponse from a JSON string
rime_get_customer_managed_key_response_instance = RimeGetCustomerManagedKeyResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetCustomerManagedKeyResponse.to_json())

# convert the object into a dict
rime_get_customer_managed_key_response_dict = rime_get_customer_managed_key_response_instance.to_dict()
# create an instance of RimeGetCustomerManagedKeyResponse from a dict
rime_get_customer_managed_key_response_from_dict = RimeGetCustomerManagedKeyResponse.from_dict(rime_get_customer_managed_key_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

