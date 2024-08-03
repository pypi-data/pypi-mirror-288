# ri.apiclient.AgentManagerApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_agent**](AgentManagerApi.md#create_agent) | **POST** /v1/agents | CreateAgent
[**create_firewall_agent**](AgentManagerApi.md#create_firewall_agent) | **POST** /v1-beta/agents/firewall | CreateFirewallAgent
[**delete_agent**](AgentManagerApi.md#delete_agent) | **DELETE** /v1/agents/{agentId.uuid} | DeleteAgent
[**get_agent**](AgentManagerApi.md#get_agent) | **GET** /v1/agents/{agentId.uuid} | GetAgent
[**get_upgrade_for_agent**](AgentManagerApi.md#get_upgrade_for_agent) | **GET** /v1-beta/agents/{agentId.uuid}/upgrade | GetUpgradeForAgent returns the desired state of the agent and the current status of the upgrade.
[**list_agents**](AgentManagerApi.md#list_agents) | **GET** /v1/agents | ListAgents
[**list_firewall_instances**](AgentManagerApi.md#list_firewall_instances) | **POST** /v1-beta/agents/firewall/instances | ListFirewallInstances
[**request_firewall_instance**](AgentManagerApi.md#request_firewall_instance) | **POST** /v1-beta/agents/firewall/{agentId.uuid}/firewall-instance/request | RequestFirewallInstance
[**upgrade_agent**](AgentManagerApi.md#upgrade_agent) | **POST** /v1-beta/agents/{agentId.uuid}/upgrade | UpgradeAgent starts the process of upgrading the agent to the version of the control plane


# **create_agent**
> RimeCreateAgentResponse create_agent(body)

CreateAgent

Creates agent and returns the configuration for installing the agent.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_create_agent_request import RimeCreateAgentRequest
from ri.apiclient.models.rime_create_agent_response import RimeCreateAgentResponse
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
    api_instance = ri.apiclient.AgentManagerApi(api_client)
    body = ri.apiclient.RimeCreateAgentRequest() # RimeCreateAgentRequest | 

    try:
        # CreateAgent
        api_response = api_instance.create_agent(body)
        print("The response of AgentManagerApi->create_agent:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentManagerApi->create_agent: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeCreateAgentRequest**](RimeCreateAgentRequest.md)|  | 

### Return type

[**RimeCreateAgentResponse**](RimeCreateAgentResponse.md)

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

# **create_firewall_agent**
> RimeCreateFirewallAgentResponse create_firewall_agent(body)

CreateFirewallAgent

Creates a firewall agent and returns the api key.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_create_firewall_agent_request import RimeCreateFirewallAgentRequest
from ri.apiclient.models.rime_create_firewall_agent_response import RimeCreateFirewallAgentResponse
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
    api_instance = ri.apiclient.AgentManagerApi(api_client)
    body = ri.apiclient.RimeCreateFirewallAgentRequest() # RimeCreateFirewallAgentRequest | 

    try:
        # CreateFirewallAgent
        api_response = api_instance.create_firewall_agent(body)
        print("The response of AgentManagerApi->create_firewall_agent:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentManagerApi->create_firewall_agent: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeCreateFirewallAgentRequest**](RimeCreateFirewallAgentRequest.md)|  | 

### Return type

[**RimeCreateFirewallAgentResponse**](RimeCreateFirewallAgentResponse.md)

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

# **delete_agent**
> object delete_agent(agent_id_uuid)

DeleteAgent

Deletes a specified agent. Must be called on an already deactivated agent. An error is returned if the deletion fails or if the agent is not in a deletable state.

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
    api_instance = ri.apiclient.AgentManagerApi(api_client)
    agent_id_uuid = 'agent_id_uuid_example' # str | Unique object ID.

    try:
        # DeleteAgent
        api_response = api_instance.delete_agent(agent_id_uuid)
        print("The response of AgentManagerApi->delete_agent:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentManagerApi->delete_agent: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_id_uuid** | **str**| Unique object ID. | 

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

# **get_agent**
> RimeGetAgentResponse get_agent(agent_id_uuid)

GetAgent

Returns the agent that matches the specified ID.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_agent_response import RimeGetAgentResponse
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
    api_instance = ri.apiclient.AgentManagerApi(api_client)
    agent_id_uuid = 'agent_id_uuid_example' # str | Unique object ID.

    try:
        # GetAgent
        api_response = api_instance.get_agent(agent_id_uuid)
        print("The response of AgentManagerApi->get_agent:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentManagerApi->get_agent: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_id_uuid** | **str**| Unique object ID. | 

### Return type

[**RimeGetAgentResponse**](RimeGetAgentResponse.md)

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

# **get_upgrade_for_agent**
> RimeGetUpgradeForAgentResponse get_upgrade_for_agent(agent_id_uuid, agent_namespace)

GetUpgradeForAgent returns the desired state of the agent and the current status of the upgrade.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_get_upgrade_for_agent_response import RimeGetUpgradeForAgentResponse
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
    api_instance = ri.apiclient.AgentManagerApi(api_client)
    agent_id_uuid = 'agent_id_uuid_example' # str | Unique object ID.
    agent_namespace = 'agent_namespace_example' # str | The namespace in which the agent is deployed. Since namespace is not known in the CP, it must be provided by the launcher when calling GetUpgradeForAgent.

    try:
        # GetUpgradeForAgent returns the desired state of the agent and the current status of the upgrade.
        api_response = api_instance.get_upgrade_for_agent(agent_id_uuid, agent_namespace)
        print("The response of AgentManagerApi->get_upgrade_for_agent:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentManagerApi->get_upgrade_for_agent: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_id_uuid** | **str**| Unique object ID. | 
 **agent_namespace** | **str**| The namespace in which the agent is deployed. Since namespace is not known in the CP, it must be provided by the launcher when calling GetUpgradeForAgent. | 

### Return type

[**RimeGetUpgradeForAgentResponse**](RimeGetUpgradeForAgentResponse.md)

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

# **list_agents**
> RimeListAgentsResponse list_agents(page_size=page_size, page_token=page_token, first_page_query_agent_status_types=first_page_query_agent_status_types, first_page_query_agent_ids=first_page_query_agent_ids, first_page_query_type=first_page_query_type)

ListAgents

Returns a paginated list of agents.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_agents_response import RimeListAgentsResponse
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
    api_instance = ri.apiclient.AgentManagerApi(api_client)
    page_size = 'page_size_example' # str | The maximum number of Agent objects to return in a single page. (optional)
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListAgents query. The ListAgents query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageQuery field. (optional)
    first_page_query_agent_status_types = ['first_page_query_agent_status_types_example'] # List[str] | Specifies a set of agent status types. The query filters for results that match the specified types.   - AGENT_STATUS_PENDING: Resources have been created for the agent but the agent has not started yet.  - AGENT_STATUS_ACTIVE: Agent can run jobs.  - AGENT_STATUS_UNRESPONSIVE: No agent heartbeat for three minutes.  - AGENT_STATUS_DEACTIVATED: Agent can no longer run jobs and can be deleted. (Deprecated after Deactivation and Deletion endpoints are combined) (optional)
    first_page_query_agent_ids = ['first_page_query_agent_ids_example'] # List[str] | Specifies a set of agent IDs. The query filters for results that match the specified IDs. (optional)
    first_page_query_type = 'AGENT_TYPE_VALIDATION' # str | Specifies the type of agent (validation or firewall). The query filters for results that match the specified type.   - AGENT_TYPE_VALIDATION: We use the zero value for VALIDATION for backwards compatibility with existing agents. protolint:disable:next ENUM_FIELD_NAMES_ZERO_VALUE_END_WITH (optional) (default to 'AGENT_TYPE_VALIDATION')

    try:
        # ListAgents
        api_response = api_instance.list_agents(page_size=page_size, page_token=page_token, first_page_query_agent_status_types=first_page_query_agent_status_types, first_page_query_agent_ids=first_page_query_agent_ids, first_page_query_type=first_page_query_type)
        print("The response of AgentManagerApi->list_agents:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentManagerApi->list_agents: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **str**| The maximum number of Agent objects to return in a single page. | [optional] 
 **page_token** | **str**| Specifies a page of the list returned by a ListAgents query. The ListAgents query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageQuery field. | [optional] 
 **first_page_query_agent_status_types** | [**List[str]**](str.md)| Specifies a set of agent status types. The query filters for results that match the specified types.   - AGENT_STATUS_PENDING: Resources have been created for the agent but the agent has not started yet.  - AGENT_STATUS_ACTIVE: Agent can run jobs.  - AGENT_STATUS_UNRESPONSIVE: No agent heartbeat for three minutes.  - AGENT_STATUS_DEACTIVATED: Agent can no longer run jobs and can be deleted. (Deprecated after Deactivation and Deletion endpoints are combined) | [optional] 
 **first_page_query_agent_ids** | [**List[str]**](str.md)| Specifies a set of agent IDs. The query filters for results that match the specified IDs. | [optional] 
 **first_page_query_type** | **str**| Specifies the type of agent (validation or firewall). The query filters for results that match the specified type.   - AGENT_TYPE_VALIDATION: We use the zero value for VALIDATION for backwards compatibility with existing agents. protolint:disable:next ENUM_FIELD_NAMES_ZERO_VALUE_END_WITH | [optional] [default to &#39;AGENT_TYPE_VALIDATION&#39;]

### Return type

[**RimeListAgentsResponse**](RimeListAgentsResponse.md)

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

# **list_firewall_instances**
> RimeListFirewallInstancesResponse list_firewall_instances(body)

ListFirewallInstances

Returns a paginated list of firewall instances.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_firewall_instances_request import RimeListFirewallInstancesRequest
from ri.apiclient.models.rime_list_firewall_instances_response import RimeListFirewallInstancesResponse
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
    api_instance = ri.apiclient.AgentManagerApi(api_client)
    body = ri.apiclient.RimeListFirewallInstancesRequest() # RimeListFirewallInstancesRequest | 

    try:
        # ListFirewallInstances
        api_response = api_instance.list_firewall_instances(body)
        print("The response of AgentManagerApi->list_firewall_instances:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentManagerApi->list_firewall_instances: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeListFirewallInstancesRequest**](RimeListFirewallInstancesRequest.md)|  | 

### Return type

[**RimeListFirewallInstancesResponse**](RimeListFirewallInstancesResponse.md)

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

# **request_firewall_instance**
> RimeRequestFirewallInstanceResponse request_firewall_instance(agent_id_uuid, body)

RequestFirewallInstance

Creates a new firewall instance record in the DB with REQUESTED status. Expects firewall agent in the DP to check for and eventually deploy the firewall instance.  This is intended to be used by external clients of the CP.  Example flow: user logs into the UI connected to the CP -> user tries to create agent in the UI -> UI calls RequestFirewallInstance -> CP tries to create the agent with the DP and then update the status

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.request_firewall_instance_request import RequestFirewallInstanceRequest
from ri.apiclient.models.rime_request_firewall_instance_response import RimeRequestFirewallInstanceResponse
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
    api_instance = ri.apiclient.AgentManagerApi(api_client)
    agent_id_uuid = 'agent_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.RequestFirewallInstanceRequest() # RequestFirewallInstanceRequest | 

    try:
        # RequestFirewallInstance
        api_response = api_instance.request_firewall_instance(agent_id_uuid, body)
        print("The response of AgentManagerApi->request_firewall_instance:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentManagerApi->request_firewall_instance: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_id_uuid** | **str**| Unique object ID. | 
 **body** | [**RequestFirewallInstanceRequest**](RequestFirewallInstanceRequest.md)|  | 

### Return type

[**RimeRequestFirewallInstanceResponse**](RimeRequestFirewallInstanceResponse.md)

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

# **upgrade_agent**
> object upgrade_agent(agent_id_uuid, body)

UpgradeAgent starts the process of upgrading the agent to the version of the control plane

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.upgrade_agent_request import UpgradeAgentRequest
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
    api_instance = ri.apiclient.AgentManagerApi(api_client)
    agent_id_uuid = 'agent_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.UpgradeAgentRequest() # UpgradeAgentRequest | 

    try:
        # UpgradeAgent starts the process of upgrading the agent to the version of the control plane
        api_response = api_instance.upgrade_agent(agent_id_uuid, body)
        print("The response of AgentManagerApi->upgrade_agent:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AgentManagerApi->upgrade_agent: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **agent_id_uuid** | **str**| Unique object ID. | 
 **body** | [**UpgradeAgentRequest**](UpgradeAgentRequest.md)|  | 

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

