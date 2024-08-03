# RimeStoreDatapointsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**datapoint_ids** | [**List[RimeUUID]**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_store_datapoints_response import RimeStoreDatapointsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeStoreDatapointsResponse from a JSON string
rime_store_datapoints_response_instance = RimeStoreDatapointsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeStoreDatapointsResponse.to_json())

# convert the object into a dict
rime_store_datapoints_response_dict = rime_store_datapoints_response_instance.to_dict()
# create an instance of RimeStoreDatapointsResponse from a dict
rime_store_datapoints_response_from_dict = RimeStoreDatapointsResponse.from_dict(rime_store_datapoints_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

