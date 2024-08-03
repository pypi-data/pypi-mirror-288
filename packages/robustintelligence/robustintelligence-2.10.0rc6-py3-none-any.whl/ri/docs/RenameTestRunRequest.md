# RenameTestRunRequest

RenameTestRunRequest defines a request to rename a specified test run to a new name.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The new name of the Test Run. | [optional] 

## Example

```python
from ri.apiclient.models.rename_test_run_request import RenameTestRunRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RenameTestRunRequest from a JSON string
rename_test_run_request_instance = RenameTestRunRequest.from_json(json)
# print the JSON string representation of the object
print(RenameTestRunRequest.to_json())

# convert the object into a dict
rename_test_run_request_dict = rename_test_run_request_instance.to_dict()
# create an instance of RenameTestRunRequest from a dict
rename_test_run_request_from_dict = RenameTestRunRequest.from_dict(rename_test_run_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

