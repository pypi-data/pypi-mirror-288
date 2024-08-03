# ri.apiclient.NotificationSettingApi

All URIs are relative to *http://https://&lt;platform-domain&gt;.rbst.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_notification**](NotificationSettingApi.md#create_notification) | **POST** /v1/notif-settings | CreateNotification
[**delete_notification**](NotificationSettingApi.md#delete_notification) | **DELETE** /v1/notif-settings/{id.uuid} | DeleteNotification
[**list_notifications**](NotificationSettingApi.md#list_notifications) | **GET** /v1/notif-settings | ListNotifications
[**update_notification**](NotificationSettingApi.md#update_notification) | **PUT** /v1/notif-settings/{notification.id.uuid} | UpdateNotification


# **create_notification**
> RimeCreateNotificationResponse create_notification(body)

CreateNotification

Creates a new notification setting.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_create_notification_request import RimeCreateNotificationRequest
from ri.apiclient.models.rime_create_notification_response import RimeCreateNotificationResponse
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
    api_instance = ri.apiclient.NotificationSettingApi(api_client)
    body = ri.apiclient.RimeCreateNotificationRequest() # RimeCreateNotificationRequest | 

    try:
        # CreateNotification
        api_response = api_instance.create_notification(body)
        print("The response of NotificationSettingApi->create_notification:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationSettingApi->create_notification: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RimeCreateNotificationRequest**](RimeCreateNotificationRequest.md)|  | 

### Return type

[**RimeCreateNotificationResponse**](RimeCreateNotificationResponse.md)

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

# **delete_notification**
> object delete_notification(id_uuid)

DeleteNotification

Hard-delete a notification setting.

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
    api_instance = ri.apiclient.NotificationSettingApi(api_client)
    id_uuid = 'id_uuid_example' # str | Unique object ID.

    try:
        # DeleteNotification
        api_response = api_instance.delete_notification(id_uuid)
        print("The response of NotificationSettingApi->delete_notification:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationSettingApi->delete_notification: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id_uuid** | **str**| Unique object ID. | 

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

# **list_notifications**
> RimeListNotificationsResponse list_notifications(list_notifications_query_object_types=list_notifications_query_object_types, list_notifications_query_object_ids=list_notifications_query_object_ids, page_token=page_token, page_size=page_size)

ListNotifications

Lists notification settings with options to filter by project or the type of notification.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_list_notifications_response import RimeListNotificationsResponse
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
    api_instance = ri.apiclient.NotificationSettingApi(api_client)
    list_notifications_query_object_types = ['list_notifications_query_object_types_example'] # List[str] | Specifies a set of object types. Filters results by the specified set of object types.   - OBJECT_TYPE_PROJECT: Used for notifications associated with an project. The Notification object ID is the Project ID. (optional)
    list_notifications_query_object_ids = ['list_notifications_query_object_ids_example'] # List[str] | Specifies a set of object IDs. Filters results by the specified set of object IDs. (optional)
    page_token = 'page_token_example' # str | Specifies a page of the list returned by a ListNotifications query. The ListNotifications query returns a pageToken when there is more than one page of results. Specify either this field or the listNotificationsQuery field. (optional)
    page_size = 'page_size_example' # str | The maximum number of Notification objects to return in a single page. (optional)

    try:
        # ListNotifications
        api_response = api_instance.list_notifications(list_notifications_query_object_types=list_notifications_query_object_types, list_notifications_query_object_ids=list_notifications_query_object_ids, page_token=page_token, page_size=page_size)
        print("The response of NotificationSettingApi->list_notifications:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationSettingApi->list_notifications: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **list_notifications_query_object_types** | [**List[str]**](str.md)| Specifies a set of object types. Filters results by the specified set of object types.   - OBJECT_TYPE_PROJECT: Used for notifications associated with an project. The Notification object ID is the Project ID. | [optional] 
 **list_notifications_query_object_ids** | [**List[str]**](str.md)| Specifies a set of object IDs. Filters results by the specified set of object IDs. | [optional] 
 **page_token** | **str**| Specifies a page of the list returned by a ListNotifications query. The ListNotifications query returns a pageToken when there is more than one page of results. Specify either this field or the listNotificationsQuery field. | [optional] 
 **page_size** | **str**| The maximum number of Notification objects to return in a single page. | [optional] 

### Return type

[**RimeListNotificationsResponse**](RimeListNotificationsResponse.md)

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

# **update_notification**
> RimeUpdateNotificationResponse update_notification(notification_id_uuid, body)

UpdateNotification

Updates an existing notification setting. The ID in the provided notification is used to identify it.

### Example

* Api Key Authentication (rime-api-key):

```python
import ri.apiclient
from ri.apiclient.models.rime_update_notification_response import RimeUpdateNotificationResponse
from ri.apiclient.models.update_notification_request import UpdateNotificationRequest
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
    api_instance = ri.apiclient.NotificationSettingApi(api_client)
    notification_id_uuid = 'notification_id_uuid_example' # str | Unique object ID.
    body = ri.apiclient.UpdateNotificationRequest() # UpdateNotificationRequest | 

    try:
        # UpdateNotification
        api_response = api_instance.update_notification(notification_id_uuid, body)
        print("The response of NotificationSettingApi->update_notification:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotificationSettingApi->update_notification: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **notification_id_uuid** | **str**| Unique object ID. | 
 **body** | [**UpdateNotificationRequest**](UpdateNotificationRequest.md)|  | 

### Return type

[**RimeUpdateNotificationResponse**](RimeUpdateNotificationResponse.md)

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

