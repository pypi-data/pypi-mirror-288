# ri.apiclient.WorkspaceServiceApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_users_to_workspace**](WorkspaceServiceApi.md#add_users_to_workspace) | **POST** /v1/workspace/{workspaceId.uuid}/users | AddUsersToWorkspace
[**create_workspace**](WorkspaceServiceApi.md#create_workspace) | **POST** /v1/workspace | CreateWorkspace
[**delete_workspace**](WorkspaceServiceApi.md#delete_workspace) | **DELETE** /v1/workspace/{workspaceId.uuid} | DeleteWorkspace
[**get_workspace**](WorkspaceServiceApi.md#get_workspace) | **GET** /v1/workspace/{workspaceId.uuid} | GetWorkspace
[**list_project_tags_in_workspace**](WorkspaceServiceApi.md#list_project_tags_in_workspace) | **GET** /v1/workspace/{workspaceId.uuid}/tags/project | ListProjectTagsInWorkspace
[**list_users_of_workspace**](WorkspaceServiceApi.md#list_users_of_workspace) | **GET** /v1/workspace/{workspaceId.uuid}/users | ListUsersOfWorkspace
[**list_workspaces**](WorkspaceServiceApi.md#list_workspaces) | **GET** /v1/workspace | ListWorkspaces
[**remove_user_from_workspace**](WorkspaceServiceApi.md#remove_user_from_workspace) | **DELETE** /v1/workspace/{workspaceId.uuid}/users/{userId.uuid} | RemoveUserFromWorkspace
[**update_user_of_workspace**](WorkspaceServiceApi.md#update_user_of_workspace) | **PUT** /v1/workspace/{workspaceId.uuid}/users/{user.userId.uuid} | UpdateUserOfWorkspace
[**update_workspace**](WorkspaceServiceApi.md#update_workspace) | **PUT** /v1/workspace/{workspace.workspaceId.uuid} | UpdateWorkspace


# **add_users_to_workspace**
> object add_users_to_workspace(workspace_id_uuid, body)

AddUsersToWorkspace

Grants Users permissions to a Workspace.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.add_users_to_workspace_request import AddUsersToWorkspaceRequest
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
    api_instance = ri.apiclient.WorkspaceServiceApi(api_client)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.AddUsersToWorkspaceRequest() # AddUsersToWorkspaceRequest | 

    try:
        # AddUsersToWorkspace
        api_response = api_instance.add_users_to_workspace(workspace_id_uuid, body)
        print("The response of WorkspaceServiceApi->add_users_to_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceServiceApi->add_users_to_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id_uuid** | **str**| Unique object ID. | 
 **body** | [**AddUsersToWorkspaceRequest**](AddUsersToWorkspaceRequest.md)|  | 

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

# **create_workspace**
> RimeCreateWorkspaceResponse create_workspace(body)

CreateWorkspace

Create a new Workspace.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_create_workspace_request import RimeCreateWorkspaceRequest
from ri.apiclient.models.rime_create_workspace_response import RimeCreateWorkspaceResponse
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
    api_instance = ri.apiclient.WorkspaceServiceApi(api_client)
    body = ri.apiclient.RimeCreateWorkspaceRequest() # RimeCreateWorkspaceRequest | 

    try:
        # CreateWorkspace
        api_response = api_instance.create_workspace(body)
        print("The response of WorkspaceServiceApi->create_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceServiceApi->create_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeCreateWorkspaceRequest**](RimeCreateWorkspaceRequest.md)|  | 

### Return type

[**RimeCreateWorkspaceResponse**](RimeCreateWorkspaceResponse.md)

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

# **delete_workspace**
> object delete_workspace(workspace_id_uuid)

DeleteWorkspace

Deletes an existing Workspace by ID.

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
    api_instance = ri.apiclient.WorkspaceServiceApi(api_client)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteWorkspace
        api_response = api_instance.delete_workspace(workspace_id_uuid)
        print("The response of WorkspaceServiceApi->delete_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceServiceApi->delete_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id_uuid** | **str**| Unique object ID. | 

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

# **get_workspace**
> RimeGetWorkspaceResponse get_workspace(workspace_id_uuid)

GetWorkspace

Return a Workspace by ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_workspace_response import RimeGetWorkspaceResponse
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
    api_instance = ri.apiclient.WorkspaceServiceApi(api_client)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID.

    try:
        # GetWorkspace
        api_response = api_instance.get_workspace(workspace_id_uuid)
        print("The response of WorkspaceServiceApi->get_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceServiceApi->get_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeGetWorkspaceResponse**](RimeGetWorkspaceResponse.md)

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

# **list_project_tags_in_workspace**
> RimeListProjectTagsInWorkspaceResponse list_project_tags_in_workspace(workspace_id_uuid)

ListProjectTagsInWorkspace

List the union of all tags in all projects in the workspace

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_project_tags_in_workspace_response import RimeListProjectTagsInWorkspaceResponse
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
    api_instance = ri.apiclient.WorkspaceServiceApi(api_client)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID.

    try:
        # ListProjectTagsInWorkspace
        api_response = api_instance.list_project_tags_in_workspace(workspace_id_uuid)
        print("The response of WorkspaceServiceApi->list_project_tags_in_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceServiceApi->list_project_tags_in_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeListProjectTagsInWorkspaceResponse**](RimeListProjectTagsInWorkspaceResponse.md)

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

# **list_users_of_workspace**
> RimeListUsersOfWorkspaceResponse list_users_of_workspace(workspace_id_uuid, page_token=page_token, page_size=page_size)

ListUsersOfWorkspace

Lists all Users that have permissions to a Workspace.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_users_of_workspace_response import RimeListUsersOfWorkspaceResponse
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
    api_instance = ri.apiclient.WorkspaceServiceApi(api_client)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID.
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListUsersOfWorkspace query. The ListUsersOfWorkspace query returns a pageToken when there is more than one page of results. (optional)
    page_size = 'page_size_example' # str | The maximum number of User objects to return in a single page. (optional)

    try:
        # ListUsersOfWorkspace
        api_response = api_instance.list_users_of_workspace(workspace_id_uuid, page_token=page_token, page_size=page_size)
        print("The response of WorkspaceServiceApi->list_users_of_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceServiceApi->list_users_of_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id_uuid** | **str**| Unique object ID. | 
 **page_token** | **str**| Specifies a page of the list returned by a ListUsersOfWorkspace query. The ListUsersOfWorkspace query returns a pageToken when there is more than one page of results. | [optional] 
 **page_size** | **str**| The maximum number of User objects to return in a single page. | [optional] 

### Return type

[**RimeListUsersOfWorkspaceResponse**](RimeListUsersOfWorkspaceResponse.md)

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

# **list_workspaces**
> RimeListWorkspacesResponse list_workspaces(page_size=page_size, page_token=page_token)

ListWorkspaces

List Workspaces with optional filter.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_workspaces_response import RimeListWorkspacesResponse
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
    api_instance = ri.apiclient.WorkspaceServiceApi(api_client)
    page_size = 'page_size_example' # str | The maximum number of Workspace objects to return in a single page. (optional)
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListWorkspaces query. The ListWorkspaces query returns a pageToken when there is more than one page of results. (optional)

    try:
        # ListWorkspaces
        api_response = api_instance.list_workspaces(page_size=page_size, page_token=page_token)
        print("The response of WorkspaceServiceApi->list_workspaces:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceServiceApi->list_workspaces: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **str**| The maximum number of Workspace objects to return in a single page. | [optional] 
 **page_token** | **str**| Specifies a page of the list returned by a ListWorkspaces query. The ListWorkspaces query returns a pageToken when there is more than one page of results. | [optional] 

### Return type

[**RimeListWorkspacesResponse**](RimeListWorkspacesResponse.md)

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

# **remove_user_from_workspace**
> object remove_user_from_workspace(workspace_id_uuid, user_id_uuid)

RemoveUserFromWorkspace

Removes a User from a Workspace.

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
    api_instance = ri.apiclient.WorkspaceServiceApi(api_client)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID.
    user_id_uuid = 'user_id_uuid_example' # str | Unique object ID.

    try:
        # RemoveUserFromWorkspace
        api_response = api_instance.remove_user_from_workspace(workspace_id_uuid, user_id_uuid)
        print("The response of WorkspaceServiceApi->remove_user_from_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceServiceApi->remove_user_from_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id_uuid** | **str**| Unique object ID. | 
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

# **update_user_of_workspace**
> object update_user_of_workspace(workspace_id_uuid, user_user_id_uuid, body)

UpdateUserOfWorkspace

Updates the permission of a specified User for a Workspace.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.update_user_of_workspace_request import UpdateUserOfWorkspaceRequest
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
    api_instance = ri.apiclient.WorkspaceServiceApi(api_client)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID.
    user_user_id_uuid = 'user_user_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.UpdateUserOfWorkspaceRequest() # UpdateUserOfWorkspaceRequest | 

    try:
        # UpdateUserOfWorkspace
        api_response = api_instance.update_user_of_workspace(workspace_id_uuid, user_user_id_uuid, body)
        print("The response of WorkspaceServiceApi->update_user_of_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceServiceApi->update_user_of_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id_uuid** | **str**| Unique object ID. | 
 **user_user_id_uuid** | **str**| Unique object ID. | 
 **body** | [**UpdateUserOfWorkspaceRequest**](UpdateUserOfWorkspaceRequest.md)|  | 

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

# **update_workspace**
> object update_workspace(workspace_workspace_id_uuid, body)

UpdateWorkspace

Updates an existing Workspace by ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.update_workspace_request import UpdateWorkspaceRequest
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
    api_instance = ri.apiclient.WorkspaceServiceApi(api_client)
    workspace_workspace_id_uuid = 'workspace_workspace_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.UpdateWorkspaceRequest() # UpdateWorkspaceRequest | 

    try:
        # UpdateWorkspace
        api_response = api_instance.update_workspace(workspace_workspace_id_uuid, body)
        print("The response of WorkspaceServiceApi->update_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspaceServiceApi->update_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_workspace_id_uuid** | **str**| Unique object ID. | 
 **body** | [**UpdateWorkspaceRequest**](UpdateWorkspaceRequest.md)|  | 

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

