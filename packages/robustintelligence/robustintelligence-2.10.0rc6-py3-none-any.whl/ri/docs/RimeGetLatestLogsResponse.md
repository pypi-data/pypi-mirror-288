# RimeGetLatestLogsResponse

GetLatestLogsResponse is the response for GetLatestLogs containing the logs of the latest pod to run a specified job.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**chunk** | **str** | A chunk of the logs to be returned to the client. Size is bounded to 1000000 bytes. | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_latest_logs_response import RimeGetLatestLogsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetLatestLogsResponse from a JSON string
rime_get_latest_logs_response_instance = RimeGetLatestLogsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetLatestLogsResponse.to_json())

# convert the object into a dict
rime_get_latest_logs_response_dict = rime_get_latest_logs_response_instance.to_dict()
# create an instance of RimeGetLatestLogsResponse from a dict
rime_get_latest_logs_response_from_dict = RimeGetLatestLogsResponse.from_dict(rime_get_latest_logs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

