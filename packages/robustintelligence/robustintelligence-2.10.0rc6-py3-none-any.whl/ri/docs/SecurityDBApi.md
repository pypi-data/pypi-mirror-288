# ri.apiclient.SecurityDBApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_model_security_report**](SecurityDBApi.md#get_model_security_report) | **GET** /v1-beta/security-report/model | GetModelSecurityReport
[**list_model_security_reports**](SecurityDBApi.md#list_model_security_reports) | **GET** /v1-beta/security-report/models | ListModelSecurityReports


# **get_model_security_report**
> RimeGetModelSecurityReportResponse get_model_security_report(repo_id)

GetModelSecurityReport

Returns the supply chain risk report for a Hugging Face model.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_model_security_report_response import RimeGetModelSecurityReportResponse
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
    api_instance = ri.apiclient.SecurityDBApi(api_client)
    repo_id = 'repo_id_example' # str | The ID of the model repository on Hugging Face.

    try:
        # GetModelSecurityReport
        api_response = api_instance.get_model_security_report(repo_id)
        print("The response of SecurityDBApi->get_model_security_report:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecurityDBApi->get_model_security_report: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repo_id** | **str**| The ID of the model repository on Hugging Face. | 

### Return type

[**RimeGetModelSecurityReportResponse**](RimeGetModelSecurityReportResponse.md)

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

# **list_model_security_reports**
> RimeListModelSecurityReportsResponse list_model_security_reports(page_token=page_token, page_size=page_size)

ListModelSecurityReports

Returns all supply chain risk reports for the workspace.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_model_security_reports_response import RimeListModelSecurityReportsResponse
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
    api_instance = ri.apiclient.SecurityDBApi(api_client)
    page_token = 'page_token_example' # str | A token representing one page from the list returned by a ListModelSecurityReports API. The ListModelSecurityReports API returns a page_token when there is more than one page of results. (optional)
    page_size = 'page_size_example' # str | The maximum number of objects to return in a single page. Maximum page size is 1000. (optional)

    try:
        # ListModelSecurityReports
        api_response = api_instance.list_model_security_reports(page_token=page_token, page_size=page_size)
        print("The response of SecurityDBApi->list_model_security_reports:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SecurityDBApi->list_model_security_reports: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_token** | **str**| A token representing one page from the list returned by a ListModelSecurityReports API. The ListModelSecurityReports API returns a page_token when there is more than one page of results. | [optional] 
 **page_size** | **str**| The maximum number of objects to return in a single page. Maximum page size is 1000. | [optional] 

### Return type

[**RimeListModelSecurityReportsResponse**](RimeListModelSecurityReportsResponse.md)

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

