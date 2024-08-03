# ri.apiclient.FileScanningApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_file_scan_result**](FileScanningApi.md#delete_file_scan_result) | **DELETE** /v1-beta/file-scan-results/{fileScanId.uuid} | DeleteFileScanResult
[**get_file_scan_result**](FileScanningApi.md#get_file_scan_result) | **GET** /v1-beta/file-scan-results/{fileScanId.uuid} | GetFileScanResult
[**list_file_scan_results**](FileScanningApi.md#list_file_scan_results) | **GET** /v1-beta/file-scan-results | ListFileScanResults


# **delete_file_scan_result**
> object delete_file_scan_result(file_scan_id_uuid)

DeleteFileScanResult

Deletes a File Scan result by ID.

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
    api_instance = ri.apiclient.FileScanningApi(api_client)
    file_scan_id_uuid = 'file_scan_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteFileScanResult
        api_response = api_instance.delete_file_scan_result(file_scan_id_uuid)
        print("The response of FileScanningApi->delete_file_scan_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileScanningApi->delete_file_scan_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_scan_id_uuid** | **str**| Unique object ID. | 

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

# **get_file_scan_result**
> RimeGetFileScanResultResponse get_file_scan_result(file_scan_id_uuid)

GetFileScanResult

Returns a File Scan result by ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_file_scan_result_response import RimeGetFileScanResultResponse
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
    api_instance = ri.apiclient.FileScanningApi(api_client)
    file_scan_id_uuid = 'file_scan_id_uuid_example' # str | Unique object ID.

    try:
        # GetFileScanResult
        api_response = api_instance.get_file_scan_result(file_scan_id_uuid)
        print("The response of FileScanningApi->get_file_scan_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileScanningApi->get_file_scan_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_scan_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeGetFileScanResultResponse**](RimeGetFileScanResultResponse.md)

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

# **list_file_scan_results**
> RimeListFileScanResultsResponse list_file_scan_results(first_page_query_project_id_uuid=first_page_query_project_id_uuid, first_page_query_model_id_uuid=first_page_query_model_id_uuid, page_token=page_token, page_size=page_size)

ListFileScanResults

Returns a paginated list of all File Scan results for the project.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_file_scan_results_response import RimeListFileScanResultsResponse
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
    api_instance = ri.apiclient.FileScanningApi(api_client)
    first_page_query_project_id_uuid = 'first_page_query_project_id_uuid_example' # str | Unique object ID. (optional)
    first_page_query_model_id_uuid = 'first_page_query_model_id_uuid_example' # str | Unique object ID. (optional)
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListFileScan query beyond the first page. (optional)
    page_size = 'page_size_example' # str | Defines the maximum number of results on a given page. API call pagination navigates through the entire set of results in groups of the specified page size. (optional)

    try:
        # ListFileScanResults
        api_response = api_instance.list_file_scan_results(first_page_query_project_id_uuid=first_page_query_project_id_uuid, first_page_query_model_id_uuid=first_page_query_model_id_uuid, page_token=page_token, page_size=page_size)
        print("The response of FileScanningApi->list_file_scan_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileScanningApi->list_file_scan_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **first_page_query_project_id_uuid** | **str**| Unique object ID. | [optional] 
 **first_page_query_model_id_uuid** | **str**| Unique object ID. | [optional] 
 **page_token** | **str**| Specifies a page of the list returned by a ListFileScan query beyond the first page. | [optional] 
 **page_size** | **str**| Defines the maximum number of results on a given page. API call pagination navigates through the entire set of results in groups of the specified page size. | [optional] 

### Return type

[**RimeListFileScanResultsResponse**](RimeListFileScanResultsResponse.md)

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

