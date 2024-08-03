# TestrunresultTestCaseDisplay

Display contains information for displaying the test case in the web UI. The contents of each field are unstable; it is not recommended to parse them programmatically.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**table_info** | **bytearray** | Table info contains information for displaying the test case in a table in the FE. | [optional] 
**details** | **bytearray** | Details includes ML-specified details for the test case. This can include graphs, HTML, etc. | [optional] 
**details_layout** | **List[str]** |  | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_test_case_display import TestrunresultTestCaseDisplay

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultTestCaseDisplay from a JSON string
testrunresult_test_case_display_instance = TestrunresultTestCaseDisplay.from_json(json)
# print the JSON string representation of the object
print(TestrunresultTestCaseDisplay.to_json())

# convert the object into a dict
testrunresult_test_case_display_dict = testrunresult_test_case_display_instance.to_dict()
# create an instance of TestrunresultTestCaseDisplay from a dict
testrunresult_test_case_display_from_dict = TestrunresultTestCaseDisplay.from_dict(testrunresult_test_case_display_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

