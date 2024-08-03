# ri.apiclient.ProjectServiceApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**activate_schedule_for_project**](ProjectServiceApi.md#activate_schedule_for_project) | **PUT** /v1-beta/projects/{projectId.uuid}/schedule/{scheduleId.uuid}/activate | ActivateScheduleForProject
[**add_users_to_project**](ProjectServiceApi.md#add_users_to_project) | **POST** /v1/projects/{projectId.uuid}/role/users | AddUsersToProject
[**create_project**](ProjectServiceApi.md#create_project) | **POST** /v1/projects | CreateProject
[**deactivate_schedule_for_project**](ProjectServiceApi.md#deactivate_schedule_for_project) | **PUT** /v1-beta/projects/{projectId.uuid}/schedule/{scheduleId.uuid}/deactivate | DeactivateScheduleForProject
[**delete_project**](ProjectServiceApi.md#delete_project) | **DELETE** /v1/projects/{projectId.uuid} | DeleteProject
[**get_project**](ProjectServiceApi.md#get_project) | **GET** /v1/projects/{projectId.uuid} | GetProject
[**get_project_url**](ProjectServiceApi.md#get_project_url) | **GET** /v1/projects/{projectId.uuid}/url | GetProjectURL
[**get_workspace_roles_for_project**](ProjectServiceApi.md#get_workspace_roles_for_project) | **GET** /v1/projects/{projectId.uuid}/role/workspace | GetWorkspaceRoleForProject
[**list_projects**](ProjectServiceApi.md#list_projects) | **GET** /v1/projects | ListProjects
[**list_users_of_project**](ProjectServiceApi.md#list_users_of_project) | **GET** /v1/projects/{projectId.uuid}/role/users | ListUsersOfProject
[**remove_user_from_project**](ProjectServiceApi.md#remove_user_from_project) | **DELETE** /v1/projects/{projectId.uuid}/role/users/{userId.uuid} | RemoveUserFromProject
[**update_project**](ProjectServiceApi.md#update_project) | **PUT** /v1/projects/{projectId.uuid} | UpdateProject
[**update_user_of_project**](ProjectServiceApi.md#update_user_of_project) | **PUT** /v1/projects/{projectId.uuid}/role/users/{user.userId.uuid} | UpdateUserOfProject
[**update_workspace_roles_for_project**](ProjectServiceApi.md#update_workspace_roles_for_project) | **PUT** /v1/projects/{projectId.uuid}/role/workspace | UpdateWorkspaceRoleForProject


# **activate_schedule_for_project**
> ProjectActivateScheduleForProjectResponse activate_schedule_for_project(project_id_uuid, schedule_id_uuid, body)

ActivateScheduleForProject

Add a Schedule to run automatic tests for a Project.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.activate_schedule_for_project_request import ActivateScheduleForProjectRequest
from ri.apiclient.models.project_activate_schedule_for_project_response import ProjectActivateScheduleForProjectResponse
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    schedule_id_uuid = 'schedule_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.ActivateScheduleForProjectRequest() # ActivateScheduleForProjectRequest | 

    try:
        # ActivateScheduleForProject
        api_response = api_instance.activate_schedule_for_project(project_id_uuid, schedule_id_uuid, body)
        print("The response of ProjectServiceApi->activate_schedule_for_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->activate_schedule_for_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **schedule_id_uuid** | **str**| Unique object ID. | 
 **body** | [**ActivateScheduleForProjectRequest**](ActivateScheduleForProjectRequest.md)|  | 

### Return type

[**ProjectActivateScheduleForProjectResponse**](ProjectActivateScheduleForProjectResponse.md)

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

# **add_users_to_project**
> object add_users_to_project(project_id_uuid, body)

AddUsersToProject

Grants existing Organization users permissions to a Project for a given Project ID, based on the pairs of role and User ID provided in the request.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.add_users_to_project_request import AddUsersToProjectRequest
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.AddUsersToProjectRequest() # AddUsersToProjectRequest | 

    try:
        # AddUsersToProject
        api_response = api_instance.add_users_to_project(project_id_uuid, body)
        print("The response of ProjectServiceApi->add_users_to_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->add_users_to_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **body** | [**AddUsersToProjectRequest**](AddUsersToProjectRequest.md)|  | 

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

# **create_project**
> ProjectCreateProjectResponse create_project(body)

CreateProject

Creates a Project with required fields. Project is an organizational entity under a Workspace that contains Test Runs, Continuous Tests, and Stress Tests, along with their configurations.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.project_create_project_request import ProjectCreateProjectRequest
from ri.apiclient.models.project_create_project_response import ProjectCreateProjectResponse
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    body = ri.apiclient.ProjectCreateProjectRequest() # ProjectCreateProjectRequest | 

    try:
        # CreateProject
        api_response = api_instance.create_project(body)
        print("The response of ProjectServiceApi->create_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->create_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProjectCreateProjectRequest**](ProjectCreateProjectRequest.md)|  | 

### Return type

[**ProjectCreateProjectResponse**](ProjectCreateProjectResponse.md)

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

# **deactivate_schedule_for_project**
> object deactivate_schedule_for_project(project_id_uuid, schedule_id_uuid, body)

DeactivateScheduleForProject

Remove a Schedule from a Project.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.activate_schedule_for_project_request import ActivateScheduleForProjectRequest
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    schedule_id_uuid = 'schedule_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.ActivateScheduleForProjectRequest() # ActivateScheduleForProjectRequest | 

    try:
        # DeactivateScheduleForProject
        api_response = api_instance.deactivate_schedule_for_project(project_id_uuid, schedule_id_uuid, body)
        print("The response of ProjectServiceApi->deactivate_schedule_for_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->deactivate_schedule_for_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **schedule_id_uuid** | **str**| Unique object ID. | 
 **body** | [**ActivateScheduleForProjectRequest**](ActivateScheduleForProjectRequest.md)|  | 

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

# **delete_project**
> object delete_project(project_id_uuid)

DeleteProject

Deletes a Project for a given Project ID.

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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteProject
        api_response = api_instance.delete_project(project_id_uuid)
        print("The response of ProjectServiceApi->delete_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->delete_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 

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

# **get_project**
> ProjectGetProjectResponse get_project(project_id_uuid)

GetProject

Returns a Project for a given Project ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.project_get_project_response import ProjectGetProjectResponse
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.

    try:
        # GetProject
        api_response = api_instance.get_project(project_id_uuid)
        print("The response of ProjectServiceApi->get_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->get_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 

### Return type

[**ProjectGetProjectResponse**](ProjectGetProjectResponse.md)

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

# **get_project_url**
> ProjectGetProjectURLResponse get_project_url(project_id_uuid)

GetProjectURL

Return the URL of a Project for a given Project ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.project_get_project_url_response import ProjectGetProjectURLResponse
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.

    try:
        # GetProjectURL
        api_response = api_instance.get_project_url(project_id_uuid)
        print("The response of ProjectServiceApi->get_project_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->get_project_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 

### Return type

[**ProjectGetProjectURLResponse**](ProjectGetProjectURLResponse.md)

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

# **get_workspace_roles_for_project**
> ProjectGetWorkspaceRolesForProjectResponse get_workspace_roles_for_project(project_id_uuid)

GetWorkspaceRoleForProject

Returns the permissions of the Workspace members for a Project given Project ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.project_get_workspace_roles_for_project_response import ProjectGetWorkspaceRolesForProjectResponse
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.

    try:
        # GetWorkspaceRoleForProject
        api_response = api_instance.get_workspace_roles_for_project(project_id_uuid)
        print("The response of ProjectServiceApi->get_workspace_roles_for_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->get_workspace_roles_for_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 

### Return type

[**ProjectGetWorkspaceRolesForProjectResponse**](ProjectGetWorkspaceRolesForProjectResponse.md)

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

# **list_projects**
> ProjectListProjectsResponse list_projects(workspace_id_uuid=workspace_id_uuid, first_page_query_is_published=first_page_query_is_published, first_page_query_creation_time_range_start_time=first_page_query_creation_time_range_start_time, first_page_query_creation_time_range_end_time=first_page_query_creation_time_range_end_time, first_page_query_last_test_run_time_range_start_time=first_page_query_last_test_run_time_range_start_time, first_page_query_last_test_run_time_range_end_time=first_page_query_last_test_run_time_range_end_time, first_page_query_stress_test_categories=first_page_query_stress_test_categories, first_page_query_continuous_test_categories=first_page_query_continuous_test_categories, first_page_query_owner_email=first_page_query_owner_email, first_page_query_model_tasks=first_page_query_model_tasks, first_page_query_status=first_page_query_status, first_page_query_sort_sort_order=first_page_query_sort_sort_order, first_page_query_sort_sort_by=first_page_query_sort_sort_by, first_page_query_search_expression=first_page_query_search_expression, first_page_query_search_search_fields=first_page_query_search_search_fields, page_token=page_token, page_size=page_size)

ListProjects

Returns a paginated list of Projects for a given Workspace ID. Filters out Projects that the user does not have access to. The list is sorted by the last test run time field of each Project.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.project_list_projects_response import ProjectListProjectsResponse
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID. (optional)
    first_page_query_is_published = True # bool | Optional: If true, return published projects. If false, return unpublished projects. If not specified, return all projects. (optional)
    first_page_query_creation_time_range_start_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    first_page_query_creation_time_range_end_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    first_page_query_last_test_run_time_range_start_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    first_page_query_last_test_run_time_range_end_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    first_page_query_stress_test_categories = ['first_page_query_stress_test_categories_example'] # List[str] | Optional: When specified, return all projects whose ST categories are a superset of the ST categories provided here. (optional)
    first_page_query_continuous_test_categories = ['first_page_query_continuous_test_categories_example'] # List[str] | Optional: When specified, return all projects whose CT categories are a superset of the CT categories provided here. (optional)
    first_page_query_owner_email = 'first_page_query_owner_email_example' # str | Optional: When specified, return all projects whose owner email matches. (optional)
    first_page_query_model_tasks = ['first_page_query_model_tasks_example'] # List[str] | Optional: When specified, return all projects whose model task is the provided model task. (optional)
    first_page_query_status = 'PROJECT_STATUS_UNSPECIFIED' # str | Optional: When specified, return all projects whose status is the provided status. (optional) (default to 'PROJECT_STATUS_UNSPECIFIED')
    first_page_query_sort_sort_order = 'ORDER_UNSPECIFIED' # str |  (optional) (default to 'ORDER_UNSPECIFIED')
    first_page_query_sort_sort_by = 'first_page_query_sort_sort_by_example' # str |  (optional)
    first_page_query_search_expression = 'first_page_query_search_expression_example' # str |  (optional)
    first_page_query_search_search_fields = ['first_page_query_search_search_fields_example'] # List[str] |  (optional)
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListProjects query. The ListProjects query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageQuery field. (optional)
    page_size = 'page_size_example' # str | The maximum number of Project objects to return in a single page. (optional)

    try:
        # ListProjects
        api_response = api_instance.list_projects(workspace_id_uuid=workspace_id_uuid, first_page_query_is_published=first_page_query_is_published, first_page_query_creation_time_range_start_time=first_page_query_creation_time_range_start_time, first_page_query_creation_time_range_end_time=first_page_query_creation_time_range_end_time, first_page_query_last_test_run_time_range_start_time=first_page_query_last_test_run_time_range_start_time, first_page_query_last_test_run_time_range_end_time=first_page_query_last_test_run_time_range_end_time, first_page_query_stress_test_categories=first_page_query_stress_test_categories, first_page_query_continuous_test_categories=first_page_query_continuous_test_categories, first_page_query_owner_email=first_page_query_owner_email, first_page_query_model_tasks=first_page_query_model_tasks, first_page_query_status=first_page_query_status, first_page_query_sort_sort_order=first_page_query_sort_sort_order, first_page_query_sort_sort_by=first_page_query_sort_sort_by, first_page_query_search_expression=first_page_query_search_expression, first_page_query_search_search_fields=first_page_query_search_search_fields, page_token=page_token, page_size=page_size)
        print("The response of ProjectServiceApi->list_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->list_projects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id_uuid** | **str**| Unique object ID. | [optional] 
 **first_page_query_is_published** | **bool**| Optional: If true, return published projects. If false, return unpublished projects. If not specified, return all projects. | [optional] 
 **first_page_query_creation_time_range_start_time** | **datetime**|  | [optional] 
 **first_page_query_creation_time_range_end_time** | **datetime**|  | [optional] 
 **first_page_query_last_test_run_time_range_start_time** | **datetime**|  | [optional] 
 **first_page_query_last_test_run_time_range_end_time** | **datetime**|  | [optional] 
 **first_page_query_stress_test_categories** | [**List[str]**](str.md)| Optional: When specified, return all projects whose ST categories are a superset of the ST categories provided here. | [optional] 
 **first_page_query_continuous_test_categories** | [**List[str]**](str.md)| Optional: When specified, return all projects whose CT categories are a superset of the CT categories provided here. | [optional] 
 **first_page_query_owner_email** | **str**| Optional: When specified, return all projects whose owner email matches. | [optional] 
 **first_page_query_model_tasks** | [**List[str]**](str.md)| Optional: When specified, return all projects whose model task is the provided model task. | [optional] 
 **first_page_query_status** | **str**| Optional: When specified, return all projects whose status is the provided status. | [optional] [default to &#39;PROJECT_STATUS_UNSPECIFIED&#39;]
 **first_page_query_sort_sort_order** | **str**|  | [optional] [default to &#39;ORDER_UNSPECIFIED&#39;]
 **first_page_query_sort_sort_by** | **str**|  | [optional] 
 **first_page_query_search_expression** | **str**|  | [optional] 
 **first_page_query_search_search_fields** | [**List[str]**](str.md)|  | [optional] 
 **page_token** | **str**| Specifies a page of the list returned by a ListProjects query. The ListProjects query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageQuery field. | [optional] 
 **page_size** | **str**| The maximum number of Project objects to return in a single page. | [optional] 

### Return type

[**ProjectListProjectsResponse**](ProjectListProjectsResponse.md)

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

# **list_users_of_project**
> ProjectListUsersOfProjectResponse list_users_of_project(project_id_uuid, page_token=page_token, page_size=page_size)

ListUsersOfProject

Lists the users and their roles of a Project for a given Project ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.project_list_users_of_project_response import ProjectListUsersOfProjectResponse
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListUsersOfProject query. The ListUsersOfProject query returns a pageToken when there is more than one page of results. (optional)
    page_size = 'page_size_example' # str | The maximum number of User objects to return in a single page. (optional)

    try:
        # ListUsersOfProject
        api_response = api_instance.list_users_of_project(project_id_uuid, page_token=page_token, page_size=page_size)
        print("The response of ProjectServiceApi->list_users_of_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->list_users_of_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **page_token** | **str**| Specifies a page of the list returned by a ListUsersOfProject query. The ListUsersOfProject query returns a pageToken when there is more than one page of results. | [optional] 
 **page_size** | **str**| The maximum number of User objects to return in a single page. | [optional] 

### Return type

[**ProjectListUsersOfProjectResponse**](ProjectListUsersOfProjectResponse.md)

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

# **remove_user_from_project**
> object remove_user_from_project(project_id_uuid, user_id_uuid)

RemoveUserFromProject

Removes all existing permissions of a user from a Project given Project ID and User ID.

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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    user_id_uuid = 'user_id_uuid_example' # str | Unique object ID.

    try:
        # RemoveUserFromProject
        api_response = api_instance.remove_user_from_project(project_id_uuid, user_id_uuid)
        print("The response of ProjectServiceApi->remove_user_from_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->remove_user_from_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
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

# **update_project**
> ProjectUpdateProjectResponse update_project(project_id_uuid, body)

UpdateProject

Updates a Project for a given Project ID. Only updates the fields specified in the FieldMask.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.project_update_project_response import ProjectUpdateProjectResponse
from ri.apiclient.models.update_project_request import UpdateProjectRequest
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.UpdateProjectRequest() # UpdateProjectRequest | 

    try:
        # UpdateProject
        api_response = api_instance.update_project(project_id_uuid, body)
        print("The response of ProjectServiceApi->update_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->update_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **body** | [**UpdateProjectRequest**](UpdateProjectRequest.md)|  | 

### Return type

[**ProjectUpdateProjectResponse**](ProjectUpdateProjectResponse.md)

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

# **update_user_of_project**
> object update_user_of_project(project_id_uuid, user_user_id_uuid, body)

UpdateUserOfProject

Updates the existing permission of a user of a Project given Project ID and User ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.update_user_of_project_request import UpdateUserOfProjectRequest
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    user_user_id_uuid = 'user_user_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.UpdateUserOfProjectRequest() # UpdateUserOfProjectRequest | 

    try:
        # UpdateUserOfProject
        api_response = api_instance.update_user_of_project(project_id_uuid, user_user_id_uuid, body)
        print("The response of ProjectServiceApi->update_user_of_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->update_user_of_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **user_user_id_uuid** | **str**| Unique object ID. | 
 **body** | [**UpdateUserOfProjectRequest**](UpdateUserOfProjectRequest.md)|  | 

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

# **update_workspace_roles_for_project**
> ProjectUpdateWorkspaceRolesForProjectResponse update_workspace_roles_for_project(project_id_uuid, body)

UpdateWorkspaceRoleForProject

Assigns users roles(permissions) on a Project based on their roles in the Workspace that contains the Project.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.project_update_workspace_roles_for_project_response import ProjectUpdateWorkspaceRolesForProjectResponse
from ri.apiclient.models.update_workspace_roles_for_project_request import UpdateWorkspaceRolesForProjectRequest
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
    api_instance = ri.apiclient.ProjectServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.UpdateWorkspaceRolesForProjectRequest() # UpdateWorkspaceRolesForProjectRequest | 

    try:
        # UpdateWorkspaceRoleForProject
        api_response = api_instance.update_workspace_roles_for_project(project_id_uuid, body)
        print("The response of ProjectServiceApi->update_workspace_roles_for_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectServiceApi->update_workspace_roles_for_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **body** | [**UpdateWorkspaceRolesForProjectRequest**](UpdateWorkspaceRolesForProjectRequest.md)|  | 

### Return type

[**ProjectUpdateWorkspaceRolesForProjectResponse**](ProjectUpdateWorkspaceRolesForProjectResponse.md)

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

