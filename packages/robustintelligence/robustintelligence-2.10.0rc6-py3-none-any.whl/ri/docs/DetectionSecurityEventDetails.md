# DetectionSecurityEventDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | [**SecurityEventDetailsSecurityEventType**](SecurityEventDetailsSecurityEventType.md) |  | [optional] 
**effect_on_model** | **List[str]** |  | [optional] 
**possible_intent** | **List[str]** |  | [optional] 
**evidence** | **List[str]** |  | [optional] 
**recommendations** | **List[str]** |  | [optional] 
**datapoints** | [**List[SecurityEventDetailsFlaggedDatapoint]**](SecurityEventDetailsFlaggedDatapoint.md) | Include descriptions of all the flagged datapoints for the attack. | [optional] 

## Example

```python
from ri.apiclient.models.detection_security_event_details import DetectionSecurityEventDetails

# TODO update the JSON string below
json = "{}"
# create an instance of DetectionSecurityEventDetails from a JSON string
detection_security_event_details_instance = DetectionSecurityEventDetails.from_json(json)
# print the JSON string representation of the object
print(DetectionSecurityEventDetails.to_json())

# convert the object into a dict
detection_security_event_details_dict = detection_security_event_details_instance.to_dict()
# create an instance of DetectionSecurityEventDetails from a dict
detection_security_event_details_from_dict = DetectionSecurityEventDetails.from_dict(detection_security_event_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

