# RuntimeinfoRunTimeInfo

Configures run-time details about how a job should be run.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_image** | [**RuntimeinfoCustomImageType**](RuntimeinfoCustomImageType.md) |  | [optional] 
**resource_request** | [**RuntimeinfoResourceRequest**](RuntimeinfoResourceRequest.md) |  | [optional] 
**explicit_errors** | **bool** | Specifies whether the job will return silent errors. By default, this is set to false, and silent errors are not returned. | [optional] 
**random_seed** | **str** | Random seed to use for the Job, so that Test Job result will be deterministic. | [optional] 

## Example

```python
from ri.apiclient.models.runtimeinfo_run_time_info import RuntimeinfoRunTimeInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RuntimeinfoRunTimeInfo from a JSON string
runtimeinfo_run_time_info_instance = RuntimeinfoRunTimeInfo.from_json(json)
# print the JSON string representation of the object
print(RuntimeinfoRunTimeInfo.to_json())

# convert the object into a dict
runtimeinfo_run_time_info_dict = runtimeinfo_run_time_info_instance.to_dict()
# create an instance of RuntimeinfoRunTimeInfo from a dict
runtimeinfo_run_time_info_from_dict = RuntimeinfoRunTimeInfo.from_dict(runtimeinfo_run_time_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

