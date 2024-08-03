# ri.apiclient.RegistryServiceApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_dataset**](RegistryServiceApi.md#delete_dataset) | **DELETE** /v1/registry/dataset/{datasetId} | DeleteDataset
[**delete_model**](RegistryServiceApi.md#delete_model) | **DELETE** /v1/registry/model/{modelId.uuid} | DeleteModel
[**delete_prediction_set**](RegistryServiceApi.md#delete_prediction_set) | **DELETE** /v1/registry/prediction/{modelId.uuid}/{datasetId} | DeletePredictionSet
[**get_dataset**](RegistryServiceApi.md#get_dataset) | **GET** /v1/registry/dataset | GetDataset
[**get_model**](RegistryServiceApi.md#get_model) | **GET** /v1/registry/model | GetModel
[**get_prediction_set**](RegistryServiceApi.md#get_prediction_set) | **GET** /v1/registry/prediction/{modelId.uuid}/{datasetId} | GetPredictionSet
[**list_datasets**](RegistryServiceApi.md#list_datasets) | **GET** /v1/registry/{projectId.uuid}/dataset | ListDatasets
[**list_models**](RegistryServiceApi.md#list_models) | **GET** /v1/registry/{projectId.uuid}/model | ListModels
[**list_prediction_sets**](RegistryServiceApi.md#list_prediction_sets) | **GET** /v1/registry/{projectId.uuid}/prediction | ListPredictionSets
[**register_dataset**](RegistryServiceApi.md#register_dataset) | **POST** /v1/registry/{projectId.uuid}/dataset | RegisterDataset
[**register_model**](RegistryServiceApi.md#register_model) | **POST** /v1/registry/{projectId.uuid}/model | RegisterModel
[**register_prediction_set**](RegistryServiceApi.md#register_prediction_set) | **POST** /v1/registry/{projectId.uuid}/model/{modelId.uuid}/dataset/{datasetId}/prediction | RegisterPredictionSet


# **delete_dataset**
> object delete_dataset(dataset_id)

DeleteDataset

Delete a Dataset from the Registry.

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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    dataset_id = 'dataset_id_example' # str | Uniquely specifies a Dataset.

    try:
        # DeleteDataset
        api_response = api_instance.delete_dataset(dataset_id)
        print("The response of RegistryServiceApi->delete_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->delete_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **str**| Uniquely specifies a Dataset. | 

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

# **delete_model**
> object delete_model(model_id_uuid)

DeleteModel

Delete a Model from the Registry.

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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    model_id_uuid = 'model_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteModel
        api_response = api_instance.delete_model(model_id_uuid)
        print("The response of RegistryServiceApi->delete_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->delete_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_id_uuid** | **str**| Unique object ID. | 

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

# **delete_prediction_set**
> object delete_prediction_set(model_id_uuid, dataset_id)

DeletePredictionSet

Delete the Prediction set corresponding to a specified Model and Dataset.

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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    model_id_uuid = 'model_id_uuid_example' # str | Unique object ID.
    dataset_id = 'dataset_id_example' # str | Uniquely specifies a Dataset.

    try:
        # DeletePredictionSet
        api_response = api_instance.delete_prediction_set(model_id_uuid, dataset_id)
        print("The response of RegistryServiceApi->delete_prediction_set:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->delete_prediction_set: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_id_uuid** | **str**| Unique object ID. | 
 **dataset_id** | **str**| Uniquely specifies a Dataset. | 

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

# **get_dataset**
> RimeGetDatasetResponse get_dataset(dataset_id=dataset_id, dataset_name=dataset_name)

GetDataset

Returns information about a registered Dataset. Allows for searching by ID or name.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_dataset_response import RimeGetDatasetResponse
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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    dataset_id = 'dataset_id_example' # str | Uniquely specifies a Dataset. (optional)
    dataset_name = 'dataset_name_example' # str | Unique name of a Dataset. (optional)

    try:
        # GetDataset
        api_response = api_instance.get_dataset(dataset_id=dataset_id, dataset_name=dataset_name)
        print("The response of RegistryServiceApi->get_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->get_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **dataset_id** | **str**| Uniquely specifies a Dataset. | [optional] 
 **dataset_name** | **str**| Unique name of a Dataset. | [optional] 

### Return type

[**RimeGetDatasetResponse**](RimeGetDatasetResponse.md)

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

# **get_model**
> RimeGetModelResponse get_model(model_id_uuid=model_id_uuid, model_name=model_name)

GetModel

Returns information about a registered Model. Allows for searching by ID or name.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_model_response import RimeGetModelResponse
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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    model_id_uuid = 'model_id_uuid_example' # str | Unique object ID. (optional)
    model_name = 'model_name_example' # str | Unique name of a Model. (optional)

    try:
        # GetModel
        api_response = api_instance.get_model(model_id_uuid=model_id_uuid, model_name=model_name)
        print("The response of RegistryServiceApi->get_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->get_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_id_uuid** | **str**| Unique object ID. | [optional] 
 **model_name** | **str**| Unique name of a Model. | [optional] 

### Return type

[**RimeGetModelResponse**](RimeGetModelResponse.md)

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

# **get_prediction_set**
> RimeGetPredictionSetResponse get_prediction_set(model_id_uuid, dataset_id)

GetPredictionSet

Returns information about a registered Prediction set.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_prediction_set_response import RimeGetPredictionSetResponse
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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    model_id_uuid = 'model_id_uuid_example' # str | Unique object ID.
    dataset_id = 'dataset_id_example' # str | Uniquely specifies a Dataset.

    try:
        # GetPredictionSet
        api_response = api_instance.get_prediction_set(model_id_uuid, dataset_id)
        print("The response of RegistryServiceApi->get_prediction_set:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->get_prediction_set: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_id_uuid** | **str**| Unique object ID. | 
 **dataset_id** | **str**| Uniquely specifies a Dataset. | 

### Return type

[**RimeGetPredictionSetResponse**](RimeGetPredictionSetResponse.md)

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

# **list_datasets**
> RimeListDatasetsResponse list_datasets(project_id_uuid, first_page_req_scheduled_ct_intervals_start_time=first_page_req_scheduled_ct_intervals_start_time, first_page_req_scheduled_ct_intervals_end_time=first_page_req_scheduled_ct_intervals_end_time, page_token=page_token, page_size=page_size)

ListDatasets

List all Datasets in the Registry with optional filters.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_datasets_response import RimeListDatasetsResponse
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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    first_page_req_scheduled_ct_intervals_start_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    first_page_req_scheduled_ct_intervals_end_time = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListDatasets query. The ListDatasets query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageReq field. (optional)
    page_size = 'page_size_example' # str | The maximum number of Dataset objects to return in a single page. (optional)

    try:
        # ListDatasets
        api_response = api_instance.list_datasets(project_id_uuid, first_page_req_scheduled_ct_intervals_start_time=first_page_req_scheduled_ct_intervals_start_time, first_page_req_scheduled_ct_intervals_end_time=first_page_req_scheduled_ct_intervals_end_time, page_token=page_token, page_size=page_size)
        print("The response of RegistryServiceApi->list_datasets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->list_datasets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **first_page_req_scheduled_ct_intervals_start_time** | **datetime**|  | [optional] 
 **first_page_req_scheduled_ct_intervals_end_time** | **datetime**|  | [optional] 
 **page_token** | **str**| Specifies a page of the list returned by a ListDatasets query. The ListDatasets query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageReq field. | [optional] 
 **page_size** | **str**| The maximum number of Dataset objects to return in a single page. | [optional] 

### Return type

[**RimeListDatasetsResponse**](RimeListDatasetsResponse.md)

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

# **list_models**
> RimeListModelsResponse list_models(project_id_uuid, page_token=page_token, page_size=page_size)

ListModels

List all Models in the Registry of the specified Project.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_models_response import RimeListModelsResponse
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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListModels query. The ListModels query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageReq field. (optional)
    page_size = 'page_size_example' # str | The maximum number of Model objects to return in a single page. (optional)

    try:
        # ListModels
        api_response = api_instance.list_models(project_id_uuid, page_token=page_token, page_size=page_size)
        print("The response of RegistryServiceApi->list_models:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->list_models: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **page_token** | **str**| Specifies a page of the list returned by a ListModels query. The ListModels query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageReq field. | [optional] 
 **page_size** | **str**| The maximum number of Model objects to return in a single page. | [optional] 

### Return type

[**RimeListModelsResponse**](RimeListModelsResponse.md)

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

# **list_prediction_sets**
> RimeListPredictionSetsResponse list_prediction_sets(project_id_uuid, first_page_req_model_id=first_page_req_model_id, first_page_req_dataset_id=first_page_req_dataset_id, page_token=page_token, page_size=page_size)

ListPredictionSets

List all Prediction sets in the Registry with optional filters.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_prediction_sets_response import RimeListPredictionSetsResponse
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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    first_page_req_model_id = 'first_page_req_model_id_example' # str | Uniquely specifies a Model. (optional)
    first_page_req_dataset_id = 'first_page_req_dataset_id_example' # str | Uniquely specifies a Dataset. (optional)
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListPredictions query. The ListPredictions query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageReq field. (optional)
    page_size = 'page_size_example' # str | The maximum number of Prediction objects to return in a single page. (optional)

    try:
        # ListPredictionSets
        api_response = api_instance.list_prediction_sets(project_id_uuid, first_page_req_model_id=first_page_req_model_id, first_page_req_dataset_id=first_page_req_dataset_id, page_token=page_token, page_size=page_size)
        print("The response of RegistryServiceApi->list_prediction_sets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->list_prediction_sets: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **first_page_req_model_id** | **str**| Uniquely specifies a Model. | [optional] 
 **first_page_req_dataset_id** | **str**| Uniquely specifies a Dataset. | [optional] 
 **page_token** | **str**| Specifies a page of the list returned by a ListPredictions query. The ListPredictions query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageReq field. | [optional] 
 **page_size** | **str**| The maximum number of Prediction objects to return in a single page. | [optional] 

### Return type

[**RimeListPredictionSetsResponse**](RimeListPredictionSetsResponse.md)

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

# **register_dataset**
> RimeRegisterDatasetResponse register_dataset(project_id_uuid, body)

RegisterDataset

Register a new Dataset for the specified Project.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.register_dataset_request import RegisterDatasetRequest
from ri.apiclient.models.rime_register_dataset_response import RimeRegisterDatasetResponse
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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.RegisterDatasetRequest() # RegisterDatasetRequest | 

    try:
        # RegisterDataset
        api_response = api_instance.register_dataset(project_id_uuid, body)
        print("The response of RegistryServiceApi->register_dataset:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->register_dataset: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **body** | [**RegisterDatasetRequest**](RegisterDatasetRequest.md)|  | 

### Return type

[**RimeRegisterDatasetResponse**](RimeRegisterDatasetResponse.md)

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

# **register_model**
> RimeRegisterModelResponse register_model(project_id_uuid, body)

RegisterModel

Register a new Model for the specified Project.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.register_model_request import RegisterModelRequest
from ri.apiclient.models.rime_register_model_response import RimeRegisterModelResponse
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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.RegisterModelRequest() # RegisterModelRequest | 

    try:
        # RegisterModel
        api_response = api_instance.register_model(project_id_uuid, body)
        print("The response of RegistryServiceApi->register_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->register_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **body** | [**RegisterModelRequest**](RegisterModelRequest.md)|  | 

### Return type

[**RimeRegisterModelResponse**](RimeRegisterModelResponse.md)

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

# **register_prediction_set**
> RimeRegisterPredictionSetResponse register_prediction_set(project_id_uuid, model_id_uuid, dataset_id, body)

RegisterPredictionSet

Register a Prediction set corresponding to a specified Model and Dataset.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.register_prediction_set_request import RegisterPredictionSetRequest
from ri.apiclient.models.rime_register_prediction_set_response import RimeRegisterPredictionSetResponse
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
    api_instance = ri.apiclient.RegistryServiceApi(api_client)
    project_id_uuid = 'project_id_uuid_example' # str | Unique object ID.
    model_id_uuid = 'model_id_uuid_example' # str | Unique object ID.
    dataset_id = 'dataset_id_example' # str | Uniquely specifies a Dataset.
    body = ri.apiclient.RegisterPredictionSetRequest() # RegisterPredictionSetRequest | 

    try:
        # RegisterPredictionSet
        api_response = api_instance.register_prediction_set(project_id_uuid, model_id_uuid, dataset_id, body)
        print("The response of RegistryServiceApi->register_prediction_set:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistryServiceApi->register_prediction_set: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id_uuid** | **str**| Unique object ID. | 
 **model_id_uuid** | **str**| Unique object ID. | 
 **dataset_id** | **str**| Uniquely specifies a Dataset. | 
 **body** | [**RegisterPredictionSetRequest**](RegisterPredictionSetRequest.md)|  | 

### Return type

[**RimeRegisterPredictionSetResponse**](RimeRegisterPredictionSetResponse.md)

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

