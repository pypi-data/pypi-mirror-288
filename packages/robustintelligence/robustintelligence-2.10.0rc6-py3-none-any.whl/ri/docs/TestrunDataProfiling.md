# TestrunDataProfiling

Specifies configuration values for profiling a dataset.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**num_quantiles** | **str** | The number of quantiles to split numeric subsets into. | [optional] 
**num_subsets** | **str** | The number of subsets to test. This field is sorted by count. | [optional] 
**column_type_info** | [**DataProfilingColumnTypeInfo**](DataProfilingColumnTypeInfo.md) |  | [optional] 
**feature_relationship_info** | [**DataProfilingFeatureRelationshipInfo**](DataProfilingFeatureRelationshipInfo.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrun_data_profiling import TestrunDataProfiling

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunDataProfiling from a JSON string
testrun_data_profiling_instance = TestrunDataProfiling.from_json(json)
# print the JSON string representation of the object
print(TestrunDataProfiling.to_json())

# convert the object into a dict
testrun_data_profiling_dict = testrun_data_profiling_instance.to_dict()
# create an instance of TestrunDataProfiling from a dict
testrun_data_profiling_from_dict = TestrunDataProfiling.from_dict(testrun_data_profiling_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

