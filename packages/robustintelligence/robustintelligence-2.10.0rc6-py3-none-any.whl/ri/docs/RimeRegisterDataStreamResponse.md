# RimeRegisterDataStreamResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_stream_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_register_data_stream_response import RimeRegisterDataStreamResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeRegisterDataStreamResponse from a JSON string
rime_register_data_stream_response_instance = RimeRegisterDataStreamResponse.from_json(json)
# print the JSON string representation of the object
print(RimeRegisterDataStreamResponse.to_json())

# convert the object into a dict
rime_register_data_stream_response_dict = rime_register_data_stream_response_instance.to_dict()
# create an instance of RimeRegisterDataStreamResponse from a dict
rime_register_data_stream_response_from_dict = RimeRegisterDataStreamResponse.from_dict(rime_register_data_stream_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

