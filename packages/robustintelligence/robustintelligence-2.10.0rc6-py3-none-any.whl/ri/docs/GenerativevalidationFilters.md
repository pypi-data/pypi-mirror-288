# GenerativevalidationFilters

Filters provides a mechanism for specifying which attacks to run. An empty set of filters will result in all tests being run.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attack_objectives** | [**List[RimeAttackObjective]**](RimeAttackObjective.md) | Only attacks that have one of these attack objectives will be run. If empty, this filter is not applied. | [optional] 

## Example

```python
from ri.apiclient.models.generativevalidation_filters import GenerativevalidationFilters

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativevalidationFilters from a JSON string
generativevalidation_filters_instance = GenerativevalidationFilters.from_json(json)
# print the JSON string representation of the object
print(GenerativevalidationFilters.to_json())

# convert the object into a dict
generativevalidation_filters_dict = generativevalidation_filters_instance.to_dict()
# create an instance of GenerativevalidationFilters from a dict
generativevalidation_filters_from_dict = GenerativevalidationFilters.from_dict(generativevalidation_filters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

