# ListPredictionSetsRequestPredictionQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_id** | **str** | Uniquely specifies a Model. | [optional] 
**dataset_id** | **str** | Uniquely specifies a Dataset. | [optional] 

## Example

```python
from ri.apiclient.models.list_prediction_sets_request_prediction_query import ListPredictionSetsRequestPredictionQuery

# TODO update the JSON string below
json = "{}"
# create an instance of ListPredictionSetsRequestPredictionQuery from a JSON string
list_prediction_sets_request_prediction_query_instance = ListPredictionSetsRequestPredictionQuery.from_json(json)
# print the JSON string representation of the object
print(ListPredictionSetsRequestPredictionQuery.to_json())

# convert the object into a dict
list_prediction_sets_request_prediction_query_dict = list_prediction_sets_request_prediction_query_instance.to_dict()
# create an instance of ListPredictionSetsRequestPredictionQuery from a dict
list_prediction_sets_request_prediction_query_from_dict = ListPredictionSetsRequestPredictionQuery.from_dict(list_prediction_sets_request_prediction_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

