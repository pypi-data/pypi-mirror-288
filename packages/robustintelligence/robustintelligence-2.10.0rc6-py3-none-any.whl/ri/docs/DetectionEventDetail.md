# DetectionEventDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metric_degradation** | **object** |  | [optional] 
**security** | [**DetectionSecurityEventDetails**](DetectionSecurityEventDetails.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.detection_event_detail import DetectionEventDetail

# TODO update the JSON string below
json = "{}"
# create an instance of DetectionEventDetail from a JSON string
detection_event_detail_instance = DetectionEventDetail.from_json(json)
# print the JSON string representation of the object
print(DetectionEventDetail.to_json())

# convert the object into a dict
detection_event_detail_dict = detection_event_detail_instance.to_dict()
# create an instance of DetectionEventDetail from a dict
detection_event_detail_from_dict = DetectionEventDetail.from_dict(detection_event_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

