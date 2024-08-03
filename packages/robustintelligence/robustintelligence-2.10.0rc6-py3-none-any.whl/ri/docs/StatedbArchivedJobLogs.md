# StatedbArchivedJobLogs

ArchivedJobLogs contains the URL to the archived logs for a RIME job and the expiration time of the URL.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | [**RimeSafeURL**](RimeSafeURL.md) |  | [optional] 
**expiration_time** | **datetime** |  | [optional] 

## Example

```python
from ri.apiclient.models.statedb_archived_job_logs import StatedbArchivedJobLogs

# TODO update the JSON string below
json = "{}"
# create an instance of StatedbArchivedJobLogs from a JSON string
statedb_archived_job_logs_instance = StatedbArchivedJobLogs.from_json(json)
# print the JSON string representation of the object
print(StatedbArchivedJobLogs.to_json())

# convert the object into a dict
statedb_archived_job_logs_dict = statedb_archived_job_logs_instance.to_dict()
# create an instance of StatedbArchivedJobLogs from a dict
statedb_archived_job_logs_from_dict = StatedbArchivedJobLogs.from_dict(statedb_archived_job_logs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

