# ri.apiclient.IntegrationServiceApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**configure_integration**](IntegrationServiceApi.md#configure_integration) | **POST** /v1-beta/integrations/{integrationId.uuid} | ConfigureIntegration
[**create_integration**](IntegrationServiceApi.md#create_integration) | **POST** /v1-beta/integrations | CreateIntegration
[**delete_integration**](IntegrationServiceApi.md#delete_integration) | **DELETE** /v1-beta/integrations/{integrationId.uuid} | DeleteIntegration
[**get_integration**](IntegrationServiceApi.md#get_integration) | **GET** /v1-beta/integrations/{integrationId.uuid} | GetIntegration
[**list_workspace_integrations**](IntegrationServiceApi.md#list_workspace_integrations) | **GET** /v1-beta/integrations/workspace/{workspaceId.uuid} | ListWorkspaceIntegrations
[**update_integration**](IntegrationServiceApi.md#update_integration) | **PUT** /v1-beta/integrations/{integration.id.uuid} | UpdateIntegration


# **configure_integration**
> RimeConfigureIntegrationResponse configure_integration(integration_id_uuid, body)

ConfigureIntegration

Configures the Integration with specified ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.configure_integration_request import ConfigureIntegrationRequest
from ri.apiclient.models.rime_configure_integration_response import RimeConfigureIntegrationResponse
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
    api_instance = ri.apiclient.IntegrationServiceApi(api_client)
    integration_id_uuid = 'integration_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.ConfigureIntegrationRequest() # ConfigureIntegrationRequest | 

    try:
        # ConfigureIntegration
        api_response = api_instance.configure_integration(integration_id_uuid, body)
        print("The response of IntegrationServiceApi->configure_integration:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IntegrationServiceApi->configure_integration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **integration_id_uuid** | **str**| Unique object ID. | 
 **body** | [**ConfigureIntegrationRequest**](ConfigureIntegrationRequest.md)|  | 

### Return type

[**RimeConfigureIntegrationResponse**](RimeConfigureIntegrationResponse.md)

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

# **create_integration**
> RimeCreateIntegrationResponse create_integration(body)

CreateIntegration

Creates a new Integration.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_create_integration_request import RimeCreateIntegrationRequest
from ri.apiclient.models.rime_create_integration_response import RimeCreateIntegrationResponse
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
    api_instance = ri.apiclient.IntegrationServiceApi(api_client)
    body = ri.apiclient.RimeCreateIntegrationRequest() # RimeCreateIntegrationRequest | 

    try:
        # CreateIntegration
        api_response = api_instance.create_integration(body)
        print("The response of IntegrationServiceApi->create_integration:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IntegrationServiceApi->create_integration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeCreateIntegrationRequest**](RimeCreateIntegrationRequest.md)|  | 

### Return type

[**RimeCreateIntegrationResponse**](RimeCreateIntegrationResponse.md)

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

# **delete_integration**
> object delete_integration(integration_id_uuid)

DeleteIntegration

Delete an Integration by specified ID.

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
    api_instance = ri.apiclient.IntegrationServiceApi(api_client)
    integration_id_uuid = 'integration_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteIntegration
        api_response = api_instance.delete_integration(integration_id_uuid)
        print("The response of IntegrationServiceApi->delete_integration:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IntegrationServiceApi->delete_integration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **integration_id_uuid** | **str**| Unique object ID. | 

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

# **get_integration**
> RimeGetIntegrationResponse get_integration(integration_id_uuid)

GetIntegration

Returns an Integration by specified ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_integration_response import RimeGetIntegrationResponse
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
    api_instance = ri.apiclient.IntegrationServiceApi(api_client)
    integration_id_uuid = 'integration_id_uuid_example' # str | Unique object ID.

    try:
        # GetIntegration
        api_response = api_instance.get_integration(integration_id_uuid)
        print("The response of IntegrationServiceApi->get_integration:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IntegrationServiceApi->get_integration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **integration_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeGetIntegrationResponse**](RimeGetIntegrationResponse.md)

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

# **list_workspace_integrations**
> RimeListWorkspaceIntegrationsResponse list_workspace_integrations(workspace_id_uuid)

ListWorkspaceIntegrations

List all Integrations for the Workspace with specified ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_workspace_integrations_response import RimeListWorkspaceIntegrationsResponse
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
    api_instance = ri.apiclient.IntegrationServiceApi(api_client)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID.

    try:
        # ListWorkspaceIntegrations
        api_response = api_instance.list_workspace_integrations(workspace_id_uuid)
        print("The response of IntegrationServiceApi->list_workspace_integrations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IntegrationServiceApi->list_workspace_integrations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeListWorkspaceIntegrationsResponse**](RimeListWorkspaceIntegrationsResponse.md)

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

# **update_integration**
> RimeUpdateIntegrationResponse update_integration(integration_id_uuid, body)

UpdateIntegration

Update the Integration with specified ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_update_integration_response import RimeUpdateIntegrationResponse
from ri.apiclient.models.update_integration_request import UpdateIntegrationRequest
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
    api_instance = ri.apiclient.IntegrationServiceApi(api_client)
    integration_id_uuid = 'integration_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.UpdateIntegrationRequest() # UpdateIntegrationRequest | 

    try:
        # UpdateIntegration
        api_response = api_instance.update_integration(integration_id_uuid, body)
        print("The response of IntegrationServiceApi->update_integration:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IntegrationServiceApi->update_integration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **integration_id_uuid** | **str**| Unique object ID. | 
 **body** | [**UpdateIntegrationRequest**](UpdateIntegrationRequest.md)|  | 

### Return type

[**RimeUpdateIntegrationResponse**](RimeUpdateIntegrationResponse.md)

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

