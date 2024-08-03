# DetectionResolution


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resolve_time** | **datetime** |  | [optional] 
**resolved_by_user_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.detection_resolution import DetectionResolution

# TODO update the JSON string below
json = "{}"
# create an instance of DetectionResolution from a JSON string
detection_resolution_instance = DetectionResolution.from_json(json)
# print the JSON string representation of the object
print(DetectionResolution.to_json())

# convert the object into a dict
detection_resolution_dict = detection_resolution_instance.to_dict()
# create an instance of DetectionResolution from a dict
detection_resolution_from_dict = DetectionResolution.from_dict(detection_resolution_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

