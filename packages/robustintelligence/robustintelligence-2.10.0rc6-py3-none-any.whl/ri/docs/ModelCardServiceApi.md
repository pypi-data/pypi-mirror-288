# ri.apiclient.ModelCardServiceApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_model_card**](ModelCardServiceApi.md#create_model_card) | **POST** /v1-beta/modelcards | CreateModelCard
[**delete_model_card**](ModelCardServiceApi.md#delete_model_card) | **DELETE** /v1-beta/modelcards/{modelCardId.uuid} | DeleteModelCard
[**list_model_cards**](ModelCardServiceApi.md#list_model_cards) | **GET** /v1-beta/modelcards/projects/{projectId} | ListModelCards
[**model_card_service_get_model_card**](ModelCardServiceApi.md#model_card_service_get_model_card) | **GET** /v1-beta/modelcards/{modelCardId.uuid} | GetModelCard
[**update_model_card**](ModelCardServiceApi.md#update_model_card) | **PUT** /v1-beta/modelcards/{modelCard.modelCardId.uuid} | UpdateModelCard


# **create_model_card**
> RimeCreateModelCardResponse create_model_card(body)

CreateModelCard

Create a new Model Card.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_create_model_card_request import RimeCreateModelCardRequest
from ri.apiclient.models.rime_create_model_card_response import RimeCreateModelCardResponse
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
    api_instance = ri.apiclient.ModelCardServiceApi(api_client)
    body = ri.apiclient.RimeCreateModelCardRequest() # RimeCreateModelCardRequest | 

    try:
        # CreateModelCard
        api_response = api_instance.create_model_card(body)
        print("The response of ModelCardServiceApi->create_model_card:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelCardServiceApi->create_model_card: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeCreateModelCardRequest**](RimeCreateModelCardRequest.md)|  | 

### Return type

[**RimeCreateModelCardResponse**](RimeCreateModelCardResponse.md)

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

# **delete_model_card**
> RimeDeleteModelCardResponse delete_model_card(model_card_id_uuid)

DeleteModelCard

Delete Model Card.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_delete_model_card_response import RimeDeleteModelCardResponse
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
    api_instance = ri.apiclient.ModelCardServiceApi(api_client)
    model_card_id_uuid = 'model_card_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteModelCard
        api_response = api_instance.delete_model_card(model_card_id_uuid)
        print("The response of ModelCardServiceApi->delete_model_card:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelCardServiceApi->delete_model_card: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_card_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeDeleteModelCardResponse**](RimeDeleteModelCardResponse.md)

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

# **list_model_cards**
> RimeListModelCardsResponse list_model_cards(project_id)

ListModelCards

List Model Cards by Project.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_model_cards_response import RimeListModelCardsResponse
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
    api_instance = ri.apiclient.ModelCardServiceApi(api_client)
    project_id = 'project_id_example' # str | Uniquely specifies a Project.

    try:
        # ListModelCards
        api_response = api_instance.list_model_cards(project_id)
        print("The response of ModelCardServiceApi->list_model_cards:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelCardServiceApi->list_model_cards: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Uniquely specifies a Project. | 

### Return type

[**RimeListModelCardsResponse**](RimeListModelCardsResponse.md)

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

# **model_card_service_get_model_card**
> RimeGetModelCardResponse model_card_service_get_model_card(model_card_id_uuid)

GetModelCard

Get Model Card By ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_model_card_response import RimeGetModelCardResponse
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
    api_instance = ri.apiclient.ModelCardServiceApi(api_client)
    model_card_id_uuid = 'model_card_id_uuid_example' # str | Unique object ID.

    try:
        # GetModelCard
        api_response = api_instance.model_card_service_get_model_card(model_card_id_uuid)
        print("The response of ModelCardServiceApi->model_card_service_get_model_card:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelCardServiceApi->model_card_service_get_model_card: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_card_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeGetModelCardResponse**](RimeGetModelCardResponse.md)

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

# **update_model_card**
> RimeUpdateModelCardResponse update_model_card(model_card_model_card_id_uuid, body)

UpdateModelCard

Update Model Card by ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_update_model_card_response import RimeUpdateModelCardResponse
from ri.apiclient.models.update_model_card_request import UpdateModelCardRequest
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
    api_instance = ri.apiclient.ModelCardServiceApi(api_client)
    model_card_model_card_id_uuid = 'model_card_model_card_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.UpdateModelCardRequest() # UpdateModelCardRequest | 

    try:
        # UpdateModelCard
        api_response = api_instance.update_model_card(model_card_model_card_id_uuid, body)
        print("The response of ModelCardServiceApi->update_model_card:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelCardServiceApi->update_model_card: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model_card_model_card_id_uuid** | **str**| Unique object ID. | 
 **body** | [**UpdateModelCardRequest**](UpdateModelCardRequest.md)|  | 

### Return type

[**RimeUpdateModelCardResponse**](RimeUpdateModelCardResponse.md)

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

