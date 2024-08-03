# DataProfilingFeatureRelationshipInfo

Specifies configuration values for feature relationships.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**num_feats_to_profile** | **str** | Number of features to profile for smart feature sampling. | [optional] 
**compute_feature_relationships** | **bool** | Specifies whether to compute feature relationships. | [optional] 
**compute_numeric_feature_relationships** | **bool** | Specifies whether to compute feature relationships for numeric columns. | [optional] 
**ignore_nan_for_feature_relationships** | **bool** | Specifies whether to ignore NaN values when computing feature relationships. | [optional] 

## Example

```python
from ri.apiclient.models.data_profiling_feature_relationship_info import DataProfilingFeatureRelationshipInfo

# TODO update the JSON string below
json = "{}"
# create an instance of DataProfilingFeatureRelationshipInfo from a JSON string
data_profiling_feature_relationship_info_instance = DataProfilingFeatureRelationshipInfo.from_json(json)
# print the JSON string representation of the object
print(DataProfilingFeatureRelationshipInfo.to_json())

# convert the object into a dict
data_profiling_feature_relationship_info_dict = data_profiling_feature_relationship_info_instance.to_dict()
# create an instance of DataProfilingFeatureRelationshipInfo from a dict
data_profiling_feature_relationship_info_from_dict = DataProfilingFeatureRelationshipInfo.from_dict(data_profiling_feature_relationship_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

