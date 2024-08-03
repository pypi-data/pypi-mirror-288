# ri.apiclient.CustomerManagedKeyServiceApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_customer_managed_key**](CustomerManagedKeyServiceApi.md#create_customer_managed_key) | **POST** /v1-beta/customer-managed-key | CreateCustomerManagedKey
[**delete_customer_managed_key**](CustomerManagedKeyServiceApi.md#delete_customer_managed_key) | **DELETE** /v1-beta/customer-managed-key | DeleteCustomerManagedKey
[**get_customer_managed_key**](CustomerManagedKeyServiceApi.md#get_customer_managed_key) | **GET** /v1-beta/customer-managed-key | GetCustomerManagedKey
[**get_key_status**](CustomerManagedKeyServiceApi.md#get_key_status) | **GET** /v1-beta/customer-managed-key/status | GetKeyStatus


# **create_customer_managed_key**
> RimeCreateCustomerManagedKeyResponse create_customer_managed_key(body)

CreateCustomerManagedKey

Creates a new customer managed key. At most one key can exist per deployment.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_create_customer_managed_key_request import RimeCreateCustomerManagedKeyRequest
from ri.apiclient.models.rime_create_customer_managed_key_response import RimeCreateCustomerManagedKeyResponse
from ri.apiclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https://<platform-domain>.rbst.io
# See configuration.py for a list of all supported configuration parameters.
configuration = ri.apiclient.Configuration(
    host = "http://https://<platform-domain>.rbst.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: rime-api-key
configuration.api_key['rime-api-key'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['rime-api-key'] = 'Bearer'

# Enter a context with an instance of the API client
with ri.apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ri.apiclient.CustomerManagedKeyServiceApi(api_client)
    body = ri.apiclient.RimeCreateCustomerManagedKeyRequest() # RimeCreateCustomerManagedKeyRequest | 

    try:
        # CreateCustomerManagedKey
        api_response = api_instance.create_customer_managed_key(body)
        print("The response of CustomerManagedKeyServiceApi->create_customer_managed_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomerManagedKeyServiceApi->create_customer_managed_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeCreateCustomerManagedKeyRequest**](RimeCreateCustomerManagedKeyRequest.md)|  | 

### Return type

[**RimeCreateCustomerManagedKeyResponse**](RimeCreateCustomerManagedKeyResponse.md)

### Authorization

[rime-api-key](../README.md#rime-api-key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_customer_managed_key**
> object delete_customer_managed_key(cmk_config_kms_key_arn, cmk_config_key_provider=cmk_config_key_provider)

DeleteCustomerManagedKey

Delete the customer managed key.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https://<platform-domain>.rbst.io
# See configuration.py for a list of all supported configuration parameters.
configuration = ri.apiclient.Configuration(
    host = "http://https://<platform-domain>.rbst.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: rime-api-key
configuration.api_key['rime-api-key'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['rime-api-key'] = 'Bearer'

# Enter a context with an instance of the API client
with ri.apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ri.apiclient.CustomerManagedKeyServiceApi(api_client)
    cmk_config_kms_key_arn = 'cmk_config_kms_key_arn_example' # str | The ARN of the AWS KMS key to use as the customer managed key.
    cmk_config_key_provider = 'KEY_PROVIDER_UNSPECIFIED' # str |  - KEY_PROVIDER_AWS_KMS: AWS Key Management Service (optional) (default to 'KEY_PROVIDER_UNSPECIFIED')

    try:
        # DeleteCustomerManagedKey
        api_response = api_instance.delete_customer_managed_key(cmk_config_kms_key_arn, cmk_config_key_provider=cmk_config_key_provider)
        print("The response of CustomerManagedKeyServiceApi->delete_customer_managed_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomerManagedKeyServiceApi->delete_customer_managed_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cmk_config_kms_key_arn** | **str**| The ARN of the AWS KMS key to use as the customer managed key. | 
 **cmk_config_key_provider** | **str**|  - KEY_PROVIDER_AWS_KMS: AWS Key Management Service | [optional] [default to &#39;KEY_PROVIDER_UNSPECIFIED&#39;]

### Return type

**object**

### Authorization

[rime-api-key](../README.md#rime-api-key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_managed_key**
> RimeGetCustomerManagedKeyResponse get_customer_managed_key(cmk_config_kms_key_arn, cmk_config_key_provider=cmk_config_key_provider)

GetCustomerManagedKey

Returns a customer managed key if one has been created.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_customer_managed_key_response import RimeGetCustomerManagedKeyResponse
from ri.apiclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https://<platform-domain>.rbst.io
# See configuration.py for a list of all supported configuration parameters.
configuration = ri.apiclient.Configuration(
    host = "http://https://<platform-domain>.rbst.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: rime-api-key
configuration.api_key['rime-api-key'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['rime-api-key'] = 'Bearer'

# Enter a context with an instance of the API client
with ri.apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ri.apiclient.CustomerManagedKeyServiceApi(api_client)
    cmk_config_kms_key_arn = 'cmk_config_kms_key_arn_example' # str | The ARN of the AWS KMS key to use as the customer managed key.
    cmk_config_key_provider = 'KEY_PROVIDER_UNSPECIFIED' # str |  - KEY_PROVIDER_AWS_KMS: AWS Key Management Service (optional) (default to 'KEY_PROVIDER_UNSPECIFIED')

    try:
        # GetCustomerManagedKey
        api_response = api_instance.get_customer_managed_key(cmk_config_kms_key_arn, cmk_config_key_provider=cmk_config_key_provider)
        print("The response of CustomerManagedKeyServiceApi->get_customer_managed_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomerManagedKeyServiceApi->get_customer_managed_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cmk_config_kms_key_arn** | **str**| The ARN of the AWS KMS key to use as the customer managed key. | 
 **cmk_config_key_provider** | **str**|  - KEY_PROVIDER_AWS_KMS: AWS Key Management Service | [optional] [default to &#39;KEY_PROVIDER_UNSPECIFIED&#39;]

### Return type

[**RimeGetCustomerManagedKeyResponse**](RimeGetCustomerManagedKeyResponse.md)

### Authorization

[rime-api-key](../README.md#rime-api-key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_key_status**
> RimeGetKeyStatusResponse get_key_status()

GetKeyStatus

Return whether the customer managed key is active or revoked.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_key_status_response import RimeGetKeyStatusResponse
from ri.apiclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https://<platform-domain>.rbst.io
# See configuration.py for a list of all supported configuration parameters.
configuration = ri.apiclient.Configuration(
    host = "http://https://<platform-domain>.rbst.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: rime-api-key
configuration.api_key['rime-api-key'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['rime-api-key'] = 'Bearer'

# Enter a context with an instance of the API client
with ri.apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ri.apiclient.CustomerManagedKeyServiceApi(api_client)

    try:
        # GetKeyStatus
        api_response = api_instance.get_key_status()
        print("The response of CustomerManagedKeyServiceApi->get_key_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomerManagedKeyServiceApi->get_key_status: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RimeGetKeyStatusResponse**](RimeGetKeyStatusResponse.md)

### Authorization

[rime-api-key](../README.md#rime-api-key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

