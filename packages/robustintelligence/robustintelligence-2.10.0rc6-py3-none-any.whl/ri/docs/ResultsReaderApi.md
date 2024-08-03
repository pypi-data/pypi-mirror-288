# ri.apiclient.ResultsReaderApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_test_run**](ResultsReaderApi.md#delete_test_run) | **DELETE** /v1/test-runs/{testRunId} | DeleteTestRun
[**get_batch_result**](ResultsReaderApi.md#get_batch_result) | **GET** /v1/test-runs/{testRunId}/batch-result/{testType} | GetBatchResult
[**get_category_results**](ResultsReaderApi.md#get_category_results) | **GET** /v1/category-results/{testRunId} | GetCategoryResults
[**get_feature_result**](ResultsReaderApi.md#get_feature_result) | **GET** /v1/test-runs/{testRunId}/feature-result/{urlSafeFeatureId} | GetFeatureResult
[**get_test_config**](ResultsReaderApi.md#get_test_config) | **GET** /v1-beta/test-runs/{testRunId}/test-config/{configName} | GetTestConfig
[**get_test_run**](ResultsReaderApi.md#get_test_run) | **GET** /v1/test-runs/{testRunId} | GetTestRun
[**list_feature_results**](ResultsReaderApi.md#list_feature_results) | **GET** /v1/feature-results | ListFeatureResults
[**list_monitor_categories**](ResultsReaderApi.md#list_monitor_categories) | **GET** /v1-beta/test-runs/test-category/monitor | ListMonitorCategories
[**list_summary_tests**](ResultsReaderApi.md#list_summary_tests) | **GET** /v1/summary-tests | ListSummaryTests
[**list_test_cases**](ResultsReaderApi.md#list_test_cases) | **GET** /v1/test-cases | ListTestCases
[**list_test_runs**](ResultsReaderApi.md#list_test_runs) | **GET** /v1/test-runs | ListTestRuns
[**list_validation_categories**](ResultsReaderApi.md#list_validation_categories) | **GET** /v1-beta/test-runs/test-category/validation | ListValidationCategories
[**rename_test_run**](ResultsReaderApi.md#rename_test_run) | **POST** /v1/test-runs/rename/{testRunId} | RenameTestRun
[**results_reader_list_batch_results**](ResultsReaderApi.md#results_reader_list_batch_results) | **GET** /v1/batch-results | ListBatchResults


# **delete_test_run**
> object delete_test_run(test_run_id)

DeleteTestRun

Deletes a specified test run.

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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    test_run_id = 'test_run_id_example' # str | Uniquely specifies a Test Run to delete.

    try:
        # DeleteTestRun
        api_response = api_instance.delete_test_run(test_run_id)
        print("The response of ResultsReaderApi->delete_test_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->delete_test_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_run_id** | **str**| Uniquely specifies a Test Run to delete. | 

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

# **get_batch_result**
> TestrunresultGetBatchResultResponse get_batch_result(test_run_id, test_type, show_display=show_display)

GetBatchResult

Gets the batch result for a given Test Run ID and a test type.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_get_batch_result_response import TestrunresultGetBatchResultResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    test_run_id = 'test_run_id_example' # str | Uniquely specifies a Test Run.
    test_type = 'test_type_example' # str | The type of test, such as \"Subset Accuracy\" or \"Overall Metrics\".
    show_display = True # bool | A Boolean flag that toggles whether to return display HTML. info with message. (optional)

    try:
        # GetBatchResult
        api_response = api_instance.get_batch_result(test_run_id, test_type, show_display=show_display)
        print("The response of ResultsReaderApi->get_batch_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->get_batch_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_run_id** | **str**| Uniquely specifies a Test Run. | 
 **test_type** | **str**| The type of test, such as \&quot;Subset Accuracy\&quot; or \&quot;Overall Metrics\&quot;. | 
 **show_display** | **bool**| A Boolean flag that toggles whether to return display HTML. info with message. | [optional] 

### Return type

[**TestrunresultGetBatchResultResponse**](TestrunresultGetBatchResultResponse.md)

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

# **get_category_results**
> TestrunresultGetCategoryResultsResponse get_category_results(test_run_id)

GetCategoryResults

Returns all category results of a test run.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_get_category_results_response import TestrunresultGetCategoryResultsResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    test_run_id = 'test_run_id_example' # str | The ID of the test run associated with summary tests. Specify exactly one of the page_token field or this field.

    try:
        # GetCategoryResults
        api_response = api_instance.get_category_results(test_run_id)
        print("The response of ResultsReaderApi->get_category_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->get_category_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_run_id** | **str**| The ID of the test run associated with summary tests. Specify exactly one of the page_token field or this field. | 

### Return type

[**TestrunresultGetCategoryResultsResponse**](TestrunresultGetCategoryResultsResponse.md)

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

# **get_feature_result**
> TestrunresultGetFeatureResultResponse get_feature_result(test_run_id, url_safe_feature_id, show_display=show_display)

GetFeatureResult

Returns the feature result that matches the specified test run ID and feature ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_get_feature_result_response import TestrunresultGetFeatureResultResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    test_run_id = 'test_run_id_example' # str | Uniquely specifies a Test Run.
    url_safe_feature_id = 'url_safe_feature_id_example' # str | Uniquely specifies a Feature.
    show_display = True # bool | A Boolean flag that specifies whether to return display HTML information. (optional)

    try:
        # GetFeatureResult
        api_response = api_instance.get_feature_result(test_run_id, url_safe_feature_id, show_display=show_display)
        print("The response of ResultsReaderApi->get_feature_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->get_feature_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_run_id** | **str**| Uniquely specifies a Test Run. | 
 **url_safe_feature_id** | **str**| Uniquely specifies a Feature. | 
 **show_display** | **bool**| A Boolean flag that specifies whether to return display HTML information. | [optional] 

### Return type

[**TestrunresultGetFeatureResultResponse**](TestrunresultGetFeatureResultResponse.md)

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

# **get_test_config**
> TestrunresultGetTestConfigResponse get_test_config(test_run_id, config_name)

GetTestConfig

Returns the test configuration of the specified test run as bytes.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_get_test_config_response import TestrunresultGetTestConfigResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    test_run_id = 'test_run_id_example' # str | Uniquely specifies a Test Run.
    config_name = 'config_name_example' # str | The name of the test config requested.

    try:
        # GetTestConfig
        api_response = api_instance.get_test_config(test_run_id, config_name)
        print("The response of ResultsReaderApi->get_test_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->get_test_config: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_run_id** | **str**| Uniquely specifies a Test Run. | 
 **config_name** | **str**| The name of the test config requested. | 

### Return type

[**TestrunresultGetTestConfigResponse**](TestrunresultGetTestConfigResponse.md)

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

# **get_test_run**
> TestrunresultGetTestRunResponse get_test_run(test_run_id)

GetTestRun

Returns the test run result detail for a given Test Run ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_get_test_run_response import TestrunresultGetTestRunResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    test_run_id = 'test_run_id_example' # str | Uniquely specifies a test run.

    try:
        # GetTestRun
        api_response = api_instance.get_test_run(test_run_id)
        print("The response of ResultsReaderApi->get_test_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->get_test_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_run_id** | **str**| Uniquely specifies a test run. | 

### Return type

[**TestrunresultGetTestRunResponse**](TestrunresultGetTestRunResponse.md)

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

# **list_feature_results**
> TestrunresultListFeatureResultsResponse list_feature_results(test_run_id=test_run_id, page_token=page_token, page_size=page_size, show_display=show_display)

ListFeatureResults

List all feature results from a test run.  #### Python pagination example:  ```python all_objects = [] # Required for authentication to all methods in the API. headers = {\"rime-api-key\": \"INSERT_API_TOKEN\"} # TODO page_token = \"\" # Initialize query parameters in a dictionary params = {\"INSERT_QUERY_PARAMETER\": \"INSERT_QUERY_VALUE\"} # TODO # Make requests until all results have been returned. while True:     # If the page_token from a previous response is not empty, we need to specify this     # token as a parameter to the next request in order to return the next page.     if page_token != \"\":         params = {\"page_token\": page_token}     res = requests.get(\"INSERT_METHOD_URI\", params=params, headers=headers) # TODO     if res.status_code != 200 :         raise ValueError(res)     res_json = res.json()     all_objects.extend(res_json['INSERT_OBJECT_KEY']) # TODO     page_token = res_json['nextPageToken']     # If all results have been returned, res_json['hasMore'] is false.     if not res_json[\"hasMore\"]:         break ```

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_list_feature_results_response import TestrunresultListFeatureResultsResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    test_run_id = 'test_run_id_example' # str | The ID of the Test Run associated with feature results. Specify exactly one of the page_token field or this field. (optional)
    page_token = 'page_token_example' # str | A token representing one page from the list returned by a ListFeatureResults query. The ListFeatureResults query returns a page_token when there is more than one page of results. Specify exactly one of the testRunId field or this field. (optional)
    page_size = 'page_size_example' # str | The maximum number of Feature Result objects to return in a single page. (optional)
    show_display = True # bool | A Boolean that specifies whether to return display HTML information. (optional)

    try:
        # ListFeatureResults
        api_response = api_instance.list_feature_results(test_run_id=test_run_id, page_token=page_token, page_size=page_size, show_display=show_display)
        print("The response of ResultsReaderApi->list_feature_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->list_feature_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_run_id** | **str**| The ID of the Test Run associated with feature results. Specify exactly one of the page_token field or this field. | [optional] 
 **page_token** | **str**| A token representing one page from the list returned by a ListFeatureResults query. The ListFeatureResults query returns a page_token when there is more than one page of results. Specify exactly one of the testRunId field or this field. | [optional] 
 **page_size** | **str**| The maximum number of Feature Result objects to return in a single page. | [optional] 
 **show_display** | **bool**| A Boolean that specifies whether to return display HTML information. | [optional] 

### Return type

[**TestrunresultListFeatureResultsResponse**](TestrunresultListFeatureResultsResponse.md)

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

# **list_monitor_categories**
> TestrunresultListMonitorCategoriesResponse list_monitor_categories()

ListMonitorCategories

Returns test categories belongs to monitor.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_list_monitor_categories_response import TestrunresultListMonitorCategoriesResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)

    try:
        # ListMonitorCategories
        api_response = api_instance.list_monitor_categories()
        print("The response of ResultsReaderApi->list_monitor_categories:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->list_monitor_categories: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**TestrunresultListMonitorCategoriesResponse**](TestrunresultListMonitorCategoriesResponse.md)

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

# **list_summary_tests**
> TestrunresultListSummaryTestsResponse list_summary_tests(query_test_run_id=query_test_run_id, page_token=page_token, page_size=page_size)

ListSummaryTests

Returns a paginated list of the summary tests of a test run. DEPRECATED: Use GetCategoryResults instead, the API request and response are the same. This method will be removed in the future.  #### Python pagination example:  ```python all_objects = [] # Required for authentication to all methods in the API. headers = {\"rime-api-key\": \"INSERT_API_TOKEN\"} # TODO page_token = \"\" # Initialize query parameters in a dictionary params = {\"INSERT_QUERY_PARAMETER\": \"INSERT_QUERY_VALUE\"} # TODO # Make requests until all results have been returned. while True:     # If the page_token from a previous response is not empty, we need to specify this     # token as a parameter to the next request in order to return the next page.     if page_token != \"\":         params = {\"page_token\": page_token}     res = requests.get(\"INSERT_METHOD_URI\", params=params, headers=headers) # TODO     if res.status_code != 200 :         raise ValueError(res)     res_json = res.json()     all_objects.extend(res_json['INSERT_OBJECT_KEY']) # TODO     page_token = res_json['nextPageToken']     # If all results have been returned, res_json['hasMore'] is false.     if not res_json[\"hasMore\"]:         break ```

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_list_summary_tests_response import TestrunresultListSummaryTestsResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    query_test_run_id = 'query_test_run_id_example' # str | The ID of the test run associated with summary tests. Specify exactly one of the page_token field or this field. (optional)
    page_token = 'page_token_example' # str | A token representing one page from the list returned by a ListSummaryTests query. The ListSummaryTests query returns a page_token when there is more than one page of results. Specify exactly one of the query.testRunId field or this field. (optional)
    page_size = 'page_size_example' # str | The maximum number of Summary Test objects to return in a single page. (optional)

    try:
        # ListSummaryTests
        api_response = api_instance.list_summary_tests(query_test_run_id=query_test_run_id, page_token=page_token, page_size=page_size)
        print("The response of ResultsReaderApi->list_summary_tests:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->list_summary_tests: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query_test_run_id** | **str**| The ID of the test run associated with summary tests. Specify exactly one of the page_token field or this field. | [optional] 
 **page_token** | **str**| A token representing one page from the list returned by a ListSummaryTests query. The ListSummaryTests query returns a page_token when there is more than one page of results. Specify exactly one of the query.testRunId field or this field. | [optional] 
 **page_size** | **str**| The maximum number of Summary Test objects to return in a single page. | [optional] 

### Return type

[**TestrunresultListSummaryTestsResponse**](TestrunresultListSummaryTestsResponse.md)

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

# **list_test_cases**
> TestrunresultListTestCasesResponse list_test_cases(list_test_cases_query_test_run_id=list_test_cases_query_test_run_id, list_test_cases_query_test_types=list_test_cases_query_test_types, list_test_cases_query_url_safe_feature_ids=list_test_cases_query_url_safe_feature_ids, page_token=page_token, page_size=page_size, show_display=show_display)

ListTestCases

Returns a paginated list of the test cases in a test run. Specify a set of test types to filter the list by test types.  #### Python pagination example:  ```python all_objects = [] # Required for authentication to all methods in the API. headers = {\"rime-api-key\": \"INSERT_API_TOKEN\"} # TODO page_token = \"\" # Initialize query parameters in a dictionary params = {\"INSERT_QUERY_PARAMETER\": \"INSERT_QUERY_VALUE\"} # TODO # Make requests until all results have been returned. while True:     # If the page_token from a previous response is not empty, we need to specify this     # token as a parameter to the next request in order to return the next page.     if page_token != \"\":         params = {\"page_token\": page_token}     res = requests.get(\"INSERT_METHOD_URI\", params=params, headers=headers) # TODO     if res.status_code != 200 :         raise ValueError(res)     res_json = res.json()     all_objects.extend(res_json['INSERT_OBJECT_KEY']) # TODO     page_token = res_json['nextPageToken']     # If all results have been returned, res_json['hasMore'] is false.     if not res_json[\"hasMore\"]:         break ```

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_list_test_cases_response import TestrunresultListTestCasesResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    list_test_cases_query_test_run_id = 'list_test_cases_query_test_run_id_example' # str | Uniquely specifies a Test Run associated with test cases. Specify exactly one of the page_token field or this field. (optional)
    list_test_cases_query_test_types = ['list_test_cases_query_test_types_example'] # List[str] | Optional filter for test types. (optional)
    list_test_cases_query_url_safe_feature_ids = ['list_test_cases_query_url_safe_feature_ids_example'] # List[str] | Optional filter for features. (optional)
    page_token = 'page_token_example' # str | A token representing one page from the list returned by a ListTestCases query. The ListTestCases query returns a page_token when there is more than one page of results. Specify exactly one of the ListTestCasesQuery.testRunId field or this field. (optional)
    page_size = 'page_size_example' # str | The maximum number of Test Case objects to return in a single page. (optional)
    show_display = True # bool | A Boolean flag that specifies whether to return display HTML information with the message. (optional)

    try:
        # ListTestCases
        api_response = api_instance.list_test_cases(list_test_cases_query_test_run_id=list_test_cases_query_test_run_id, list_test_cases_query_test_types=list_test_cases_query_test_types, list_test_cases_query_url_safe_feature_ids=list_test_cases_query_url_safe_feature_ids, page_token=page_token, page_size=page_size, show_display=show_display)
        print("The response of ResultsReaderApi->list_test_cases:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->list_test_cases: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **list_test_cases_query_test_run_id** | **str**| Uniquely specifies a Test Run associated with test cases. Specify exactly one of the page_token field or this field. | [optional] 
 **list_test_cases_query_test_types** | [**List[str]**](str.md)| Optional filter for test types. | [optional] 
 **list_test_cases_query_url_safe_feature_ids** | [**List[str]**](str.md)| Optional filter for features. | [optional] 
 **page_token** | **str**| A token representing one page from the list returned by a ListTestCases query. The ListTestCases query returns a page_token when there is more than one page of results. Specify exactly one of the ListTestCasesQuery.testRunId field or this field. | [optional] 
 **page_size** | **str**| The maximum number of Test Case objects to return in a single page. | [optional] 
 **show_display** | **bool**| A Boolean flag that specifies whether to return display HTML information with the message. | [optional] 

### Return type

[**TestrunresultListTestCasesResponse**](TestrunresultListTestCasesResponse.md)

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

# **list_test_runs**
> TestrunresultListTestRunsResponse list_test_runs(project_id=project_id, page_token=page_token, first_page_query_project_id_uuid=first_page_query_project_id_uuid, first_page_query_testing_type=first_page_query_testing_type, first_page_query_schedule_id_uuid=first_page_query_schedule_id_uuid, page_size=page_size)

ListTestRuns

Lists all test runs belonging to a project.  #### Python pagination example:  ```python all_objects = [] # Required for authentication to all methods in the API. headers = {\"rime-api-key\": \"INSERT_API_TOKEN\"} # TODO page_token = \"\" # Initialize query parameters in a dictionary params = {\"INSERT_QUERY_PARAMETER\": \"INSERT_QUERY_VALUE\"} # TODO # Make requests until all results have been returned. while True:     # If the page_token from a previous response is not empty, we need to specify this     # token as a parameter to the next request in order to return the next page.     if page_token != \"\":         params = {\"page_token\": page_token}     res = requests.get(\"INSERT_METHOD_URI\", params=params, headers=headers) # TODO     if res.status_code != 200 :         raise ValueError(res)     res_json = res.json()     all_objects.extend(res_json['INSERT_OBJECT_KEY']) # TODO     page_token = res_json['nextPageToken']     # If all results have been returned, res_json['hasMore'] is false.     if not res_json[\"hasMore\"]:         break ```

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_list_test_runs_response import TestrunresultListTestRunsResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    project_id = 'project_id_example' # str | The field is deprecated in v2.2. Use first_page_query.project_id instead. The field will be removed after v2.3. The ID of the project containing the requested test runs. Specify exactly one of the page_token field or this field. (optional)
    page_token = 'page_token_example' # str | A token representing one page from the list returned by a ListTestRuns query. The ListTestRuns query returns a page_token when there is more than one page of results. Specify exactly one of the projectId field or this field. (optional)
    first_page_query_project_id_uuid = 'first_page_query_project_id_uuid_example' # str | Unique object ID. (optional)
    first_page_query_testing_type = 'TEST_TYPE_STRESS_TESTING_UNSPECIFIED' # str | The test type of Test Runs to request. Defaults to Stress Testing.   - TEST_TYPE_STRESS_TESTING_UNSPECIFIED: Default type as stress testing (optional) (default to 'TEST_TYPE_STRESS_TESTING_UNSPECIFIED')
    first_page_query_schedule_id_uuid = 'first_page_query_schedule_id_uuid_example' # str | Unique object ID. (optional)
    page_size = 'page_size_example' # str | The maximum number of Test Run objects to return in a single page. (optional)

    try:
        # ListTestRuns
        api_response = api_instance.list_test_runs(project_id=project_id, page_token=page_token, first_page_query_project_id_uuid=first_page_query_project_id_uuid, first_page_query_testing_type=first_page_query_testing_type, first_page_query_schedule_id_uuid=first_page_query_schedule_id_uuid, page_size=page_size)
        print("The response of ResultsReaderApi->list_test_runs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->list_test_runs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| The field is deprecated in v2.2. Use first_page_query.project_id instead. The field will be removed after v2.3. The ID of the project containing the requested test runs. Specify exactly one of the page_token field or this field. | [optional] 
 **page_token** | **str**| A token representing one page from the list returned by a ListTestRuns query. The ListTestRuns query returns a page_token when there is more than one page of results. Specify exactly one of the projectId field or this field. | [optional] 
 **first_page_query_project_id_uuid** | **str**| Unique object ID. | [optional] 
 **first_page_query_testing_type** | **str**| The test type of Test Runs to request. Defaults to Stress Testing.   - TEST_TYPE_STRESS_TESTING_UNSPECIFIED: Default type as stress testing | [optional] [default to &#39;TEST_TYPE_STRESS_TESTING_UNSPECIFIED&#39;]
 **first_page_query_schedule_id_uuid** | **str**| Unique object ID. | [optional] 
 **page_size** | **str**| The maximum number of Test Run objects to return in a single page. | [optional] 

### Return type

[**TestrunresultListTestRunsResponse**](TestrunresultListTestRunsResponse.md)

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

# **list_validation_categories**
> TestrunresultListValidationCategoriesResponse list_validation_categories()

ListValidationCategories

Returns test categories belongs to validation.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_list_validation_categories_response import TestrunresultListValidationCategoriesResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)

    try:
        # ListValidationCategories
        api_response = api_instance.list_validation_categories()
        print("The response of ResultsReaderApi->list_validation_categories:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->list_validation_categories: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**TestrunresultListValidationCategoriesResponse**](TestrunresultListValidationCategoriesResponse.md)

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

# **rename_test_run**
> TestrunresultRenameTestRunResponse rename_test_run(test_run_id, body)

RenameTestRun

Updates the name of a test run.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rename_test_run_request import RenameTestRunRequest
from ri.apiclient.models.testrunresult_rename_test_run_response import TestrunresultRenameTestRunResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    test_run_id = 'test_run_id_example' # str | Uniquely specifies a Test Run to rename.
    body = ri.apiclient.RenameTestRunRequest() # RenameTestRunRequest | 

    try:
        # RenameTestRun
        api_response = api_instance.rename_test_run(test_run_id, body)
        print("The response of ResultsReaderApi->rename_test_run:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->rename_test_run: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_run_id** | **str**| Uniquely specifies a Test Run to rename. | 
 **body** | [**RenameTestRunRequest**](RenameTestRunRequest.md)|  | 

### Return type

[**TestrunresultRenameTestRunResponse**](TestrunresultRenameTestRunResponse.md)

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

# **results_reader_list_batch_results**
> TestrunresultListBatchResultsResponse results_reader_list_batch_results(test_run_id=test_run_id, page_token=page_token, page_size=page_size, show_display=show_display)

ListBatchResults

Returns a paginated list of batch results from a test run.  #### Python pagination example:  ```python all_objects = [] # Required for authentication to all methods in the API. headers = {\"rime-api-key\": \"INSERT_API_TOKEN\"} # TODO page_token = \"\" # Initialize query parameters in a dictionary params = {\"INSERT_QUERY_PARAMETER\": \"INSERT_QUERY_VALUE\"} # TODO # Make requests until all results have been returned. while True:     # If the page_token from a previous response is not empty, we need to specify this     # token as a parameter to the next request in order to return the next page.     if page_token != \"\":         params = {\"page_token\": page_token}     res = requests.get(\"INSERT_METHOD_URI\", params=params, headers=headers) # TODO     if res.status_code != 200 :         raise ValueError(res)     res_json = res.json()     all_objects.extend(res_json['INSERT_OBJECT_KEY']) # TODO     page_token = res_json['nextPageToken']     # If all results have been returned, res_json['hasMore'] is false.     if not res_json[\"hasMore\"]:         break ```

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.testrunresult_list_batch_results_response import TestrunresultListBatchResultsResponse
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
    api_instance = ri.apiclient.ResultsReaderApi(api_client)
    test_run_id = 'test_run_id_example' # str | The ID of the Test Run associated with batch results. Specify exactly one of the pageToken field or this field. (optional)
    page_token = 'page_token_example' # str | A token representing one page from the list returned by a ListBatchResults query. The ListBatchResults query returns a page_token when there is more than one page of results. Specify exactly one of the testRunId field or this field. (optional)
    page_size = 'page_size_example' # str | The maximum number of Batch Result objects to return in a single page. (optional)
    show_display = True # bool | A Boolean that toggles whether to return display html info. (optional)

    try:
        # ListBatchResults
        api_response = api_instance.results_reader_list_batch_results(test_run_id=test_run_id, page_token=page_token, page_size=page_size, show_display=show_display)
        print("The response of ResultsReaderApi->results_reader_list_batch_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsReaderApi->results_reader_list_batch_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_run_id** | **str**| The ID of the Test Run associated with batch results. Specify exactly one of the pageToken field or this field. | [optional] 
 **page_token** | **str**| A token representing one page from the list returned by a ListBatchResults query. The ListBatchResults query returns a page_token when there is more than one page of results. Specify exactly one of the testRunId field or this field. | [optional] 
 **page_size** | **str**| The maximum number of Batch Result objects to return in a single page. | [optional] 
 **show_display** | **bool**| A Boolean that toggles whether to return display html info. | [optional] 

### Return type

[**TestrunresultListBatchResultsResponse**](TestrunresultListBatchResultsResponse.md)

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

