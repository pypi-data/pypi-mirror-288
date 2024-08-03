# ri.apiclient.DataCollectorApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_datapoints**](DataCollectorApi.md#get_datapoints) | **GET** /v1-beta/data-collector/datapoints/{dataStreamId.uuid} | GetDatapoints
[**get_predictions**](DataCollectorApi.md#get_predictions) | **GET** /v1-beta/data-collector/predictions/{modelId.uuid}/{dataStreamId.uuid} | GetPredictions
[**register_data_stream**](DataCollectorApi.md#register_data_stream) | **POST** /v1-beta/data-collector/datastream/{projectId.uuid} | RegisterDataStream
[**store_datapoints**](DataCollectorApi.md#store_datapoints) | **PUT** /v1-beta/data-collector/data/{dataStreamId.uuid} | StoreDatapoints
[**store_predictions**](DataCollectorApi.md#store_predictions) | **PUT** /v1-beta/data-collector/predictions/{modelId.uuid} | StorePredictions


# **get_datapoints**
> StreamResultOfRimeGetDatapointsResponse get_datapoints(data_stream_id_uuid, time_interval_start_time=time_interval_start_time, time_interval_end_time=time_interval_end_time)

GetDatapoints

GetDatapoints returns all datapoints from a time period.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.stream_result_of_rime_get_datapoints_response import StreamResultOfRimeGetDatapointsResponse
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
    api_instance = ri.apiclient.DataCollectorApi(api_client)
    data_stream_id_uuid = 'data_stream_id_uuid_example' # str | Unique object ID.
    time_interval_start_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    time_interval_end_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # GetDatapoints
        api_response = api_instance.get_datapoints(data_stream_id_uuid, time_interval_start_time=time_interval_start_time, time_interval_end_time=time_interval_end_time)
        print("The response of DataCollectorApi->get_datapoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataCollectorApi->get_datapoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_stream_id_uuid** | **str**| Unique object ID. | 
 **time_interval_start_time** | **datetime**|  | [optional] 
 **time_interval_end_time** | **datetime**|  | [optional] 

### Return type

[**StreamResultOfRimeGetDatapointsResponse**](StreamResultOfRimeGetDatapointsResponse.md)

### Authorization

[rime-api-key](../README.md#rime-api-key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response.(streaming responses) |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_predictions**
> StreamResultOfRimeGetPredictionsResponse get_predictions(model_id_uuid, data_stream_id_uuid, time_interval_start_time=time_interval_start_time, time_interval_end_time=time_interval_end_time)

GetPredictions

GetPredictions returns all predictions from a time period

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.stream_result_of_rime_get_predictions_response import StreamResultOfRimeGetPredictionsResponse
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
    api_instance = ri.apiclient.DataCollectorApi(api_client)
    model_id_uuid = 'model_id_uuid_example' # str | Unique object ID.
    data_stream_id_uuid = 'data_stream_id_uuid_example' # str | Unique object ID.
    time_interval_start_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    time_interval_end_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)

    try:
        # GetPredictions
        api_response = api_instance.get_predictions(model_id_uuid, data_stream_id_uuid, time_interval_start_time=time_interval_start_time, time_interval_end_time=time_interval_end_time)
        print("The response of DataCollectorApi->get_predictions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataCollectorApi->get_predictions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_id_uuid** | **str**| Unique object ID. | 
 **data_stream_id_uuid** | **str**| Unique object ID. | 
 **time_interval_start_time** | **datetime**|  | [optional] 
 **time_interval_end_time** | **datetime**|  | [optional] 

### Return type

[**StreamResultOfRimeGetPredictionsResponse**](StreamResultOfRimeGetPredictionsResponse.md)

### Authorization

[rime-api-key](../README.md#rime-api-key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response.(streaming responses) |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_data_stream**
> RimeRegisterDataStreamResponse register_data_stream(project_id_uuid, body)

RegisterDataStream

Registers a new data stream. A data stream is a location where data points are stored. All data points that are in the same registered data set must be stored in the same data stream.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.register_data_stream_request import RegisterDataStreamRequest
from ri.apiclient.models.rime_register_data_stream_response import RimeRegisterDataStreamResponse
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
    api_instance = ri.apiclient.DataCollectorApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.RegisterDataStreamRequest() # RegisterDataStreamRequest | 

    try:
        # RegisterDataStream
        api_response = api_instance.register_data_stream(project_id_uuid, body)
        print("The response of DataCollectorApi->register_data_stream:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataCollectorApi->register_data_stream: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **body** | [**RegisterDataStreamRequest**](RegisterDataStreamRequest.md)|  | 

### Return type

[**RimeRegisterDataStreamResponse**](RimeRegisterDataStreamResponse.md)

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

# **store_datapoints**
> RimeStoreDatapointsResponse store_datapoints(data_stream_id_uuid, body)

StoreDatapoints

Store multiple new datapoints into a data stream.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_store_datapoints_response import RimeStoreDatapointsResponse
from ri.apiclient.models.store_datapoints_request import StoreDatapointsRequest
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
    api_instance = ri.apiclient.DataCollectorApi(api_client)
    data_stream_id_uuid = 'data_stream_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.StoreDatapointsRequest() # StoreDatapointsRequest | 

    try:
        # StoreDatapoints
        api_response = api_instance.store_datapoints(data_stream_id_uuid, body)
        print("The response of DataCollectorApi->store_datapoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataCollectorApi->store_datapoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_stream_id_uuid** | **str**| Unique object ID. | 
 **body** | [**StoreDatapointsRequest**](StoreDatapointsRequest.md)|  | 

### Return type

[**RimeStoreDatapointsResponse**](RimeStoreDatapointsResponse.md)

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

# **store_predictions**
> object store_predictions(model_id_uuid, body)

StorePredictions

Store multiple new predictions.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.store_predictions_request import StorePredictionsRequest
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
    api_instance = ri.apiclient.DataCollectorApi(api_client)
    model_id_uuid = 'model_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.StorePredictionsRequest() # StorePredictionsRequest | 

    try:
        # StorePredictions
        api_response = api_instance.store_predictions(model_id_uuid, body)
        print("The response of DataCollectorApi->store_predictions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataCollectorApi->store_predictions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_id_uuid** | **str**| Unique object ID. | 
 **body** | [**StorePredictionsRequest**](StorePredictionsRequest.md)|  | 

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

