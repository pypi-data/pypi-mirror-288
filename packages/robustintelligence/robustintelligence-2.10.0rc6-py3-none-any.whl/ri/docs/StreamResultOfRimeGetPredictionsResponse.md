# StreamResultOfRimeGetPredictionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | [**RimeGetPredictionsResponse**](RimeGetPredictionsResponse.md) |  | [optional] 
**error** | [**GooglerpcStatus**](GooglerpcStatus.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.stream_result_of_rime_get_predictions_response import StreamResultOfRimeGetPredictionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StreamResultOfRimeGetPredictionsResponse from a JSON string
stream_result_of_rime_get_predictions_response_instance = StreamResultOfRimeGetPredictionsResponse.from_json(json)
# print the JSON string representation of the object
print(StreamResultOfRimeGetPredictionsResponse.to_json())

# convert the object into a dict
stream_result_of_rime_get_predictions_response_dict = stream_result_of_rime_get_predictions_response_instance.to_dict()
# create an instance of StreamResultOfRimeGetPredictionsResponse from a dict
stream_result_of_rime_get_predictions_response_from_dict = StreamResultOfRimeGetPredictionsResponse.from_dict(stream_result_of_rime_get_predictions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

