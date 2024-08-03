# DetectionDetectionEvent

DetectionEvent describes a specific problem with a model. Examples of issues reported by this event include performance metrics dropping below a specified threshold or detecting an evasion attack. Each event is attached to a parent monitor that has a corresponding test in the RIME engine.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**firewall_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**event_type** | [**DetectionEventType**](DetectionEventType.md) |  | [optional] 
**severity** | [**RimeSeverity**](RimeSeverity.md) |  | [optional] 
**event_object_id** | **str** | The event object varies with the event type. CT and security events use a monitor. Offline Test events use the test run. | [optional] 
**event_object_name** | **str** | event_object_name to avoid extra query from UI to display, and allow easier search support with DB. If the event object is renamed, the event will not be updated. | [optional] 
**event_time_range** | [**RimeTimeInterval**](RimeTimeInterval.md) |  | [optional] 
**last_update_time** | **datetime** |  | [optional] 
**risk_category_type** | [**RiskscoreRiskCategoryType**](RiskscoreRiskCategoryType.md) |  | [optional] 
**test_category** | [**TestrunTestCategoryType**](TestrunTestCategoryType.md) |  | [optional] 
**description** | **str** | Human-readable description of the event. | [optional] 
**description_html** | **str** | Description of the event with HTML for nicer rendering. | [optional] 
**resolution** | [**DetectionResolution**](DetectionResolution.md) |  | [optional] 
**detail** | [**DetectionEventDetail**](DetectionEventDetail.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.detection_detection_event import DetectionDetectionEvent

# TODO update the JSON string below
json = "{}"
# create an instance of DetectionDetectionEvent from a JSON string
detection_detection_event_instance = DetectionDetectionEvent.from_json(json)
# print the JSON string representation of the object
print(DetectionDetectionEvent.to_json())

# convert the object into a dict
detection_detection_event_dict = detection_detection_event_instance.to_dict()
# create an instance of DetectionDetectionEvent from a dict
detection_detection_event_from_dict = DetectionDetectionEvent.from_dict(detection_detection_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

