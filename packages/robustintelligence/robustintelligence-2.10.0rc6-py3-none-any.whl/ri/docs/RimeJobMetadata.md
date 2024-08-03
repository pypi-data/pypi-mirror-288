# RimeJobMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job_id** | **str** | The identifier within our job tracking system. | [optional] 
**job_type** | [**RimeJobType**](RimeJobType.md) |  | [optional] 
**status** | [**RimeJobStatus**](RimeJobStatus.md) |  | [optional] 
**start_time** | **datetime** | The start time of the job (when the job transitions in state to RUNNING). Note, this may not be populated immediately when the job is created. | [optional] 
**creation_time** | **datetime** | The time the job was created. | [optional] 
**completion_time** | **datetime** | The time the job entered a terminal state. | [optional] 
**running_time_secs** | **float** | The total running time a job took to complete if the job is finished or the current running time if the job is still in progress (seconds). | [optional] 
**job_data** | [**RimeJobData**](RimeJobData.md) |  | [optional] 
**job_progress_str** | **str** | Pretty-printed, human-readable representation of job progress. This will only be populated for Read methods with the FULL job view. To get schema for progress for each type of job, see the field inside that job&#39;s job data message (e.g. StressTestJobProgress). Note: this is unstable, do not rely on parsing this. | [optional] 
**cancellation_requested** | **bool** | Marked when the job has been requested to be cancelled by the user. This is declarative; once the user requests cancellation, the backend will conduct garbage collection on the job in the background and eventually update the status of the job to CANCELLED. | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**archived_job_logs** | [**StatedbArchivedJobLogs**](StatedbArchivedJobLogs.md) |  | [optional] 
**error_msg** | **str** | User-facing error message for the job. | [optional] 

## Example

```python
from ri.apiclient.models.rime_job_metadata import RimeJobMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of RimeJobMetadata from a JSON string
rime_job_metadata_instance = RimeJobMetadata.from_json(json)
# print the JSON string representation of the object
print(RimeJobMetadata.to_json())

# convert the object into a dict
rime_job_metadata_dict = rime_job_metadata_instance.to_dict()
# create an instance of RimeJobMetadata from a dict
rime_job_metadata_from_dict = RimeJobMetadata.from_dict(rime_job_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

