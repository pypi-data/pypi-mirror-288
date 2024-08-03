# RimeSeverityCounts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**num_none_severity** | **str** |  | [optional] 
**num_low_severity** | **str** |  | [optional] 
**num_high_severity** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_severity_counts import RimeSeverityCounts

# TODO update the JSON string below
json = "{}"
# create an instance of RimeSeverityCounts from a JSON string
rime_severity_counts_instance = RimeSeverityCounts.from_json(json)
# print the JSON string representation of the object
print(RimeSeverityCounts.to_json())

# convert the object into a dict
rime_severity_counts_dict = rime_severity_counts_instance.to_dict()
# create an instance of RimeSeverityCounts from a dict
rime_severity_counts_from_dict = RimeSeverityCounts.from_dict(rime_severity_counts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

