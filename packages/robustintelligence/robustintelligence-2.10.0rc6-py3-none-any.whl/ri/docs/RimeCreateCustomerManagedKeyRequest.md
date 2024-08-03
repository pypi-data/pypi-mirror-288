# RimeCreateCustomerManagedKeyRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cmk_config** | [**CustomermanagedkeyCustomerManagedKeyConfig**](CustomermanagedkeyCustomerManagedKeyConfig.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_customer_managed_key_request import RimeCreateCustomerManagedKeyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateCustomerManagedKeyRequest from a JSON string
rime_create_customer_managed_key_request_instance = RimeCreateCustomerManagedKeyRequest.from_json(json)
# print the JSON string representation of the object
print(RimeCreateCustomerManagedKeyRequest.to_json())

# convert the object into a dict
rime_create_customer_managed_key_request_dict = rime_create_customer_managed_key_request_instance.to_dict()
# create an instance of RimeCreateCustomerManagedKeyRequest from a dict
rime_create_customer_managed_key_request_from_dict = RimeCreateCustomerManagedKeyRequest.from_dict(rime_create_customer_managed_key_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

