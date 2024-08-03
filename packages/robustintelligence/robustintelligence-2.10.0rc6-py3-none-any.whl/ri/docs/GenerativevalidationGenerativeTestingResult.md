# GenerativevalidationGenerativeTestingResult

GenerativeTestingResult represents a single result of testing a Generative model with attack prompts. The model output is sent to a detection layer, which indicates whether it contains objectionable content. There is a single test result for the \"attack_technique\", \"attack_objective\", and \"objective_sub_category\" combination.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**job_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**attack_technique** | **str** | The attack technique used in the prompt. This is a string because the types of attacks changes frequently over time depending on our threat intelligence. | [optional] 
**attack_objective** | [**RimeAttackObjective**](RimeAttackObjective.md) |  | [optional] 
**objective_sub_category** | [**GenerativevalidationObjectiveSubCategory**](GenerativevalidationObjectiveSubCategory.md) |  | [optional] 
**failing_examples** | [**List[GenerativeTestingResultExample]**](GenerativeTestingResultExample.md) | List of failing examples to demonstrate failures in this category. | [optional] 
**severity** | [**LibgenerativeSeverity**](LibgenerativeSeverity.md) |  | [optional] 
**owasp_standards** | [**List[GenerativeTestingResultStandardInfo]**](GenerativeTestingResultStandardInfo.md) | List of the OWASP AI risk standards associated with the attacks in these results. | [optional] 
**nist_standards** | [**List[GenerativeTestingResultStandardInfo]**](GenerativeTestingResultStandardInfo.md) | List of the NIST AI risk standards associated with the attacks in these results. | [optional] 
**mitre_standards** | [**List[GenerativeTestingResultStandardInfo]**](GenerativeTestingResultStandardInfo.md) | List of the MITRE AI risk standards associated with the attacks in these results. | [optional] 
**attacks_attempted** | **int** | The number of attacks attempted for these results. | [optional] 
**threat** | [**GenerativevalidationThreat**](GenerativevalidationThreat.md) |  | [optional] 
**successful_attacks** | **int** | The number of successful attacks completed for these results. | [optional] 
**skipped_reason** | **str** | Indicates that the test was skipped and provides a reason. If the test was not skipped this will be the empty string. | [optional] 
**generative_validation_test_run_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.generativevalidation_generative_testing_result import GenerativevalidationGenerativeTestingResult

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativevalidationGenerativeTestingResult from a JSON string
generativevalidation_generative_testing_result_instance = GenerativevalidationGenerativeTestingResult.from_json(json)
# print the JSON string representation of the object
print(GenerativevalidationGenerativeTestingResult.to_json())

# convert the object into a dict
generativevalidation_generative_testing_result_dict = generativevalidation_generative_testing_result_instance.to_dict()
# create an instance of GenerativevalidationGenerativeTestingResult from a dict
generativevalidation_generative_testing_result_from_dict = GenerativevalidationGenerativeTestingResult.from_dict(generativevalidation_generative_testing_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

