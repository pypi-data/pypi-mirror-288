# RimeListPredictionSetsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**predictions** | [**List[RegistrypredictionPrediction]**](RegistrypredictionPrediction.md) |  | [optional] 
**next_page_token** | **str** |  | [optional] 
**has_more** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_prediction_sets_response import RimeListPredictionSetsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListPredictionSetsResponse from a JSON string
rime_list_prediction_sets_response_instance = RimeListPredictionSetsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListPredictionSetsResponse.to_json())

# convert the object into a dict
rime_list_prediction_sets_response_dict = rime_list_prediction_sets_response_instance.to_dict()
# create an instance of RimeListPredictionSetsResponse from a dict
rime_list_prediction_sets_response_from_dict = RimeListPredictionSetsResponse.from_dict(rime_list_prediction_sets_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

