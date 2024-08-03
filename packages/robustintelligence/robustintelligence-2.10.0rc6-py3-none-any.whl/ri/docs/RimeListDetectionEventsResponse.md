# RimeListDetectionEventsResponse

ListDetectionEventsResponse repesents a single page of detection events returned from the backend.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**events** | [**List[DetectionDetectionEvent]**](DetectionDetectionEvent.md) | Page of events returned from the backend. | [optional] 
**next_page_token** | **str** | Page token to use in the next ListDetectionEvents call. | [optional] 
**has_more** | **bool** | Indicates whether there are more events to return. | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_detection_events_response import RimeListDetectionEventsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListDetectionEventsResponse from a JSON string
rime_list_detection_events_response_instance = RimeListDetectionEventsResponse.from_json(json)
# print the JSON string representation of the object
print(RimeListDetectionEventsResponse.to_json())

# convert the object into a dict
rime_list_detection_events_response_dict = rime_list_detection_events_response_instance.to_dict()
# create an instance of RimeListDetectionEventsResponse from a dict
rime_list_detection_events_response_from_dict = RimeListDetectionEventsResponse.from_dict(rime_list_detection_events_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

