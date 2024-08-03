# TestrunresultTestBatchResultDisplay

Display contains information for displaying the test case in the RI web app. The contents of each field are unstable; it is not recommended to parse them programmatically.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**summary_details** | **bytearray** | Summary details are marshalled JSON, the field is not used and is empty. | [optional] 
**table_columns_to_show** | [**List[RimeTableColumn]**](RimeTableColumn.md) |  | [optional] 
**long_description_tabs** | [**List[RimeLongDescriptionTab]**](RimeLongDescriptionTab.md) | More detailed information about the test batch. | [optional] 
**description_html** | **str** | Description of the test batch result that may contain HTML. | [optional] 

## Example

```python
from ri.apiclient.models.testrunresult_test_batch_result_display import TestrunresultTestBatchResultDisplay

# TODO update the JSON string below
json = "{}"
# create an instance of TestrunresultTestBatchResultDisplay from a JSON string
testrunresult_test_batch_result_display_instance = TestrunresultTestBatchResultDisplay.from_json(json)
# print the JSON string representation of the object
print(TestrunresultTestBatchResultDisplay.to_json())

# convert the object into a dict
testrunresult_test_batch_result_display_dict = testrunresult_test_batch_result_display_instance.to_dict()
# create an instance of TestrunresultTestBatchResultDisplay from a dict
testrunresult_test_batch_result_display_from_dict = TestrunresultTestBatchResultDisplay.from_dict(testrunresult_test_batch_result_display_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

