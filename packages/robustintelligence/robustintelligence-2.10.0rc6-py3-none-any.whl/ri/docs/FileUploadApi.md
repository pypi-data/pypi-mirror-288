# ri.apiclient.FileUploadApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_uploaded_file_url**](FileUploadApi.md#delete_uploaded_file_url) | **DELETE** /v1-beta/datasets/upload-url | DeleteUploadedFileURL
[**file_upload_get_dataset_file_upload_url**](FileUploadApi.md#file_upload_get_dataset_file_upload_url) | **GET** /v1-beta/datasets/upload-url | GetDatasetFileUploadURL
[**file_upload_get_dataset_file_upload_url2**](FileUploadApi.md#file_upload_get_dataset_file_upload_url2) | **POST** /v1-beta/datasets/upload-url | GetDatasetFileUploadURL
[**file_upload_get_model_directory_upload_urls**](FileUploadApi.md#file_upload_get_model_directory_upload_urls) | **GET** /v1-beta/models/upload-url | GetModelDirectoryUploadURL
[**file_upload_get_model_directory_upload_urls2**](FileUploadApi.md#file_upload_get_model_directory_upload_urls2) | **POST** /v1-beta/models/upload-url | GetModelDirectoryUploadURL
[**list_uploaded_file_urls**](FileUploadApi.md#list_uploaded_file_urls) | **GET** /v1-beta/uploaded-file-urls | ListUploadedFileURLs


# **delete_uploaded_file_url**
> object delete_uploaded_file_url(uploaded_url)

DeleteUploadedFileURL

Deletes the uploaded dataset at the specified URL from the blob store.

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
    api_instance = ri.apiclient.FileUploadApi(api_client)
    uploaded_url = 'uploaded_url_example' # str | URL of the uploaded file to delete.

    try:
        # DeleteUploadedFileURL
        api_response = api_instance.delete_uploaded_file_url(uploaded_url)
        print("The response of FileUploadApi->delete_uploaded_file_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileUploadApi->delete_uploaded_file_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uploaded_url** | **str**| URL of the uploaded file to delete. | 

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

# **file_upload_get_dataset_file_upload_url**
> RimeGetDatasetFileUploadURLResponse file_upload_get_dataset_file_upload_url(file_name, upload_path=upload_path)

GetDatasetFileUploadURL

Returns a pre-signed upload URL for a dataset.  File uploading is not currently supported in a Cloud deployment. Please use an external data source instead.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_dataset_file_upload_url_response import RimeGetDatasetFileUploadURLResponse
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
    api_instance = ri.apiclient.FileUploadApi(api_client)
    file_name = 'file_name_example' # str | Path of dataset file on the local file system.
    upload_path = 'upload_path_example' # str | Specify a path in the blob store to use for data uploads. (optional)

    try:
        # GetDatasetFileUploadURL
        api_response = api_instance.file_upload_get_dataset_file_upload_url(file_name, upload_path=upload_path)
        print("The response of FileUploadApi->file_upload_get_dataset_file_upload_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileUploadApi->file_upload_get_dataset_file_upload_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_name** | **str**| Path of dataset file on the local file system. | 
 **upload_path** | **str**| Specify a path in the blob store to use for data uploads. | [optional] 

### Return type

[**RimeGetDatasetFileUploadURLResponse**](RimeGetDatasetFileUploadURLResponse.md)

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

# **file_upload_get_dataset_file_upload_url2**
> RimeGetDatasetFileUploadURLResponse file_upload_get_dataset_file_upload_url2(body)

GetDatasetFileUploadURL

Returns a pre-signed upload URL for a dataset.  File uploading is not currently supported in a Cloud deployment. Please use an external data source instead.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_dataset_file_upload_url_request import RimeGetDatasetFileUploadURLRequest
from ri.apiclient.models.rime_get_dataset_file_upload_url_response import RimeGetDatasetFileUploadURLResponse
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
    api_instance = ri.apiclient.FileUploadApi(api_client)
    body = ri.apiclient.RimeGetDatasetFileUploadURLRequest() # RimeGetDatasetFileUploadURLRequest | 

    try:
        # GetDatasetFileUploadURL
        api_response = api_instance.file_upload_get_dataset_file_upload_url2(body)
        print("The response of FileUploadApi->file_upload_get_dataset_file_upload_url2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileUploadApi->file_upload_get_dataset_file_upload_url2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeGetDatasetFileUploadURLRequest**](RimeGetDatasetFileUploadURLRequest.md)|  | 

### Return type

[**RimeGetDatasetFileUploadURLResponse**](RimeGetDatasetFileUploadURLResponse.md)

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

# **file_upload_get_model_directory_upload_urls**
> RimeGetModelDirectoryUploadURLsResponse file_upload_get_model_directory_upload_urls(directory_name, relative_file_paths, upload_path=upload_path)

GetModelDirectoryUploadURL

Returns a pre-signed upload URL for a model directory.  File uploading is not currently supported in a Cloud deployment. Please use an external data source instead.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_model_directory_upload_urls_response import RimeGetModelDirectoryUploadURLsResponse
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
    api_instance = ri.apiclient.FileUploadApi(api_client)
    directory_name = 'directory_name_example' # str | Path of model directory on local file system.
    relative_file_paths = ['relative_file_paths_example'] # List[str] | Array of relative paths from the model directory to model files.
    upload_path = 'upload_path_example' # str | Specify a path in the blob store to which the model will be uploaded. (optional)

    try:
        # GetModelDirectoryUploadURL
        api_response = api_instance.file_upload_get_model_directory_upload_urls(directory_name, relative_file_paths, upload_path=upload_path)
        print("The response of FileUploadApi->file_upload_get_model_directory_upload_urls:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileUploadApi->file_upload_get_model_directory_upload_urls: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **directory_name** | **str**| Path of model directory on local file system. | 
 **relative_file_paths** | [**List[str]**](str.md)| Array of relative paths from the model directory to model files. | 
 **upload_path** | **str**| Specify a path in the blob store to which the model will be uploaded. | [optional] 

### Return type

[**RimeGetModelDirectoryUploadURLsResponse**](RimeGetModelDirectoryUploadURLsResponse.md)

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

# **file_upload_get_model_directory_upload_urls2**
> RimeGetModelDirectoryUploadURLsResponse file_upload_get_model_directory_upload_urls2(body)

GetModelDirectoryUploadURL

Returns a pre-signed upload URL for a model directory.  File uploading is not currently supported in a Cloud deployment. Please use an external data source instead.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_model_directory_upload_urls_request import RimeGetModelDirectoryUploadURLsRequest
from ri.apiclient.models.rime_get_model_directory_upload_urls_response import RimeGetModelDirectoryUploadURLsResponse
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
    api_instance = ri.apiclient.FileUploadApi(api_client)
    body = ri.apiclient.RimeGetModelDirectoryUploadURLsRequest() # RimeGetModelDirectoryUploadURLsRequest | 

    try:
        # GetModelDirectoryUploadURL
        api_response = api_instance.file_upload_get_model_directory_upload_urls2(body)
        print("The response of FileUploadApi->file_upload_get_model_directory_upload_urls2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileUploadApi->file_upload_get_model_directory_upload_urls2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeGetModelDirectoryUploadURLsRequest**](RimeGetModelDirectoryUploadURLsRequest.md)|  | 

### Return type

[**RimeGetModelDirectoryUploadURLsResponse**](RimeGetModelDirectoryUploadURLsResponse.md)

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

# **list_uploaded_file_urls**
> RimeListUploadedFileURLsResponse list_uploaded_file_urls()

ListUploadedFileURLs

List up to 1000 blob store URLs for uploaded files.  File uploading is not currently supported in a Cloud deployment. Please use an external data source instead.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_uploaded_file_urls_response import RimeListUploadedFileURLsResponse
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
    api_instance = ri.apiclient.FileUploadApi(api_client)

    try:
        # ListUploadedFileURLs
        api_response = api_instance.list_uploaded_file_urls()
        print("The response of FileUploadApi->list_uploaded_file_urls:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileUploadApi->list_uploaded_file_urls: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RimeListUploadedFileURLsResponse**](RimeListUploadedFileURLsResponse.md)

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

