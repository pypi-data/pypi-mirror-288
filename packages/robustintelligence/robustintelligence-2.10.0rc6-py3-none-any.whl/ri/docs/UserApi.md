# ri.apiclient.UserApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_api_token**](UserApi.md#create_api_token) | **POST** /v1/users/api-tokens | CreateAPIToken
[**create_user**](UserApi.md#create_user) | **POST** /v1/users | CreateUser
[**delete_api_token**](UserApi.md#delete_api_token) | **DELETE** /v1/users/api-tokens/{id.uuid} | DeleteAPIToken
[**delete_user**](UserApi.md#delete_user) | **DELETE** /v1/users/{userId.uuid} | DeleteUser
[**get_user**](UserApi.md#get_user) | **GET** /v1/users/{userId.uuid} | GetUser
[**list_api_tokens**](UserApi.md#list_api_tokens) | **GET** /v1/users/api-tokens | ListAPITokens
[**list_current_user_roles**](UserApi.md#list_current_user_roles) | **GET** /v1/users/roles | ListCurrentUserRoles
[**list_users**](UserApi.md#list_users) | **GET** /v1/users | ListUsers
[**reset_password**](UserApi.md#reset_password) | **POST** /v1/users/reset-password/{userId.uuid} | ResetPassword
[**update_agent_api_token**](UserApi.md#update_agent_api_token) | **PUT** /v1/users/agent-api-tokens | UpdateAgentAPIToken
[**update_user**](UserApi.md#update_user) | **PUT** /v1/users/{user.id.uuid} | UpdateUser


# **create_api_token**
> RimeCreateAPITokenResponse create_api_token(body)

CreateAPIToken

Create a new API token.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_create_api_token_request import RimeCreateAPITokenRequest
from ri.apiclient.models.rime_create_api_token_response import RimeCreateAPITokenResponse
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
    api_instance = ri.apiclient.UserApi(api_client)
    body = ri.apiclient.RimeCreateAPITokenRequest() # RimeCreateAPITokenRequest | 

    try:
        # CreateAPIToken
        api_response = api_instance.create_api_token(body)
        print("The response of UserApi->create_api_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->create_api_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeCreateAPITokenRequest**](RimeCreateAPITokenRequest.md)|  | 

### Return type

[**RimeCreateAPITokenResponse**](RimeCreateAPITokenResponse.md)

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

# **create_user**
> RimeCreateUserResponse create_user(body)

CreateUser

Creates a user.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_create_user_request import RimeCreateUserRequest
from ri.apiclient.models.rime_create_user_response import RimeCreateUserResponse
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
    api_instance = ri.apiclient.UserApi(api_client)
    body = ri.apiclient.RimeCreateUserRequest() # RimeCreateUserRequest | 

    try:
        # CreateUser
        api_response = api_instance.create_user(body)
        print("The response of UserApi->create_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->create_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeCreateUserRequest**](RimeCreateUserRequest.md)|  | 

### Return type

[**RimeCreateUserResponse**](RimeCreateUserResponse.md)

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

# **delete_api_token**
> object delete_api_token(id_uuid)

DeleteAPIToken

Delete an API token by ID.

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
    api_instance = ri.apiclient.UserApi(api_client)
    id_uuid = 'id_uuid_example' # str | Unique object ID.

    try:
        # DeleteAPIToken
        api_response = api_instance.delete_api_token(id_uuid)
        print("The response of UserApi->delete_api_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->delete_api_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_uuid** | **str**| Unique object ID. | 

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

# **delete_user**
> object delete_user(user_id_uuid)

DeleteUser

Delete the user with the specified ID.

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
    api_instance = ri.apiclient.UserApi(api_client)
    user_id_uuid = 'user_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteUser
        api_response = api_instance.delete_user(user_id_uuid)
        print("The response of UserApi->delete_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->delete_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id_uuid** | **str**| Unique object ID. | 

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

# **get_user**
> RimeGetUserResponse get_user(user_id_uuid, oidc_id_token=oidc_id_token)

GetUser

Return the user with the specified ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_user_response import RimeGetUserResponse
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
    api_instance = ri.apiclient.UserApi(api_client)
    user_id_uuid = 'user_id_uuid_example' # str | Unique object ID.
    oidc_id_token = 'oidc_id_token_example' # str | ID of the OIDC provider token. (optional)

    try:
        # GetUser
        api_response = api_instance.get_user(user_id_uuid, oidc_id_token=oidc_id_token)
        print("The response of UserApi->get_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->get_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id_uuid** | **str**| Unique object ID. | 
 **oidc_id_token** | **str**| ID of the OIDC provider token. | [optional] 

### Return type

[**RimeGetUserResponse**](RimeGetUserResponse.md)

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

# **list_api_tokens**
> RimeListAPITokensResponse list_api_tokens(page_size=page_size, workspace_id_uuid=workspace_id_uuid, page_token=page_token, first_page_query_token_type=first_page_query_token_type)

ListAPITokens

List all API tokens for a Workspace.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_api_tokens_response import RimeListAPITokensResponse
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
    api_instance = ri.apiclient.UserApi(api_client)
    page_size = 'page_size_example' # str | The maximum number of API Token objects to return in a single page. (optional)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID. (optional)
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListAPITokens query. The ListAPITokens query returns a pageToken when there is more than one page of results. (optional)
    first_page_query_token_type = 'TOKEN_TYPE_UNSPECIFIED' # str | Specifies the type of token. The query filters for results that match the specified type. (optional) (default to 'TOKEN_TYPE_UNSPECIFIED')

    try:
        # ListAPITokens
        api_response = api_instance.list_api_tokens(page_size=page_size, workspace_id_uuid=workspace_id_uuid, page_token=page_token, first_page_query_token_type=first_page_query_token_type)
        print("The response of UserApi->list_api_tokens:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->list_api_tokens: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **str**| The maximum number of API Token objects to return in a single page. | [optional] 
 **workspace_id_uuid** | **str**| Unique object ID. | [optional] 
 **page_token** | **str**| Specifies a page of the list returned by a ListAPITokens query. The ListAPITokens query returns a pageToken when there is more than one page of results. | [optional] 
 **first_page_query_token_type** | **str**| Specifies the type of token. The query filters for results that match the specified type. | [optional] [default to &#39;TOKEN_TYPE_UNSPECIFIED&#39;]

### Return type

[**RimeListAPITokensResponse**](RimeListAPITokensResponse.md)

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

# **list_current_user_roles**
> RimeListCurrentUserRolesResponse list_current_user_roles()

ListCurrentUserRoles

Returns the list of roles of the logged in user.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_current_user_roles_response import RimeListCurrentUserRolesResponse
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
    api_instance = ri.apiclient.UserApi(api_client)

    try:
        # ListCurrentUserRoles
        api_response = api_instance.list_current_user_roles()
        print("The response of UserApi->list_current_user_roles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->list_current_user_roles: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RimeListCurrentUserRolesResponse**](RimeListCurrentUserRolesResponse.md)

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

# **list_users**
> RimeListUsersResponse list_users(page_token=page_token, page_size=page_size)

ListUsers

List all users.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_users_response import RimeListUsersResponse
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
    api_instance = ri.apiclient.UserApi(api_client)
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListUsers query. The ListUsers query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageQuery field. (optional)
    page_size = 'page_size_example' # str | The maximum number of User objects to return in a single page. (optional)

    try:
        # ListUsers
        api_response = api_instance.list_users(page_token=page_token, page_size=page_size)
        print("The response of UserApi->list_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->list_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_token** | **str**| Specifies a page of the list returned by a ListUsers query. The ListUsers query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageQuery field. | [optional] 
 **page_size** | **str**| The maximum number of User objects to return in a single page. | [optional] 

### Return type

[**RimeListUsersResponse**](RimeListUsersResponse.md)

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

# **reset_password**
> object reset_password(user_id_uuid, body)

ResetPassword

Reset the password of a user with the specified ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.reset_password_request import ResetPasswordRequest
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
    api_instance = ri.apiclient.UserApi(api_client)
    user_id_uuid = 'user_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.ResetPasswordRequest() # ResetPasswordRequest | 

    try:
        # ResetPassword
        api_response = api_instance.reset_password(user_id_uuid, body)
        print("The response of UserApi->reset_password:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->reset_password: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id_uuid** | **str**| Unique object ID. | 
 **body** | [**ResetPasswordRequest**](ResetPasswordRequest.md)|  | 

### Return type

**object**

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

# **update_agent_api_token**
> RimeUpdateAgentAPITokenResponse update_agent_api_token(body)

UpdateAgentAPIToken

Refreshes an agent's API token.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_update_agent_api_token_request import RimeUpdateAgentAPITokenRequest
from ri.apiclient.models.rime_update_agent_api_token_response import RimeUpdateAgentAPITokenResponse
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
    api_instance = ri.apiclient.UserApi(api_client)
    body = ri.apiclient.RimeUpdateAgentAPITokenRequest() # RimeUpdateAgentAPITokenRequest | 

    try:
        # UpdateAgentAPIToken
        api_response = api_instance.update_agent_api_token(body)
        print("The response of UserApi->update_agent_api_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->update_agent_api_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeUpdateAgentAPITokenRequest**](RimeUpdateAgentAPITokenRequest.md)|  | 

### Return type

[**RimeUpdateAgentAPITokenResponse**](RimeUpdateAgentAPITokenResponse.md)

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

# **update_user**
> object update_user(user_id_uuid, body)

UpdateUser

Update a user with the specified ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.update_user_request import UpdateUserRequest
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
    api_instance = ri.apiclient.UserApi(api_client)
    user_id_uuid = 'user_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.UpdateUserRequest() # UpdateUserRequest | 

    try:
        # UpdateUser
        api_response = api_instance.update_user(user_id_uuid, body)
        print("The response of UserApi->update_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UserApi->update_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id_uuid** | **str**| Unique object ID. | 
 **body** | [**UpdateUserRequest**](UpdateUserRequest.md)|  | 

### Return type

**object**

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

