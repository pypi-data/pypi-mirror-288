# DataProfilingColumnTypeInfo

Specifies configuration values for column types.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**min_nunique_for_numeric** | **str** | Specifies a minimum number of unique values in a column. Columns with at least the specified number of unique values are considered numeric columns. Columns with fewer unique values are considered categorical. | [optional] 
**numeric_violation_threshold** | **float** | Maximum fraction of violations when assigning numeric columns (not including missing values). | [optional] 
**categorical_violation_threshold** | **float** | Maximum fraction of violations when assigning categorical subtypes (not including missing values). | [optional] 
**min_unique_prop** | **float** | If data has at least min_unique_prop proportion of unique values then classify as a column that must have unique values. | [optional] 
**allow_float_unique** | **bool** | Allow float columns to be inferred as unique values. | [optional] 
**numeric_range_inference_threshold** | **float** | The percent of non-null values which must fall within an inferrable numeric range ([0,1], [0,inf), (-inf, inf)) for that to be inferred as the valid range for a numeric column. If 1.0 (default), then all non-null values must fall within the range for that range to be inferred. For ex: if 98% of feature X falls in [0, 1] but 100% of feature X falls in [0, inf) then we&#39;ll infer [0, inf) as the valid range for feature X. However, if this threshold is 0.98, we&#39;ll instead infer [0, 1] as feature X&#39;s range. | [optional] 
**unseen_values_allowed_criteria** | **float** | Either the fraction or count of unique values in the ref set required to infer that a categorical feature is allowed to have unseen values in the eval set. If the criteria is provided as a float in [0.0, 1.0] it will be treated as the fraction of unique non-null values divided by the total number of non-null values required to infer that unseen values are allowed. If provided as an integer in [2, inf), it will be treated as the count of non-null unique values required to infer that unseen values are allowed. | [optional] 

## Example

```python
from ri.apiclient.models.data_profiling_column_type_info import DataProfilingColumnTypeInfo

# TODO update the JSON string below
json = "{}"
# create an instance of DataProfilingColumnTypeInfo from a JSON string
data_profiling_column_type_info_instance = DataProfilingColumnTypeInfo.from_json(json)
# print the JSON string representation of the object
print(DataProfilingColumnTypeInfo.to_json())

# convert the object into a dict
data_profiling_column_type_info_dict = data_profiling_column_type_info_instance.to_dict()
# create an instance of DataProfilingColumnTypeInfo from a dict
data_profiling_column_type_info_from_dict = DataProfilingColumnTypeInfo.from_dict(data_profiling_column_type_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

