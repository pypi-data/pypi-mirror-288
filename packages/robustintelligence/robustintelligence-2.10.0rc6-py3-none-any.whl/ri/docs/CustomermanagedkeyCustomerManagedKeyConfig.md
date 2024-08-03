# CustomermanagedkeyCustomerManagedKeyConfig

CustomerManagedKeyConfig specifies the configuration of a customer managed key. This config contains the key provider and the resource identifier of the key.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key_provider** | [**CustomermanagedkeyKeyProvider**](CustomermanagedkeyKeyProvider.md) |  | [optional] 
**kms_key_arn** | **str** | The ARN of the AWS KMS key to use as the customer managed key. | 

## Example

```python
from ri.apiclient.models.customermanagedkey_customer_managed_key_config import CustomermanagedkeyCustomerManagedKeyConfig

# TODO update the JSON string below
json = "{}"
# create an instance of CustomermanagedkeyCustomerManagedKeyConfig from a JSON string
customermanagedkey_customer_managed_key_config_instance = CustomermanagedkeyCustomerManagedKeyConfig.from_json(json)
# print the JSON string representation of the object
print(CustomermanagedkeyCustomerManagedKeyConfig.to_json())

# convert the object into a dict
customermanagedkey_customer_managed_key_config_dict = customermanagedkey_customer_managed_key_config_instance.to_dict()
# create an instance of CustomermanagedkeyCustomerManagedKeyConfig from a dict
customermanagedkey_customer_managed_key_config_from_dict = CustomermanagedkeyCustomerManagedKeyConfig.from_dict(customermanagedkey_customer_managed_key_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

