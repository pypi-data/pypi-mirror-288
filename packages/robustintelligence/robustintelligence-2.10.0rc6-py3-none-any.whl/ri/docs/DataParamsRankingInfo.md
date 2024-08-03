# DataParamsRankingInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**query_col** | **str** | Name of column in dataset that contains the query ids. | [optional] 
**nqueries** | **str** | Number of queries to consider. If null, will use all queries. | [optional] 
**nrows_per_query** | **str** | Number of rows to use per query. If null, will use all rows. | [optional] 
**drop_query_id** | **bool** | Whether to drop the query ID column from the dataset to avoid passing as a feature to the model. | [optional] 

## Example

```python
from ri.apiclient.models.data_params_ranking_info import DataParamsRankingInfo

# TODO update the JSON string below
json = "{}"
# create an instance of DataParamsRankingInfo from a JSON string
data_params_ranking_info_instance = DataParamsRankingInfo.from_json(json)
# print the JSON string representation of the object
print(DataParamsRankingInfo.to_json())

# convert the object into a dict
data_params_ranking_info_dict = data_params_ranking_info_instance.to_dict()
# create an instance of DataParamsRankingInfo from a dict
data_params_ranking_info_from_dict = DataParamsRankingInfo.from_dict(data_params_ranking_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

