# ri.apiclient.ScheduleServiceApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_schedule**](ScheduleServiceApi.md#create_schedule) | **POST** /v1-beta/schedules | CreateSchedule creates a schedule.
[**delete_schedule**](ScheduleServiceApi.md#delete_schedule) | **DELETE** /v1-beta/schedules/{scheduleId.uuid} | DeleteSchedule deletes a schedule.
[**get_schedule**](ScheduleServiceApi.md#get_schedule) | **GET** /v1-beta/schedules/{scheduleId.uuid} | GetSchedule gets a schedule.
[**update_schedule**](ScheduleServiceApi.md#update_schedule) | **PATCH** /v1-beta/schedules/{schedule.scheduleId.uuid} | UpdateSchedule updates a schedule.


# **create_schedule**
> RimeCreateScheduleResponse create_schedule(body)

CreateSchedule creates a schedule.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_create_schedule_request import RimeCreateScheduleRequest
from ri.apiclient.models.rime_create_schedule_response import RimeCreateScheduleResponse
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
    api_instance = ri.apiclient.ScheduleServiceApi(api_client)
    body = ri.apiclient.RimeCreateScheduleRequest() # RimeCreateScheduleRequest | 

    try:
        # CreateSchedule creates a schedule.
        api_response = api_instance.create_schedule(body)
        print("The response of ScheduleServiceApi->create_schedule:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScheduleServiceApi->create_schedule: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeCreateScheduleRequest**](RimeCreateScheduleRequest.md)|  | 

### Return type

[**RimeCreateScheduleResponse**](RimeCreateScheduleResponse.md)

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

# **delete_schedule**
> object delete_schedule(schedule_id_uuid)

DeleteSchedule deletes a schedule.

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
    api_instance = ri.apiclient.ScheduleServiceApi(api_client)
    schedule_id_uuid = 'schedule_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteSchedule deletes a schedule.
        api_response = api_instance.delete_schedule(schedule_id_uuid)
        print("The response of ScheduleServiceApi->delete_schedule:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScheduleServiceApi->delete_schedule: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **schedule_id_uuid** | **str**| Unique object ID. | 

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

# **get_schedule**
> RimeGetScheduleResponse get_schedule(schedule_id_uuid)

GetSchedule gets a schedule.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_schedule_response import RimeGetScheduleResponse
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
    api_instance = ri.apiclient.ScheduleServiceApi(api_client)
    schedule_id_uuid = 'schedule_id_uuid_example' # str | Unique object ID.

    try:
        # GetSchedule gets a schedule.
        api_response = api_instance.get_schedule(schedule_id_uuid)
        print("The response of ScheduleServiceApi->get_schedule:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScheduleServiceApi->get_schedule: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **schedule_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeGetScheduleResponse**](RimeGetScheduleResponse.md)

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

# **update_schedule**
> RimeUpdateScheduleResponse update_schedule(schedule_schedule_id_uuid, mask, schedule)

UpdateSchedule updates a schedule.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_update_schedule_response import RimeUpdateScheduleResponse
from ri.apiclient.models.update_schedule_request import UpdateScheduleRequest
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
    api_instance = ri.apiclient.ScheduleServiceApi(api_client)
    schedule_schedule_id_uuid = 'schedule_schedule_id_uuid_example' # str | Unique object ID.
    mask = 'mask_example' # str | Update mask specifies the fields in the config that will be updated. Any values not in the mask will be ignored. Currently only updated the frequency of the schedule is supported.
    schedule = ri.apiclient.UpdateScheduleRequest() # UpdateScheduleRequest | 

    try:
        # UpdateSchedule updates a schedule.
        api_response = api_instance.update_schedule(schedule_schedule_id_uuid, mask, schedule)
        print("The response of ScheduleServiceApi->update_schedule:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScheduleServiceApi->update_schedule: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **schedule_schedule_id_uuid** | **str**| Unique object ID. | 
 **mask** | **str**| Update mask specifies the fields in the config that will be updated. Any values not in the mask will be ignored. Currently only updated the frequency of the schedule is supported. | 
 **schedule** | [**UpdateScheduleRequest**](UpdateScheduleRequest.md)|  | 

### Return type

[**RimeUpdateScheduleResponse**](RimeUpdateScheduleResponse.md)

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

