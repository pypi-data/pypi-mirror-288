# RimeGetDatapointsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**datapoints** | [**List[DatacollectorDatapoint]**](DatacollectorDatapoint.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_datapoints_response import RimeGetDatapointsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetDatapointsResponse from a JSON string
rime_get_datapoints_response_instance = RimeGetDatapointsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetDatapointsResponse.to_json())

# convert the object into a dict
rime_get_datapoints_response_dict = rime_get_datapoints_response_instance.to_dict()
# create an instance of RimeGetDatapointsResponse from a dict
rime_get_datapoints_response_from_dict = RimeGetDatapointsResponse.from_dict(rime_get_datapoints_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

