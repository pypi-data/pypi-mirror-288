# ri.apiclient.FirewallServiceApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**firewall_service_create_firewall**](FirewallServiceApi.md#firewall_service_create_firewall) | **POST** /v1/firewall | CreateFirewall
[**firewall_service_delete_firewall**](FirewallServiceApi.md#firewall_service_delete_firewall) | **DELETE** /v1/firewall/{firewallId.uuid} | DeleteFirewall
[**firewall_service_get_firewall**](FirewallServiceApi.md#firewall_service_get_firewall) | **GET** /v1/firewall/{firewallId.uuid} | GetFirewall
[**firewall_service_get_url**](FirewallServiceApi.md#firewall_service_get_url) | **GET** /v1-beta/firewall/{firewallId.uuid}/url | GetURL
[**firewall_service_update_firewall**](FirewallServiceApi.md#firewall_service_update_firewall) | **PUT** /v1/firewall/{firewall.firewallId.uuid} | UpdateFirewall


# **firewall_service_create_firewall**
> RimeCreateFirewallResponse firewall_service_create_firewall(body)

CreateFirewall

Creates a firewall with the required fields. This service is deprecated in Robust Intelligence v2.2 and will not be supported from v2.4.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_create_firewall_request import RimeCreateFirewallRequest
from ri.apiclient.models.rime_create_firewall_response import RimeCreateFirewallResponse
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
    api_instance = ri.apiclient.FirewallServiceApi(api_client)
    body = ri.apiclient.RimeCreateFirewallRequest() # RimeCreateFirewallRequest | 

    try:
        # CreateFirewall
        api_response = api_instance.firewall_service_create_firewall(body)
        print("The response of FirewallServiceApi->firewall_service_create_firewall:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallServiceApi->firewall_service_create_firewall: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeCreateFirewallRequest**](RimeCreateFirewallRequest.md)|  | 

### Return type

[**RimeCreateFirewallResponse**](RimeCreateFirewallResponse.md)

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

# **firewall_service_delete_firewall**
> object firewall_service_delete_firewall(firewall_id_uuid)

DeleteFirewall

Deletes the firewall with the specified ID. This service is deprecated in Robust Intelligence v2.2 and will not be supported from v2.4.

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
    api_instance = ri.apiclient.FirewallServiceApi(api_client)
    firewall_id_uuid = 'firewall_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteFirewall
        api_response = api_instance.firewall_service_delete_firewall(firewall_id_uuid)
        print("The response of FirewallServiceApi->firewall_service_delete_firewall:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallServiceApi->firewall_service_delete_firewall: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_id_uuid** | **str**| Unique object ID. | 

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

# **firewall_service_get_firewall**
> RimeGetFirewallResponse firewall_service_get_firewall(firewall_id_uuid)

GetFirewall

Gets the firewall that matches the specified ID. This service is deprecated in Robust Intelligence v2.2 and will not be supported from v2.4.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_firewall_response import RimeGetFirewallResponse
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
    api_instance = ri.apiclient.FirewallServiceApi(api_client)
    firewall_id_uuid = 'firewall_id_uuid_example' # str | Unique object ID.

    try:
        # GetFirewall
        api_response = api_instance.firewall_service_get_firewall(firewall_id_uuid)
        print("The response of FirewallServiceApi->firewall_service_get_firewall:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallServiceApi->firewall_service_get_firewall: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeGetFirewallResponse**](RimeGetFirewallResponse.md)

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

# **firewall_service_get_url**
> RimeGetURLResponse firewall_service_get_url(firewall_id_uuid)

GetURL

Returns the URL for the specified Firewall in the Robust Intelligence web application. This service is deprecated in Robust Intelligence v2.2 and will not be supported from v2.4.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_url_response import RimeGetURLResponse
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
    api_instance = ri.apiclient.FirewallServiceApi(api_client)
    firewall_id_uuid = 'firewall_id_uuid_example' # str | Unique object ID.

    try:
        # GetURL
        api_response = api_instance.firewall_service_get_url(firewall_id_uuid)
        print("The response of FirewallServiceApi->firewall_service_get_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallServiceApi->firewall_service_get_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeGetURLResponse**](RimeGetURLResponse.md)

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

# **firewall_service_update_firewall**
> RimeUpdateFirewallResponse firewall_service_update_firewall(firewall_firewall_id_uuid, body)

UpdateFirewall

Updates a firewall's editable fields. This service is deprecated in Robust Intelligence v2.2 and will not be supported from v2.4.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.firewall_service_update_firewall_request import FirewallServiceUpdateFirewallRequest
from ri.apiclient.models.rime_update_firewall_response import RimeUpdateFirewallResponse
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
    api_instance = ri.apiclient.FirewallServiceApi(api_client)
    firewall_firewall_id_uuid = 'firewall_firewall_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.FirewallServiceUpdateFirewallRequest() # FirewallServiceUpdateFirewallRequest | 

    try:
        # UpdateFirewall
        api_response = api_instance.firewall_service_update_firewall(firewall_firewall_id_uuid, body)
        print("The response of FirewallServiceApi->firewall_service_update_firewall:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallServiceApi->firewall_service_update_firewall: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_firewall_id_uuid** | **str**| Unique object ID. | 
 **body** | [**FirewallServiceUpdateFirewallRequest**](FirewallServiceUpdateFirewallRequest.md)|  | 

### Return type

[**RimeUpdateFirewallResponse**](RimeUpdateFirewallResponse.md)

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

