# ri.fwclient.FirewallApi

All URIs are relative to *http://https://&lt;ai-firewall-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**effective_config**](FirewallApi.md#effective_config) | **GET** /v1-beta/firewall/{firewallInstanceId.uuid}/effective-config | GetFirewallEffectiveConfig
[**validate**](FirewallApi.md#validate) | **PUT** /v1-beta/firewall/{firewallInstanceId.uuid}/validate | Validate


# **effective_config**
> GenerativefirewallGetFirewallEffectiveConfigResponse effective_config(firewall_instance_id_uuid)

GetFirewallEffectiveConfig

Retrieve the effective config of the firewall. The effective config is the users config plus all defaults. This request will be routed to a specific FirewallInstance. There can be multiple FirewallInstances in the cluster with different configurations.

### Example

* Api Key Authentication (X-Firewall-Auth-Token):

```python
import ri.fwclient
from ri.fwclient.models.generativefirewall_get_firewall_effective_config_response import GenerativefirewallGetFirewallEffectiveConfigResponse
from ri.fwclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https://<ai-firewall-domain>.rbst.io
# See configuration.py for a list of all supported configuration parameters.
configuration = ri.fwclient.Configuration(
    host = "http://https://<ai-firewall-domain>.rbst.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: X-Firewall-Auth-Token
configuration.api_key['X-Firewall-Auth-Token'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-Firewall-Auth-Token'] = 'Bearer'

# Enter a context with an instance of the API client
with ri.fwclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ri.fwclient.FirewallApi(api_client)
    firewall_instance_id_uuid = 'firewall_instance_id_uuid_example' # str | Unique object ID.

    try:
        # GetFirewallEffectiveConfig
        api_response = api_instance.effective_config(firewall_instance_id_uuid)
        print("The response of FirewallApi->effective_config:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallApi->effective_config: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_instance_id_uuid** | **str**| Unique object ID. | 

### Return type

[**GenerativefirewallGetFirewallEffectiveConfigResponse**](GenerativefirewallGetFirewallEffectiveConfigResponse.md)

### Authorization

[X-Firewall-Auth-Token](../README.md#X-Firewall-Auth-Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **validate**
> GenerativefirewallValidateResponse validate(firewall_instance_id_uuid, body)

Validate

Validate performs real-time validation on a single query to the model. This request will be routed to a specific FirewallInstance. There can be multiple FirewallInstances in the cluster with different configurations.

### Example

* Api Key Authentication (X-Firewall-Auth-Token):

```python
import ri.fwclient
from ri.fwclient.models.generativefirewall_validate_response import GenerativefirewallValidateResponse
from ri.fwclient.models.validate_request import ValidateRequest
from ri.fwclient.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://https://<ai-firewall-domain>.rbst.io
# See configuration.py for a list of all supported configuration parameters.
configuration = ri.fwclient.Configuration(
    host = "http://https://<ai-firewall-domain>.rbst.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: X-Firewall-Auth-Token
configuration.api_key['X-Firewall-Auth-Token'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-Firewall-Auth-Token'] = 'Bearer'

# Enter a context with an instance of the API client
with ri.fwclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ri.fwclient.FirewallApi(api_client)
    firewall_instance_id_uuid = 'firewall_instance_id_uuid_example' # str | Unique object ID.
    body = ri.fwclient.ValidateRequest() # ValidateRequest | 

    try:
        # Validate
        api_response = api_instance.validate(firewall_instance_id_uuid, body)
        print("The response of FirewallApi->validate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FirewallApi->validate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firewall_instance_id_uuid** | **str**| Unique object ID. | 
 **body** | [**ValidateRequest**](ValidateRequest.md)|  | 

### Return type

[**GenerativefirewallValidateResponse**](GenerativefirewallValidateResponse.md)

### Authorization

[X-Firewall-Auth-Token](../README.md#X-Firewall-Auth-Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**0** | An unexpected error response. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

