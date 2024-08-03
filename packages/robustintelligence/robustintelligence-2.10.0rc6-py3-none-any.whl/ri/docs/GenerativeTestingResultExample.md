# GenerativeTestingResultExample


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attack_prompt** | **str** | RI attack prompt to elicit issues. | [optional] 
**model_output** | **str** | Output from the generative model on the given prompt. | [optional] 

## Example

```python
from ri.apiclient.models.generative_testing_result_example import GenerativeTestingResultExample

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativeTestingResultExample from a JSON string
generative_testing_result_example_instance = GenerativeTestingResultExample.from_json(json)
# print the JSON string representation of the object
print(GenerativeTestingResultExample.to_json())

# convert the object into a dict
generative_testing_result_example_dict = generative_testing_result_example_instance.to_dict()
# create an instance of GenerativeTestingResultExample from a dict
generative_testing_result_example_from_dict = GenerativeTestingResultExample.from_dict(generative_testing_result_example_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

