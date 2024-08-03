# ri.apiclient.JobReaderApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cancel_job**](JobReaderApi.md#cancel_job) | **POST** /v1/jobs/cancel/{jobId} | CancelJob
[**get_job**](JobReaderApi.md#get_job) | **GET** /v1/jobs/{jobId} | GetJob
[**get_project_id**](JobReaderApi.md#get_project_id) | **GET** /v1/jobs/{jobId}/project-id | GetProjectID
[**get_test_run_id**](JobReaderApi.md#get_test_run_id) | **GET** /v1/jobs/{jobId}/test-run-id | GetTestRunID
[**list_gai_test_job**](JobReaderApi.md#list_gai_test_job) | **GET** /v1-beta/jobs/generative/workspaces/{workspaceId.uuid} | ListGAITestJob is a method to list all GAI test jobs for a given workspace.
[**list_jobs_for_project**](JobReaderApi.md#list_jobs_for_project) | **GET** /v1/jobs/project/{projectId.uuid} | ListJobsForProject


# **cancel_job**
> object cancel_job(job_id)

CancelJob

Cancels the job with the specified ID.

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
    api_instance = ri.apiclient.JobReaderApi(api_client)
    job_id = 'job_id_example' # str | Unique job ID of job to be cancelled.

    try:
        # CancelJob
        api_response = api_instance.cancel_job(job_id)
        print("The response of JobReaderApi->cancel_job:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobReaderApi->cancel_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Unique job ID of job to be cancelled. | 

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

# **get_job**
> RimeGetJobResponse get_job(job_id, view=view)

GetJob

Get a single job by ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_job_response import RimeGetJobResponse
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
    api_instance = ri.apiclient.JobReaderApi(api_client)
    job_id = 'job_id_example' # str | Unique job ID
    view = 'JOB_VIEW_UNSPECIFIED' # str | Specifies how much information about the job to retrieve. The default behavior is the Basic view.   - JOB_VIEW_BASIC: Server responses only include basic information about the job, including type, status, and some job data.  - JOB_VIEW_FULL: Server responses include all available information about the job, including progress. Has greater performance requirements than the Basic view. (optional) (default to 'JOB_VIEW_UNSPECIFIED')

    try:
        # GetJob
        api_response = api_instance.get_job(job_id, view=view)
        print("The response of JobReaderApi->get_job:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobReaderApi->get_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Unique job ID | 
 **view** | **str**| Specifies how much information about the job to retrieve. The default behavior is the Basic view.   - JOB_VIEW_BASIC: Server responses only include basic information about the job, including type, status, and some job data.  - JOB_VIEW_FULL: Server responses include all available information about the job, including progress. Has greater performance requirements than the Basic view. | [optional] [default to &#39;JOB_VIEW_UNSPECIFIED&#39;]

### Return type

[**RimeGetJobResponse**](RimeGetJobResponse.md)

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

# **get_project_id**
> RimeGetProjectIDResponse get_project_id(job_id)

GetProjectID

Returns the project ID of the project running the job with the specified job ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_project_id_response import RimeGetProjectIDResponse
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
    api_instance = ri.apiclient.JobReaderApi(api_client)
    job_id = 'job_id_example' # str | Unique job ID belonging to the project.

    try:
        # GetProjectID
        api_response = api_instance.get_project_id(job_id)
        print("The response of JobReaderApi->get_project_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobReaderApi->get_project_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Unique job ID belonging to the project. | 

### Return type

[**RimeGetProjectIDResponse**](RimeGetProjectIDResponse.md)

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

# **get_test_run_id**
> RimeGetTestRunIDResponse get_test_run_id(job_id)

GetTestRunID

Returns a test run ID based on a specified job ID. The job ID must be for a completed stress test job.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_test_run_id_response import RimeGetTestRunIDResponse
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
    api_instance = ri.apiclient.JobReaderApi(api_client)
    job_id = 'job_id_example' # str | Unique job ID associated with the test run.

    try:
        # GetTestRunID
        api_response = api_instance.get_test_run_id(job_id)
        print("The response of JobReaderApi->get_test_run_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobReaderApi->get_test_run_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| Unique job ID associated with the test run. | 

### Return type

[**RimeGetTestRunIDResponse**](RimeGetTestRunIDResponse.md)

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

# **list_gai_test_job**
> RimeListGAITestJobResponse list_gai_test_job(workspace_id_uuid, first_page_query_selected_statuses=first_page_query_selected_statuses, page_token=page_token, page_size=page_size, view=view)

ListGAITestJob is a method to list all GAI test jobs for a given workspace.

They will be sorted in descending order by creation time.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_gai_test_job_response import RimeListGAITestJobResponse
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
    api_instance = ri.apiclient.JobReaderApi(api_client)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID.
    first_page_query_selected_statuses = ['first_page_query_selected_statuses_example'] # List[str] | Specifies a set of statuses. The query only returns results with a status in the specified set. Specify no statuses to return all results.   - JOB_STATUS_PENDING: Resources have been created for the job but the job has not started yet.  - JOB_STATUS_FAILED: Blanket status for user or system-related job failure.  - JOB_STATUS_REQUESTED: The job descriptor exists but has no resources allocated. Jobs that remain in this status without moving to the PENDING status are at risk of entering the FAILED status.  - JOB_STATUS_CANCELLED: Job has been cancelled. Cancelled jobs cannot be recovered. (optional)
    page_token = 'page_token_example' # str | The ListJobs query returns a pageToken after the first request. (optional)
    page_size = 'page_size_example' # str | The maximum number of Job objects to return in a single page. (optional)
    view = 'JOB_VIEW_UNSPECIFIED' # str | Specifies how much information about each job to retrieve.   - JOB_VIEW_BASIC: Server responses only include basic information about the job, including type, status, and some job data.  - JOB_VIEW_FULL: Server responses include all available information about the job, including progress. Has greater performance requirements than the Basic view. (optional) (default to 'JOB_VIEW_UNSPECIFIED')

    try:
        # ListGAITestJob is a method to list all GAI test jobs for a given workspace.
        api_response = api_instance.list_gai_test_job(workspace_id_uuid, first_page_query_selected_statuses=first_page_query_selected_statuses, page_token=page_token, page_size=page_size, view=view)
        print("The response of JobReaderApi->list_gai_test_job:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobReaderApi->list_gai_test_job: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id_uuid** | **str**| Unique object ID. | 
 **first_page_query_selected_statuses** | [**List[str]**](str.md)| Specifies a set of statuses. The query only returns results with a status in the specified set. Specify no statuses to return all results.   - JOB_STATUS_PENDING: Resources have been created for the job but the job has not started yet.  - JOB_STATUS_FAILED: Blanket status for user or system-related job failure.  - JOB_STATUS_REQUESTED: The job descriptor exists but has no resources allocated. Jobs that remain in this status without moving to the PENDING status are at risk of entering the FAILED status.  - JOB_STATUS_CANCELLED: Job has been cancelled. Cancelled jobs cannot be recovered. | [optional] 
 **page_token** | **str**| The ListJobs query returns a pageToken after the first request. | [optional] 
 **page_size** | **str**| The maximum number of Job objects to return in a single page. | [optional] 
 **view** | **str**| Specifies how much information about each job to retrieve.   - JOB_VIEW_BASIC: Server responses only include basic information about the job, including type, status, and some job data.  - JOB_VIEW_FULL: Server responses include all available information about the job, including progress. Has greater performance requirements than the Basic view. | [optional] [default to &#39;JOB_VIEW_UNSPECIFIED&#39;]

### Return type

[**RimeListGAITestJobResponse**](RimeListGAITestJobResponse.md)

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

# **list_jobs_for_project**
> RimeListJobsForProjectResponse list_jobs_for_project(project_id_uuid, first_page_query_selected_statuses=first_page_query_selected_statuses, first_page_query_selected_types=first_page_query_selected_types, page_token=page_token, page_size=page_size, view=view)

ListJobsForProject

Returns a paginated list of jobs for a given project. The list can be filtered by job type and status.  #### Python pagination example:  ```python all_objects = [] # Required for authentication to all methods in the API. headers = {\"rime-api-key\": \"INSERT_API_TOKEN\"} # TODO page_token = \"\" # Initialize query parameters in a dictionary params = {\"INSERT_QUERY_PARAMETER\": \"INSERT_QUERY_VALUE\"} # TODO # Make requests until all results have been returned. while True:     # If the page_token from a previous response is not empty, we need to specify this     # token as a parameter to the next request in order to return the next page.     if page_token != \"\":         params = {\"page_token\": page_token}     res = requests.get(\"INSERT_METHOD_URI\", params=params, headers=headers) # TODO     if res.status_code != 200 :         raise ValueError(res)     res_json = res.json()     all_objects.extend(res_json['INSERT_OBJECT_KEY']) # TODO     page_token = res_json['nextPageToken']     # If all results have been returned, res_json['hasMore'] is false.     if not res_json[\"hasMore\"]:         break ```

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_jobs_for_project_response import RimeListJobsForProjectResponse
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
    api_instance = ri.apiclient.JobReaderApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    first_page_query_selected_statuses = ['first_page_query_selected_statuses_example'] # List[str] | Specifies a set of statuses. The query only returns results with a status in the specified set. Specify no statuses to return all results.   - JOB_STATUS_PENDING: Resources have been created for the job but the job has not started yet.  - JOB_STATUS_FAILED: Blanket status for user or system-related job failure.  - JOB_STATUS_REQUESTED: The job descriptor exists but has no resources allocated. Jobs that remain in this status without moving to the PENDING status are at risk of entering the FAILED status.  - JOB_STATUS_CANCELLED: Job has been cancelled. Cancelled jobs cannot be recovered. (optional)
    first_page_query_selected_types = ['first_page_query_selected_types_example'] # List[str] | Specifies a set of types. The query only returns jobs with types in the specified set. Specify no types to return all results. Job types not tied to projects will not be returned. (optional)
    page_token = 'page_token_example' # str | The ListJobs query returns a pageToken after the first request. (optional)
    page_size = 'page_size_example' # str | The maximum number of Job objects to return in a single page. (optional)
    view = 'JOB_VIEW_UNSPECIFIED' # str | Specifies how much information about each job to retrieve.   - JOB_VIEW_BASIC: Server responses only include basic information about the job, including type, status, and some job data.  - JOB_VIEW_FULL: Server responses include all available information about the job, including progress. Has greater performance requirements than the Basic view. (optional) (default to 'JOB_VIEW_UNSPECIFIED')

    try:
        # ListJobsForProject
        api_response = api_instance.list_jobs_for_project(project_id_uuid, first_page_query_selected_statuses=first_page_query_selected_statuses, first_page_query_selected_types=first_page_query_selected_types, page_token=page_token, page_size=page_size, view=view)
        print("The response of JobReaderApi->list_jobs_for_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling JobReaderApi->list_jobs_for_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **first_page_query_selected_statuses** | [**List[str]**](str.md)| Specifies a set of statuses. The query only returns results with a status in the specified set. Specify no statuses to return all results.   - JOB_STATUS_PENDING: Resources have been created for the job but the job has not started yet.  - JOB_STATUS_FAILED: Blanket status for user or system-related job failure.  - JOB_STATUS_REQUESTED: The job descriptor exists but has no resources allocated. Jobs that remain in this status without moving to the PENDING status are at risk of entering the FAILED status.  - JOB_STATUS_CANCELLED: Job has been cancelled. Cancelled jobs cannot be recovered. | [optional] 
 **first_page_query_selected_types** | [**List[str]**](str.md)| Specifies a set of types. The query only returns jobs with types in the specified set. Specify no types to return all results. Job types not tied to projects will not be returned. | [optional] 
 **page_token** | **str**| The ListJobs query returns a pageToken after the first request. | [optional] 
 **page_size** | **str**| The maximum number of Job objects to return in a single page. | [optional] 
 **view** | **str**| Specifies how much information about each job to retrieve.   - JOB_VIEW_BASIC: Server responses only include basic information about the job, including type, status, and some job data.  - JOB_VIEW_FULL: Server responses include all available information about the job, including progress. Has greater performance requirements than the Basic view. | [optional] [default to &#39;JOB_VIEW_UNSPECIFIED&#39;]

### Return type

[**RimeListJobsForProjectResponse**](RimeListJobsForProjectResponse.md)

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

