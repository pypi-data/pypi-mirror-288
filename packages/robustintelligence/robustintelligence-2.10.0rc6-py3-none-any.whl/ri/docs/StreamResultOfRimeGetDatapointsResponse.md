# StreamResultOfRimeGetDatapointsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | [**RimeGetDatapointsResponse**](RimeGetDatapointsResponse.md) |  | [optional] 
**error** | [**GooglerpcStatus**](GooglerpcStatus.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.stream_result_of_rime_get_datapoints_response import StreamResultOfRimeGetDatapointsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StreamResultOfRimeGetDatapointsResponse from a JSON string
stream_result_of_rime_get_datapoints_response_instance = StreamResultOfRimeGetDatapointsResponse.from_json(json)
# print the JSON string representation of the object
print(StreamResultOfRimeGetDatapointsResponse.to_json())

# convert the object into a dict
stream_result_of_rime_get_datapoints_response_dict = stream_result_of_rime_get_datapoints_response_instance.to_dict()
# create an instance of StreamResultOfRimeGetDatapointsResponse from a dict
stream_result_of_rime_get_datapoints_response_from_dict = StreamResultOfRimeGetDatapointsResponse.from_dict(stream_result_of_rime_get_datapoints_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

