# RimeListDetectionEventsRequestQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**firewall_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**event_object_id** | **str** | Optional: return a series of detection events for a single object. | [optional] 
**event_time_range** | [**RimeTimeInterval**](RimeTimeInterval.md) |  | [optional] 
**severity** | [**RimeSeverity**](RimeSeverity.md) |  | [optional] 
**event_types** | [**List[DetectionEventType]**](DetectionEventType.md) | Optional: When the list is empty, returns all. | [optional] 
**risk_category_types** | [**List[RiskscoreRiskCategoryType]**](RiskscoreRiskCategoryType.md) | Optional: When the list is empty, returns all. | [optional] 
**test_categories** | [**List[TestrunTestCategoryType]**](TestrunTestCategoryType.md) | Optional: When the list is empty, return all. | [optional] 
**sort** | [**RimeSortSpec**](RimeSortSpec.md) |  | [optional] 
**include_resolved** | **bool** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_list_detection_events_request_query import RimeListDetectionEventsRequestQuery

# TODO update the JSON string below
json = "{}"
# create an instance of RimeListDetectionEventsRequestQuery from a JSON string
rime_list_detection_events_request_query_instance = RimeListDetectionEventsRequestQuery.from_json(json)
# print the JSON string representation of the object
print(RimeListDetectionEventsRequestQuery.to_json())

# convert the object into a dict
rime_list_detection_events_request_query_dict = rime_list_detection_events_request_query_instance.to_dict()
# create an instance of RimeListDetectionEventsRequestQuery from a dict
rime_list_detection_events_request_query_from_dict = RimeListDetectionEventsRequestQuery.from_dict(rime_list_detection_events_request_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

