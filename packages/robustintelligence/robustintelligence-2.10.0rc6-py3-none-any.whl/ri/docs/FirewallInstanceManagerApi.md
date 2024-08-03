# ri.fwclient.FirewallInstanceManagerApi

All URIs are relative to *http://https://&lt;ai-firewall-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_instance**](FirewallInstanceManagerApi.md#create_instance) | **POST** /v1-beta/firewall-instance | CreateFirewallInstance
[**delete_instance**](FirewallInstanceManagerApi.md#delete_instance) | **DELETE** /v1-beta/firewall-instance/{firewallInstanceId.uuid} | DeleteFirewallInstance
[**get_instance**](FirewallInstanceManagerApi.md#get_instance) | **GET** /v1-beta/firewall-instance/{firewallInstanceId.uuid} | GetFirewallInstance
[**list_instances**](FirewallInstanceManagerApi.md#list_instances) | **GET** /v1-beta/firewall-instance | ListFirewallInstances
[**update_instance**](FirewallInstanceManagerApi.md#update_instance) | **PATCH** /v1-beta/firewall-instance/{firewallInstance.firewallInstanceId.uuid} | UpdateFirewallInstance


# **create_instance**
> GenerativefirewallCreateFirewallInstanceResponse create_instance(body)

CreateFirewallInstance

This creates a new Firewall Instance with the desired user configuration. It will take time for the new instance to become available; use the `GetFirewallInstance` API to track the status of the deployment.

### Example

* Api Key Authentication (X-Firewall-Auth-Token):

```python
import ri.fwclient
from ri.fwclient.models.generativefirewall_create_firewall_instance_request import GenerativefirewallCreateFirewallInstanceRequest
from ri.fwclient.models.generativefirewall_create_firewall_instance_response import GenerativefirewallCreateFirewallInstanceResponse
from ri.fwclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https://<ai-firewall-domain>.rbst.io
# See configuration.py for a list of all supported configuration parameters.
configuration = ri.fwclient.Configuration(
    host = "http://https://<ai-firewall-domain>.rbst.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: X-Firewall-Auth-Token
configuration.api_key['X-Firewall-Auth-Token'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-Firewall-Auth-Token'] = 'Bearer'

# Enter a context with an instance of the API client
with ri.fwclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ri.fwclient.FirewallInstanceManagerApi(api_client)
    body = ri.fwclient.GenerativefirewallCreateFirewallInstanceRequest() # GenerativefirewallCreateFirewallInstanceRequest | 

    try:
        # CreateFirewallInstance
        api_response = api_instance.create_instance(body)
        print("The response of FirewallInstanceManagerApi->create_instance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallInstanceManagerApi->create_instance: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GenerativefirewallCreateFirewallInstanceRequest**](GenerativefirewallCreateFirewallInstanceRequest.md)|  | 

### Return type

[**GenerativefirewallCreateFirewallInstanceResponse**](GenerativefirewallCreateFirewallInstanceResponse.md)

### Authorization

[X-Firewall-Auth-Token](../README.md#X-Firewall-Auth-Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_instance**
> object delete_instance(firewall_instance_id_uuid)

DeleteFirewallInstance

This hard-deletes a Firewall Instance from the cluster. Be careful with this API because it will interrupt in-flight validation.

### Example

* Api Key Authentication (X-Firewall-Auth-Token):

```python
import ri.fwclient
from ri.fwclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https://<ai-firewall-domain>.rbst.io
# See configuration.py for a list of all supported configuration parameters.
configuration = ri.fwclient.Configuration(
    host = "http://https://<ai-firewall-domain>.rbst.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: X-Firewall-Auth-Token
configuration.api_key['X-Firewall-Auth-Token'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-Firewall-Auth-Token'] = 'Bearer'

# Enter a context with an instance of the API client
with ri.fwclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ri.fwclient.FirewallInstanceManagerApi(api_client)
    firewall_instance_id_uuid = 'firewall_instance_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteFirewallInstance
        api_response = api_instance.delete_instance(firewall_instance_id_uuid)
        print("The response of FirewallInstanceManagerApi->delete_instance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallInstanceManagerApi->delete_instance: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_instance_id_uuid** | **str**| Unique object ID. | 

### Return type

**object**

### Authorization

[X-Firewall-Auth-Token](../README.md#X-Firewall-Auth-Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_instance**
> GenerativefirewallGetFirewallInstanceResponse get_instance(firewall_instance_id_uuid)

GetFirewallInstance

This retrieves information about a single Firewall Instance.

### Example

* Api Key Authentication (X-Firewall-Auth-Token):

```python
import ri.fwclient
from ri.fwclient.models.generativefirewall_get_firewall_instance_response import GenerativefirewallGetFirewallInstanceResponse
from ri.fwclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https://<ai-firewall-domain>.rbst.io
# See configuration.py for a list of all supported configuration parameters.
configuration = ri.fwclient.Configuration(
    host = "http://https://<ai-firewall-domain>.rbst.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: X-Firewall-Auth-Token
configuration.api_key['X-Firewall-Auth-Token'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-Firewall-Auth-Token'] = 'Bearer'

# Enter a context with an instance of the API client
with ri.fwclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ri.fwclient.FirewallInstanceManagerApi(api_client)
    firewall_instance_id_uuid = 'firewall_instance_id_uuid_example' # str | Unique object ID.

    try:
        # GetFirewallInstance
        api_response = api_instance.get_instance(firewall_instance_id_uuid)
        print("The response of FirewallInstanceManagerApi->get_instance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallInstanceManagerApi->get_instance: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_instance_id_uuid** | **str**| Unique object ID. | 

### Return type

[**GenerativefirewallGetFirewallInstanceResponse**](GenerativefirewallGetFirewallInstanceResponse.md)

### Authorization

[X-Firewall-Auth-Token](../README.md#X-Firewall-Auth-Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_instances**
> GenerativefirewallListFirewallInstancesResponse list_instances()

ListFirewallInstances

This lists the Firewall Instances on the cluster.

### Example

* Api Key Authentication (X-Firewall-Auth-Token):

```python
import ri.fwclient
from ri.fwclient.models.generativefirewall_list_firewall_instances_response import GenerativefirewallListFirewallInstancesResponse
from ri.fwclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https://<ai-firewall-domain>.rbst.io
# See configuration.py for a list of all supported configuration parameters.
configuration = ri.fwclient.Configuration(
    host = "http://https://<ai-firewall-domain>.rbst.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: X-Firewall-Auth-Token
configuration.api_key['X-Firewall-Auth-Token'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-Firewall-Auth-Token'] = 'Bearer'

# Enter a context with an instance of the API client
with ri.fwclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ri.fwclient.FirewallInstanceManagerApi(api_client)

    try:
        # ListFirewallInstances
        api_response = api_instance.list_instances()
        print("The response of FirewallInstanceManagerApi->list_instances:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallInstanceManagerApi->list_instances: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GenerativefirewallListFirewallInstancesResponse**](GenerativefirewallListFirewallInstancesResponse.md)

### Authorization

[X-Firewall-Auth-Token](../README.md#X-Firewall-Auth-Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_instance**
> GenerativefirewallUpdateFirewallInstanceResponse update_instance(firewall_instance_firewall_instance_id_uuid, firewall_instance, mask=mask)

UpdateFirewallInstance

Update an existing FirewallInstance. This redeploys the firewall instance. The status will be REDEPLOYING until the new version of the firewall instance reaches READY.

### Example

* Api Key Authentication (X-Firewall-Auth-Token):

```python
import ri.fwclient
from ri.fwclient.models.generativefirewall_update_firewall_instance_response import GenerativefirewallUpdateFirewallInstanceResponse
from ri.fwclient.models.update_instance_request import UpdateInstanceRequest
from ri.fwclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https://<ai-firewall-domain>.rbst.io
# See configuration.py for a list of all supported configuration parameters.
configuration = ri.fwclient.Configuration(
    host = "http://https://<ai-firewall-domain>.rbst.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: X-Firewall-Auth-Token
configuration.api_key['X-Firewall-Auth-Token'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-Firewall-Auth-Token'] = 'Bearer'

# Enter a context with an instance of the API client
with ri.fwclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ri.fwclient.FirewallInstanceManagerApi(api_client)
    firewall_instance_firewall_instance_id_uuid = 'firewall_instance_firewall_instance_id_uuid_example' # str | Unique object ID.
    firewall_instance = ri.fwclient.UpdateInstanceRequest() # UpdateInstanceRequest | 
    mask = 'mask_example' # str |  (optional)

    try:
        # UpdateFirewallInstance
        api_response = api_instance.update_instance(firewall_instance_firewall_instance_id_uuid, firewall_instance, mask=mask)
        print("The response of FirewallInstanceManagerApi->update_instance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallInstanceManagerApi->update_instance: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_instance_firewall_instance_id_uuid** | **str**| Unique object ID. | 
 **firewall_instance** | [**UpdateInstanceRequest**](UpdateInstanceRequest.md)|  | 
 **mask** | **str**|  | [optional] 

### Return type

[**GenerativefirewallUpdateFirewallInstanceResponse**](GenerativefirewallUpdateFirewallInstanceResponse.md)

### Authorization

[X-Firewall-Auth-Token](../README.md#X-Firewall-Auth-Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

