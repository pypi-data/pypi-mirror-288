# RegisterDataStreamRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | **object** | Uniquely specifies a Project. | [optional] 

## Example

```python
from ri.apiclient.models.register_data_stream_request import RegisterDataStreamRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RegisterDataStreamRequest from a JSON string
register_data_stream_request_instance = RegisterDataStreamRequest.from_json(json)
# print the JSON string representation of the object
print(RegisterDataStreamRequest.to_json())

# convert the object into a dict
register_data_stream_request_dict = register_data_stream_request_instance.to_dict()
# create an instance of RegisterDataStreamRequest from a dict
register_data_stream_request_from_dict = RegisterDataStreamRequest.from_dict(register_data_stream_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

