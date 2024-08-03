# RimeJobDataGenerativeModelTest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**progress** | [**RimeGenerativeModelTestProgress**](RimeGenerativeModelTestProgress.md) |  | [optional] 
**name** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**model_output_is_sensitive** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_job_data_generative_model_test import RimeJobDataGenerativeModelTest

# TODO update the JSON string below
json = "{}"
# create an instance of RimeJobDataGenerativeModelTest from a JSON string
rime_job_data_generative_model_test_instance = RimeJobDataGenerativeModelTest.from_json(json)
# print the JSON string representation of the object
print(RimeJobDataGenerativeModelTest.to_json())

# convert the object into a dict
rime_job_data_generative_model_test_dict = rime_job_data_generative_model_test_instance.to_dict()
# create an instance of RimeJobDataGenerativeModelTest from a dict
rime_job_data_generative_model_test_from_dict = RimeJobDataGenerativeModelTest.from_dict(rime_job_data_generative_model_test_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

