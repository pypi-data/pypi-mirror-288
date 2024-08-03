# ri.apiclient.ModelTestingApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**start_continuous_test**](ModelTestingApi.md#start_continuous_test) | **POST** /v1/continuous-tests/{firewallId.uuid} | StartContinuousTest
[**start_file_scan**](ModelTestingApi.md#start_file_scan) | **POST** /v1-beta/file-scans | StartFileScan
[**start_stress_test**](ModelTestingApi.md#start_stress_test) | **POST** /v1/stress-tests/{projectId.uuid} | StartStressTest


# **start_continuous_test**
> RimeStartContinuousTestResponse start_continuous_test(firewall_id_uuid, body)

StartContinuousTest

Starts a Continuous Test and returns a Job object containing metadata for the Test Run.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_start_continuous_test_response import RimeStartContinuousTestResponse
from ri.apiclient.models.start_continuous_test_request import StartContinuousTestRequest
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
    api_instance = ri.apiclient.ModelTestingApi(api_client)
    firewall_id_uuid = 'firewall_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.StartContinuousTestRequest() # StartContinuousTestRequest | 

    try:
        # StartContinuousTest
        api_response = api_instance.start_continuous_test(firewall_id_uuid, body)
        print("The response of ModelTestingApi->start_continuous_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelTestingApi->start_continuous_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_id_uuid** | **str**| Unique object ID. | 
 **body** | [**StartContinuousTestRequest**](StartContinuousTestRequest.md)|  | 

### Return type

[**RimeStartContinuousTestResponse**](RimeStartContinuousTestResponse.md)

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

# **start_file_scan**
> RimeStartFileScanResponse start_file_scan(body)

StartFileScan

Starts a File Scan for the specified model.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_start_file_scan_request import RimeStartFileScanRequest
from ri.apiclient.models.rime_start_file_scan_response import RimeStartFileScanResponse
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
    api_instance = ri.apiclient.ModelTestingApi(api_client)
    body = ri.apiclient.RimeStartFileScanRequest() # RimeStartFileScanRequest | 

    try:
        # StartFileScan
        api_response = api_instance.start_file_scan(body)
        print("The response of ModelTestingApi->start_file_scan:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelTestingApi->start_file_scan: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeStartFileScanRequest**](RimeStartFileScanRequest.md)|  | 

### Return type

[**RimeStartFileScanResponse**](RimeStartFileScanResponse.md)

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

# **start_stress_test**
> RimeStartStressTestResponse start_stress_test(project_id_uuid, body)

StartStressTest

Starts a Stress Test and returns a Job object containing metadata for the Test Run.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_start_stress_test_response import RimeStartStressTestResponse
from ri.apiclient.models.start_stress_test_request import StartStressTestRequest
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
    api_instance = ri.apiclient.ModelTestingApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.StartStressTestRequest() # StartStressTestRequest | 

    try:
        # StartStressTest
        api_response = api_instance.start_stress_test(project_id_uuid, body)
        print("The response of ModelTestingApi->start_stress_test:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelTestingApi->start_stress_test: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **body** | [**StartStressTestRequest**](StartStressTestRequest.md)|  | 

### Return type

[**RimeStartStressTestResponse**](RimeStartStressTestResponse.md)

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

