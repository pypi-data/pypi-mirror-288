# ri.apiclient.RIMEInfoApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_rime_info**](RIMEInfoApi.md#get_rime_info) | **GET** /v1/rime-info | GetRIMEInfo


# **get_rime_info**
> RimeGetRIMEInfoResponse get_rime_info()

GetRIMEInfo

Returns information about the Robust Intelligence cluster you are querying.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_rime_info_response import RimeGetRIMEInfoResponse
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
    api_instance = ri.apiclient.RIMEInfoApi(api_client)

    try:
        # GetRIMEInfo
        api_response = api_instance.get_rime_info()
        print("The response of RIMEInfoApi->get_rime_info:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RIMEInfoApi->get_rime_info: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**RimeGetRIMEInfoResponse**](RimeGetRIMEInfoResponse.md)

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

