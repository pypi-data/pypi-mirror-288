# RimeSearchSpec

SearchSpec will return all elements that contain the provided expression as a substring in any of the specified search_fields.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expression** | **str** |  | [optional] 
**search_fields** | **List[str]** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_search_spec import RimeSearchSpec

# TODO update the JSON string below
json = "{}"
# create an instance of RimeSearchSpec from a JSON string
rime_search_spec_instance = RimeSearchSpec.from_json(json)
# print the JSON string representation of the object
print(RimeSearchSpec.to_json())

# convert the object into a dict
rime_search_spec_dict = rime_search_spec_instance.to_dict()
# create an instance of RimeSearchSpec from a dict
rime_search_spec_from_dict = RimeSearchSpec.from_dict(rime_search_spec_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

