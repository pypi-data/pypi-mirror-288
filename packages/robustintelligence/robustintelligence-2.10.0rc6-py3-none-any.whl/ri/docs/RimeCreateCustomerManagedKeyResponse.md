# RimeCreateCustomerManagedKeyResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cmk_config** | [**CustomermanagedkeyCustomerManagedKeyConfig**](CustomermanagedkeyCustomerManagedKeyConfig.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_customer_managed_key_response import RimeCreateCustomerManagedKeyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateCustomerManagedKeyResponse from a JSON string
rime_create_customer_managed_key_response_instance = RimeCreateCustomerManagedKeyResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateCustomerManagedKeyResponse.to_json())

# convert the object into a dict
rime_create_customer_managed_key_response_dict = rime_create_customer_managed_key_response_instance.to_dict()
# create an instance of RimeCreateCustomerManagedKeyResponse from a dict
rime_create_customer_managed_key_response_from_dict = RimeCreateCustomerManagedKeyResponse.from_dict(rime_create_customer_managed_key_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

