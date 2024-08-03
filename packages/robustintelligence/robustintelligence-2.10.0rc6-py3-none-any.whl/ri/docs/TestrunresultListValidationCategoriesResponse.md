# TestrunresultListValidationCategoriesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**categories** | [**List[TestrunTestCategoryType]**](TestrunTestCategoryType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_list_validation_categories_response import TestrunresultListValidationCategoriesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultListValidationCategoriesResponse from a JSON string
testrunresult_list_validation_categories_response_instance = TestrunresultListValidationCategoriesResponse.from_json(json)
# print the JSON string representation of the object
print(TestrunresultListValidationCategoriesResponse.to_json())

# convert the object into a dict
testrunresult_list_validation_categories_response_dict = testrunresult_list_validation_categories_response_instance.to_dict()
# create an instance of TestrunresultListValidationCategoriesResponse from a dict
testrunresult_list_validation_categories_response_from_dict = TestrunresultListValidationCategoriesResponse.from_dict(testrunresult_list_validation_categories_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

