# GenerativevalidationJobInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**job_status** | [**RimeJobStatus**](RimeJobStatus.md) |  | [optional] 
**completion_time** | **datetime** | When the job finished. | [optional] 

## Example

```python
from ri.apiclient.models.generativevalidation_job_info import GenerativevalidationJobInfo

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativevalidationJobInfo from a JSON string
generativevalidation_job_info_instance = GenerativevalidationJobInfo.from_json(json)
# print the JSON string representation of the object
print(GenerativevalidationJobInfo.to_json())

# convert the object into a dict
generativevalidation_job_info_dict = generativevalidation_job_info_instance.to_dict()
# create an instance of GenerativevalidationJobInfo from a dict
generativevalidation_job_info_from_dict = GenerativevalidationJobInfo.from_dict(generativevalidation_job_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

