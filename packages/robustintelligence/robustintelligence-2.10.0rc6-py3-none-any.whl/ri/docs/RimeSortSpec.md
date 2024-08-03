# RimeSortSpec


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sort_order** | [**RimeOrder**](RimeOrder.md) |  | [optional] 
**sort_by** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_sort_spec import RimeSortSpec

# TODO update the JSON string below
json = "{}"
# create an instance of RimeSortSpec from a JSON string
rime_sort_spec_instance = RimeSortSpec.from_json(json)
# print the JSON string representation of the object
print(RimeSortSpec.to_json())

# convert the object into a dict
rime_sort_spec_dict = rime_sort_spec_instance.to_dict()
# create an instance of RimeSortSpec from a dict
rime_sort_spec_from_dict = RimeSortSpec.from_dict(rime_sort_spec_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

