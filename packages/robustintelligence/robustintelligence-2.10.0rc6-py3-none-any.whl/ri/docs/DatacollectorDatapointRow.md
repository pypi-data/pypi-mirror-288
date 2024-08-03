# DatacollectorDatapointRow


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**input_data** | **bytearray** |  | [optional] 
**label** | **bytearray** |  | [optional] 
**timestamp** | **datetime** | If timestamp is not provided in request, the time when the datapoint is stored will be used. | [optional] 
**query_id** | **bytearray** | Query ID is required for Ranking model tasks. | [optional] 

## Example

```python
from ri.apiclient.models.datacollector_datapoint_row import DatacollectorDatapointRow

# TODO update the JSON string below
json = "{}"
# create an instance of DatacollectorDatapointRow from a JSON string
datacollector_datapoint_row_instance = DatacollectorDatapointRow.from_json(json)
# print the JSON string representation of the object
print(DatacollectorDatapointRow.to_json())

# convert the object into a dict
datacollector_datapoint_row_dict = datacollector_datapoint_row_instance.to_dict()
# create an instance of DatacollectorDatapointRow from a dict
datacollector_datapoint_row_from_dict = DatacollectorDatapointRow.from_dict(datacollector_datapoint_row_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

