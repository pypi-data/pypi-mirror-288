# RimeTableColumn


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**type** | [**RimeTableColumnType**](RimeTableColumnType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_table_column import RimeTableColumn

# TODO update the JSON string below
json = "{}"
# create an instance of RimeTableColumn from a JSON string
rime_table_column_instance = RimeTableColumn.from_json(json)
# print the JSON string representation of the object
print(RimeTableColumn.to_json())

# convert the object into a dict
rime_table_column_dict = rime_table_column_instance.to_dict()
# create an instance of RimeTableColumn from a dict
rime_table_column_from_dict = RimeTableColumn.from_dict(rime_table_column_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

