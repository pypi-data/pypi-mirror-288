# RimeGetTestRunIDResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_run_id** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_test_run_id_response import RimeGetTestRunIDResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetTestRunIDResponse from a JSON string
rime_get_test_run_id_response_instance = RimeGetTestRunIDResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetTestRunIDResponse.to_json())

# convert the object into a dict
rime_get_test_run_id_response_dict = rime_get_test_run_id_response_instance.to_dict()
# create an instance of RimeGetTestRunIDResponse from a dict
rime_get_test_run_id_response_from_dict = RimeGetTestRunIDResponse.from_dict(rime_get_test_run_id_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

