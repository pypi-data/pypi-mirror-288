# RegistryDataParams

DataParams specifies the parameters for a dataset.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label_col** | **str** | Naming of special columns. | [optional] 
**timestamp_col** | **str** | Column to look at for CT timestamp. | [optional] 
**class_names** | **List[str]** | List of label class names. | [optional] 
**ranking_info** | [**DataParamsRankingInfo**](DataParamsRankingInfo.md) |  | [optional] 
**nrows** | **str** | Dataset size parameters. Number of rows of data to load and test. If null, will load all rows. | [optional] 
**nrows_per_time_bin** | **str** | Number of rows of data per time bin to load and test in CT. If null, will load all rows. | [optional] 
**sample** | **bool** | Whether to sample rows in the data. Default is True. | [optional] 
**categorical_features** | **List[str]** | Feature types and relations. | [optional] 
**protected_features** | **List[str]** | Features that are protected attributes. If Bias and Fairness category is specified, these tests will run only over protected_features. | [optional] 
**features_not_in_model** | **List[str]** |  | [optional] 
**text_features** | **List[str]** | Text features to run NLP tests over. | [optional] 
**image_features** | **List[str]** | Image features to run CV tests over. | [optional] 
**prompt_col** | **str** | Prompt template column for Generative tasks. | [optional] 
**intersections** | [**List[DataParamsFeatureIntersection]**](DataParamsFeatureIntersection.md) | A list of arrays of features. Each array represents the intersection of features on which certain subset and fairness tests are run. | [optional] 
**loading_kwargs** | **str** | Paths for external resources. Keyword arguments to be passed to the pandas loading function (either pd.read_CSV or pd.read_Parquet, depending on your data format). NOTE: if you wish to specify nrows, this should NOT be done with kwargs. | [optional] 
**feature_type_path** | **str** | Path to a CSV file that specifies the data type of each feature. The file should have two columns: FeatureName and FeatureType. | [optional] 
**image_load_path** | **str** | Path to a python file containing a custom function for loading images in the dataset. | [optional] 
**experimental_fields** | **Dict[str, object]** | Fields that enable experimental functionality.  WARNING: these fields are experimental; ie, their functionality may not be reliable or backwards-compatible. Do not use these fields in production. | [optional] 

## Example

```python
from ri.apiclient.models.registry_data_params import RegistryDataParams

# TODO update the JSON string below
json = "{}"
# create an instance of RegistryDataParams from a JSON string
registry_data_params_instance = RegistryDataParams.from_json(json)
# print the JSON string representation of the object
print(RegistryDataParams.to_json())

# convert the object into a dict
registry_data_params_dict = registry_data_params_instance.to_dict()
# create an instance of RegistryDataParams from a dict
registry_data_params_from_dict = RegistryDataParams.from_dict(registry_data_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

