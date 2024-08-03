# RimeFailingRow


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**row_id** | **str** |  | [optional] 
**failing_features** | **List[str]** |  | [optional] 
**details** | **bytearray** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_failing_row import RimeFailingRow

# TODO update the JSON string below
json = "{}"
# create an instance of RimeFailingRow from a JSON string
rime_failing_row_instance = RimeFailingRow.from_json(json)
# print the JSON string representation of the object
print(RimeFailingRow.to_json())

# convert the object into a dict
rime_failing_row_dict = rime_failing_row_instance.to_dict()
# create an instance of RimeFailingRow from a dict
rime_failing_row_from_dict = RimeFailingRow.from_dict(rime_failing_row_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

