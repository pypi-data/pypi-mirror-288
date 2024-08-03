# DatacollectorDatapoint

Datapoint contains the DatapointRow and additional metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**datapoint_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**data_stream_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**datapoint** | [**DatacollectorDatapointRow**](DatacollectorDatapointRow.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.datacollector_datapoint import DatacollectorDatapoint

# TODO update the JSON string below
json = "{}"
# create an instance of DatacollectorDatapoint from a JSON string
datacollector_datapoint_instance = DatacollectorDatapoint.from_json(json)
# print the JSON string representation of the object
print(DatacollectorDatapoint.to_json())

# convert the object into a dict
datacollector_datapoint_dict = datacollector_datapoint_instance.to_dict()
# create an instance of DatacollectorDatapoint from a dict
datacollector_datapoint_from_dict = DatacollectorDatapoint.from_dict(datacollector_datapoint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

