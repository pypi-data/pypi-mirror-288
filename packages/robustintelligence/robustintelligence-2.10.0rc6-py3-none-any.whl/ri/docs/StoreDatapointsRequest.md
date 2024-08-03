# StoreDatapointsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_stream_id** | **object** | Uniquely specifies a data stream. | [optional] 
**datapoints** | [**List[DatacollectorDatapointRow]**](DatacollectorDatapointRow.md) | The datapoints to store. | [optional] 

## Example

```python
from ri.apiclient.models.store_datapoints_request import StoreDatapointsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of StoreDatapointsRequest from a JSON string
store_datapoints_request_instance = StoreDatapointsRequest.from_json(json)
# print the JSON string representation of the object
print(StoreDatapointsRequest.to_json())

# convert the object into a dict
store_datapoints_request_dict = store_datapoints_request_instance.to_dict()
# create an instance of StoreDatapointsRequest from a dict
store_datapoints_request_from_dict = StoreDatapointsRequest.from_dict(store_datapoints_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

