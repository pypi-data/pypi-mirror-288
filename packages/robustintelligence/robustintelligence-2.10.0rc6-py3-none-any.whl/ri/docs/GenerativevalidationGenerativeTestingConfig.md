# GenerativevalidationGenerativeTestingConfig

GenerativeTestingConfig is the configuration to run a generative model test.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt_bank** | [**GenerativevalidationPromptBank**](GenerativevalidationPromptBank.md) |  | [optional] 
**system_prompt** | **str** | The system prompt that is currently active on the provided endpoint. If this is not set, system prompt extraction tests will be skipped. | [optional] 
**connection** | [**GenerativevalidationModelConnectionSpec**](GenerativevalidationModelConnectionSpec.md) |  | [optional] 
**model_output_is_sensitive** | **bool** | Will not be saved to the database, logged in plaintext, etc. | [optional] 
**filters** | [**GenerativevalidationFilters**](GenerativevalidationFilters.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.generativevalidation_generative_testing_config import GenerativevalidationGenerativeTestingConfig

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativevalidationGenerativeTestingConfig from a JSON string
generativevalidation_generative_testing_config_instance = GenerativevalidationGenerativeTestingConfig.from_json(json)
# print the JSON string representation of the object
print(GenerativevalidationGenerativeTestingConfig.to_json())

# convert the object into a dict
generativevalidation_generative_testing_config_dict = generativevalidation_generative_testing_config_instance.to_dict()
# create an instance of GenerativevalidationGenerativeTestingConfig from a dict
generativevalidation_generative_testing_config_from_dict = GenerativevalidationGenerativeTestingConfig.from_dict(generativevalidation_generative_testing_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

