# ri.apiclient.FeatureFlagApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_limit_status**](FeatureFlagApi.md#get_limit_status) | **GET** /v1/feature-flags/{customerName}/limits/{limit} | GetLimitStatus
[**list_enabled_features**](FeatureFlagApi.md#list_enabled_features) | **GET** /v1/feature-flags/{customerName}/features | ListEnabledFeatures


# **get_limit_status**
> RimeGetLimitStatusResponse get_limit_status(customer_name, limit)

GetLimitStatus

Returns the status of a specified limit in this deployment's license.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_limit_status_response import RimeGetLimitStatusResponse
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
    api_instance = ri.apiclient.FeatureFlagApi(api_client)
    customer_name = 'customer_name_example' # str | Name of the customer to query.
    limit = 'limit_example' # str | Specifies which limit to query.

    try:
        # GetLimitStatus
        api_response = api_instance.get_limit_status(customer_name, limit)
        print("The response of FeatureFlagApi->get_limit_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeatureFlagApi->get_limit_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_name** | **str**| Name of the customer to query. | 
 **limit** | **str**| Specifies which limit to query. | 

### Return type

[**RimeGetLimitStatusResponse**](RimeGetLimitStatusResponse.md)

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

# **list_enabled_features**
> RimeListEnabledFeaturesResponse list_enabled_features(customer_name)

ListEnabledFeatures

Returns all features enabled in license for a customer.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_enabled_features_response import RimeListEnabledFeaturesResponse
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
    api_instance = ri.apiclient.FeatureFlagApi(api_client)
    customer_name = 'customer_name_example' # str | Name of the customer to query.

    try:
        # ListEnabledFeatures
        api_response = api_instance.list_enabled_features(customer_name)
        print("The response of FeatureFlagApi->list_enabled_features:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeatureFlagApi->list_enabled_features: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_name** | **str**| Name of the customer to query. | 

### Return type

[**RimeListEnabledFeaturesResponse**](RimeListEnabledFeaturesResponse.md)

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

