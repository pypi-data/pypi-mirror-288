# ListDatasetsRequestDatasetsQuery

DatasetsQuery is used to filter all datasets within a specified time range and firewall ID.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**scheduled_ct_intervals** | [**RimeTimeInterval**](RimeTimeInterval.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.list_datasets_request_datasets_query import ListDatasetsRequestDatasetsQuery

# TODO update the JSON string below
json = "{}"
# create an instance of ListDatasetsRequestDatasetsQuery from a JSON string
list_datasets_request_datasets_query_instance = ListDatasetsRequestDatasetsQuery.from_json(json)
# print the JSON string representation of the object
print(ListDatasetsRequestDatasetsQuery.to_json())

# convert the object into a dict
list_datasets_request_datasets_query_dict = list_datasets_request_datasets_query_instance.to_dict()
# create an instance of ListDatasetsRequestDatasetsQuery from a dict
list_datasets_request_datasets_query_from_dict = ListDatasetsRequestDatasetsQuery.from_dict(list_datasets_request_datasets_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

