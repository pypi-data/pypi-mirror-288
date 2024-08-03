# ri.apiclient.GenerativeValidationApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**quick_scan**](GenerativeValidationApi.md#quick_scan) | **POST** /v1-beta/generative/testing/quick | Start Generative AI Validation Quick Scan
[**results**](GenerativeValidationApi.md#results) | **GET** /v1-beta/generative/testing/{jobId.uuid} | Get Generative AI Validation Results
[**start_generative_test**](GenerativeValidationApi.md#start_generative_test) | **POST** /v1-beta/generative/testing | Start a Generative AI Validation Test
[**test_runs**](GenerativeValidationApi.md#test_runs) | **GET** /v1-beta/generative/testing/workspaces/{workspaceId.uuid} | List Generative AI Validation Test Runs


# **quick_scan**
> GenerativevalidationStartTestResponse quick_scan(body)

Start Generative AI Validation Quick Scan

Starts an AI Validation quick scan on the specified generative model.  Results for this are not comprehensive. The status of the job can be tracked through the [JobReader service](#tag/JobReader). The results can of the test  can be retrieved using the [Results endpoint](#tag/GenerativeModelTesting/operation/Results).

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.generativevalidation_start_test_request import GenerativevalidationStartTestRequest
from ri.apiclient.models.generativevalidation_start_test_response import GenerativevalidationStartTestResponse
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
    api_instance = ri.apiclient.GenerativeValidationApi(api_client)
    body = ri.apiclient.GenerativevalidationStartTestRequest() # GenerativevalidationStartTestRequest | 

    try:
        # Start Generative AI Validation Quick Scan
        api_response = api_instance.quick_scan(body)
        print("The response of GenerativeValidationApi->quick_scan:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GenerativeValidationApi->quick_scan: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GenerativevalidationStartTestRequest**](GenerativevalidationStartTestRequest.md)|  | 

### Return type

[**GenerativevalidationStartTestResponse**](GenerativevalidationStartTestResponse.md)

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

# **results**
> GenerativevalidationGetResultsResponse results(job_id_uuid, page_token=page_token, page_size=page_size)

Get Generative AI Validation Results

Retrieve the results of a generative model testing for a successful job. This is a paginated API.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.generativevalidation_get_results_response import GenerativevalidationGetResultsResponse
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
    api_instance = ri.apiclient.GenerativeValidationApi(api_client)
    job_id_uuid = 'job_id_uuid_example' # str | Unique object ID.
    page_token = 'page_token_example' # str | A token representing one page from the list returned by a GetResults API. The GetResults API returns a page_token when there is more than one page of results. (optional)
    page_size = 'page_size_example' # str | The maximum number of objects to return in a single page.  Maximum page size is 1000. (optional)

    try:
        # Get Generative AI Validation Results
        api_response = api_instance.results(job_id_uuid, page_token=page_token, page_size=page_size)
        print("The response of GenerativeValidationApi->results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GenerativeValidationApi->results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id_uuid** | **str**| Unique object ID. | 
 **page_token** | **str**| A token representing one page from the list returned by a GetResults API. The GetResults API returns a page_token when there is more than one page of results. | [optional] 
 **page_size** | **str**| The maximum number of objects to return in a single page.  Maximum page size is 1000. | [optional] 

### Return type

[**GenerativevalidationGetResultsResponse**](GenerativevalidationGetResultsResponse.md)

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

# **start_generative_test**
> GenerativevalidationStartTestResponse start_generative_test(body)

Start a Generative AI Validation Test

Starts an AI validation test on the specified generative model. Generative testing is designed to work with a model that is served over an HTTP endpoint that returns JSON. It assumes that the model is a Q&A style model which takes a prompt as an input and returns a single textual response. See the API details for supported features, such as system prompt.  The status of the job can be tracked through the [JobReader service](#tag/JobReader). The results of the test can be retrieved using the [Results endpoint](#tag/GenerativeModelTesting/operation/Results).

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.generativevalidation_start_test_request import GenerativevalidationStartTestRequest
from ri.apiclient.models.generativevalidation_start_test_response import GenerativevalidationStartTestResponse
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
    api_instance = ri.apiclient.GenerativeValidationApi(api_client)
    body = ri.apiclient.GenerativevalidationStartTestRequest() # GenerativevalidationStartTestRequest | 

    try:
        # Start a Generative AI Validation Test
        api_response = api_instance.start_generative_test(body)
        print("The response of GenerativeValidationApi->start_generative_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GenerativeValidationApi->start_generative_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GenerativevalidationStartTestRequest**](GenerativevalidationStartTestRequest.md)|  | 

### Return type

[**GenerativevalidationStartTestResponse**](GenerativevalidationStartTestResponse.md)

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

# **test_runs**
> ApigenerativevalidationListTestRunsResponse test_runs(workspace_id_uuid, page_token=page_token, page_size=page_size)

List Generative AI Validation Test Runs

Retrieves generative validation test runs for a workspace.  This is a paginated API.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.apigenerativevalidation_list_test_runs_response import ApigenerativevalidationListTestRunsResponse
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
    api_instance = ri.apiclient.GenerativeValidationApi(api_client)
    workspace_id_uuid = 'workspace_id_uuid_example' # str | Unique object ID.
    page_token = 'page_token_example' # str | A token representing one page from the list returned by a GetGenerativeModelTestResults API. The GetGenerativeModelTestResults API returns a page_token when there is more than one page of results. (optional)
    page_size = 'page_size_example' # str | The maximum number of objects to return in a single page.  Maximum page size is 1000. (optional)

    try:
        # List Generative AI Validation Test Runs
        api_response = api_instance.test_runs(workspace_id_uuid, page_token=page_token, page_size=page_size)
        print("The response of GenerativeValidationApi->test_runs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GenerativeValidationApi->test_runs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id_uuid** | **str**| Unique object ID. | 
 **page_token** | **str**| A token representing one page from the list returned by a GetGenerativeModelTestResults API. The GetGenerativeModelTestResults API returns a page_token when there is more than one page of results. | [optional] 
 **page_size** | **str**| The maximum number of objects to return in a single page.  Maximum page size is 1000. | [optional] 

### Return type

[**ApigenerativevalidationListTestRunsResponse**](ApigenerativevalidationListTestRunsResponse.md)

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

