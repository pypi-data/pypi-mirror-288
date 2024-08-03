# ri.apiclient.MonitorServiceApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_custom_monitor**](MonitorServiceApi.md#create_custom_monitor) | **POST** /v1-beta/custom-monitors/{name} | CreateCustomMonitor
[**delete_custom_monitor**](MonitorServiceApi.md#delete_custom_monitor) | **DELETE** /v1-beta/custom-monitors/{monitorId.uuid} | DeleteCustomMonitor
[**get_monitor_result**](MonitorServiceApi.md#get_monitor_result) | **GET** /v1-beta/monitors/result/{monitorId.uuid} | GetMonitorResult
[**list_metric_identifiers**](MonitorServiceApi.md#list_metric_identifiers) | **GET** /v1-beta/custom-monitors/metrics/{firewallId.uuid} | ListMetricIdentifiers
[**list_monitors**](MonitorServiceApi.md#list_monitors) | **GET** /v1-beta/monitors/{firewallId.uuid} | ListMonitors
[**update_monitor**](MonitorServiceApi.md#update_monitor) | **PUT** /v1-beta/monitors/{monitor.id.uuid} | UpdateMonitor


# **create_custom_monitor**
> RimeCreateCustomMonitorResponse create_custom_monitor(name, body)

CreateCustomMonitor

Create a new custom monitor

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.create_custom_monitor_request import CreateCustomMonitorRequest
from ri.apiclient.models.rime_create_custom_monitor_response import RimeCreateCustomMonitorResponse
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
    api_instance = ri.apiclient.MonitorServiceApi(api_client)
    name = 'name_example' # str | The name of the monitor.
    body = ri.apiclient.CreateCustomMonitorRequest() # CreateCustomMonitorRequest | 

    try:
        # CreateCustomMonitor
        api_response = api_instance.create_custom_monitor(name, body)
        print("The response of MonitorServiceApi->create_custom_monitor:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MonitorServiceApi->create_custom_monitor: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| The name of the monitor. | 
 **body** | [**CreateCustomMonitorRequest**](CreateCustomMonitorRequest.md)|  | 

### Return type

[**RimeCreateCustomMonitorResponse**](RimeCreateCustomMonitorResponse.md)

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

# **delete_custom_monitor**
> object delete_custom_monitor(monitor_id_uuid)

DeleteCustomMonitor

Delete a custom monitor

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
    api_instance = ri.apiclient.MonitorServiceApi(api_client)
    monitor_id_uuid = 'monitor_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteCustomMonitor
        api_response = api_instance.delete_custom_monitor(monitor_id_uuid)
        print("The response of MonitorServiceApi->delete_custom_monitor:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MonitorServiceApi->delete_custom_monitor: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **monitor_id_uuid** | **str**| Unique object ID. | 

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

# **get_monitor_result**
> RimeGetMonitorResultResponse get_monitor_result(monitor_id_uuid, time_interval_start_time=time_interval_start_time, time_interval_end_time=time_interval_end_time)

GetMonitorResult

Graph a monitor within a time range

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_monitor_result_response import RimeGetMonitorResultResponse
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
    api_instance = ri.apiclient.MonitorServiceApi(api_client)
    monitor_id_uuid = 'monitor_id_uuid_example' # str | Unique object ID.
    time_interval_start_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    time_interval_end_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # GetMonitorResult
        api_response = api_instance.get_monitor_result(monitor_id_uuid, time_interval_start_time=time_interval_start_time, time_interval_end_time=time_interval_end_time)
        print("The response of MonitorServiceApi->get_monitor_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MonitorServiceApi->get_monitor_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **monitor_id_uuid** | **str**| Unique object ID. | 
 **time_interval_start_time** | **datetime**|  | [optional] 
 **time_interval_end_time** | **datetime**|  | [optional] 

### Return type

[**RimeGetMonitorResultResponse**](RimeGetMonitorResultResponse.md)

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

# **list_metric_identifiers**
> RimeListMetricIdentifiersResponse list_metric_identifiers(firewall_id_uuid)

ListMetricIdentifiers

List all possible Custom Monitor Metric Identifiers

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_metric_identifiers_response import RimeListMetricIdentifiersResponse
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
    api_instance = ri.apiclient.MonitorServiceApi(api_client)
    firewall_id_uuid = 'firewall_id_uuid_example' # str | Unique object ID.

    try:
        # ListMetricIdentifiers
        api_response = api_instance.list_metric_identifiers(firewall_id_uuid)
        print("The response of MonitorServiceApi->list_metric_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MonitorServiceApi->list_metric_identifiers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeListMetricIdentifiersResponse**](RimeListMetricIdentifiersResponse.md)

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

# **list_monitors**
> RimeListMonitorsResponse list_monitors(firewall_id_uuid, first_page_req_included_monitor_types=first_page_req_included_monitor_types, first_page_req_included_risk_category_types=first_page_req_included_risk_category_types, first_page_req_pinned_monitors_only=first_page_req_pinned_monitors_only, page_token=page_token, page_size=page_size)

ListMonitors

lists monitors by firewall ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_monitors_response import RimeListMonitorsResponse
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
    api_instance = ri.apiclient.MonitorServiceApi(api_client)
    firewall_id_uuid = 'firewall_id_uuid_example' # str | Unique object ID.
    first_page_req_included_monitor_types = ['first_page_req_included_monitor_types_example'] # List[str] | Specifies a list of monitor types. Filters results to match the specified monitor types. (optional)
    first_page_req_included_risk_category_types = ['first_page_req_included_risk_category_types_example'] # List[str] | Specifies a list of risk category types. Filters results to match the specified risk category types. (optional)
    first_page_req_pinned_monitors_only = True # bool | When the value of this Boolean is True, this endpoint returns a list of pinned Monitors. Otherwise, this endpoint does not filter Monitors by pinned status. (optional)
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListMonitors query. The ListMonitors query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageReq field. (optional)
    page_size = 'page_size_example' # str | The maximum number of Monitor objects to return in a single page. (optional)

    try:
        # ListMonitors
        api_response = api_instance.list_monitors(firewall_id_uuid, first_page_req_included_monitor_types=first_page_req_included_monitor_types, first_page_req_included_risk_category_types=first_page_req_included_risk_category_types, first_page_req_pinned_monitors_only=first_page_req_pinned_monitors_only, page_token=page_token, page_size=page_size)
        print("The response of MonitorServiceApi->list_monitors:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MonitorServiceApi->list_monitors: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_id_uuid** | **str**| Unique object ID. | 
 **first_page_req_included_monitor_types** | [**List[str]**](str.md)| Specifies a list of monitor types. Filters results to match the specified monitor types. | [optional] 
 **first_page_req_included_risk_category_types** | [**List[str]**](str.md)| Specifies a list of risk category types. Filters results to match the specified risk category types. | [optional] 
 **first_page_req_pinned_monitors_only** | **bool**| When the value of this Boolean is True, this endpoint returns a list of pinned Monitors. Otherwise, this endpoint does not filter Monitors by pinned status. | [optional] 
 **page_token** | **str**| Specifies a page of the list returned by a ListMonitors query. The ListMonitors query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageReq field. | [optional] 
 **page_size** | **str**| The maximum number of Monitor objects to return in a single page. | [optional] 

### Return type

[**RimeListMonitorsResponse**](RimeListMonitorsResponse.md)

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

# **update_monitor**
> RimeUpdateMonitorResponse update_monitor(monitor_id_uuid, body)

UpdateMonitor

Updates a monitor.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_update_monitor_response import RimeUpdateMonitorResponse
from ri.apiclient.models.update_monitor_request import UpdateMonitorRequest
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
    api_instance = ri.apiclient.MonitorServiceApi(api_client)
    monitor_id_uuid = 'monitor_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.UpdateMonitorRequest() # UpdateMonitorRequest | 

    try:
        # UpdateMonitor
        api_response = api_instance.update_monitor(monitor_id_uuid, body)
        print("The response of MonitorServiceApi->update_monitor:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MonitorServiceApi->update_monitor: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **monitor_id_uuid** | **str**| Unique object ID. | 
 **body** | [**UpdateMonitorRequest**](UpdateMonitorRequest.md)|  | 

### Return type

[**RimeUpdateMonitorResponse**](RimeUpdateMonitorResponse.md)

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

