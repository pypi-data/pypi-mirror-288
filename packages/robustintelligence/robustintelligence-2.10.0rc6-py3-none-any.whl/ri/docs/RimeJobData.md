# RimeJobData

Note that progress may not be populated depending on the parameters of the request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**stress** | [**JobDataStressTest**](JobDataStressTest.md) |  | [optional] 
**continuous_inc** | [**JobDataContinuousIncrementalTest**](JobDataContinuousIncrementalTest.md) |  | [optional] 
**file_scan** | [**JobDataScan**](JobDataScan.md) |  | [optional] 
**cross_plane_res** | [**CrossplanetaskCrossPlaneResponse**](CrossplanetaskCrossPlaneResponse.md) |  | [optional] 
**generative_model** | [**RimeJobDataGenerativeModelTest**](RimeJobDataGenerativeModelTest.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_job_data import RimeJobData

# TODO update the JSON string below
json = "{}"
# create an instance of RimeJobData from a JSON string
rime_job_data_instance = RimeJobData.from_json(json)
# print the JSON string representation of the object
print(RimeJobData.to_json())

# convert the object into a dict
rime_job_data_dict = rime_job_data_instance.to_dict()
# create an instance of RimeJobData from a dict
rime_job_data_from_dict = RimeJobData.from_dict(rime_job_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

