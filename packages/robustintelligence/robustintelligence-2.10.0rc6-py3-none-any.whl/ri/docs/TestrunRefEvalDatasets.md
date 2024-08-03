# TestrunRefEvalDatasets

RefEvalDatasets uniquely specifies information about reference and evaluation Datasets.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ref_dataset_id** | **str** | Uniquely specifies a reference Dataset. | [optional] 
**eval_dataset_id** | **str** | Uniquely specifies an evaluation Dataset. | 
**eval_dataset_time_interval** | [**RimeTimeInterval**](RimeTimeInterval.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrun_ref_eval_datasets import TestrunRefEvalDatasets

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunRefEvalDatasets from a JSON string
testrun_ref_eval_datasets_instance = TestrunRefEvalDatasets.from_json(json)
# print the JSON string representation of the object
print(TestrunRefEvalDatasets.to_json())

# convert the object into a dict
testrun_ref_eval_datasets_dict = testrun_ref_eval_datasets_instance.to_dict()
# create an instance of TestrunRefEvalDatasets from a dict
testrun_ref_eval_datasets_from_dict = TestrunRefEvalDatasets.from_dict(testrun_ref_eval_datasets_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

