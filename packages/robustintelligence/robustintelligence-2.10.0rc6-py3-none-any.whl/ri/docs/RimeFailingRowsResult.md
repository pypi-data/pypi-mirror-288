# RimeFailingRowsResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**failing_rows** | [**List[RimeFailingRow]**](RimeFailingRow.md) |  | [optional] 
**top_count** | **str** |  | [optional] 
**total_count** | **str** |  | [optional] 
**all_included** | **bool** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_failing_rows_result import RimeFailingRowsResult

# TODO update the JSON string below
json = "{}"
# create an instance of RimeFailingRowsResult from a JSON string
rime_failing_rows_result_instance = RimeFailingRowsResult.from_json(json)
# print the JSON string representation of the object
print(RimeFailingRowsResult.to_json())

# convert the object into a dict
rime_failing_rows_result_dict = rime_failing_rows_result_instance.to_dict()
# create an instance of RimeFailingRowsResult from a dict
rime_failing_rows_result_from_dict = RimeFailingRowsResult.from_dict(rime_failing_rows_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

