# PiiDetectionDetailsFlaggedEntity


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**entity_type** | [**GenerativefirewallPiiEntityType**](GenerativefirewallPiiEntityType.md) |  | [optional] 
**custom_entity_name** | **str** | Custom entity name is the name of the custom-defined entity that was detected for this substring, if applicable. | [optional] 
**flagged_substring** | [**GenerativefirewallFlaggedSubstring**](GenerativefirewallFlaggedSubstring.md) |  | [optional] 
**confidence_score** | **float** | Confidence score is a metric of how confident (on a scale of 0-1) the rule is about this entity being flagged. | [optional] 

## Example

```python
from ri.fwclient.models.pii_detection_details_flagged_entity import PiiDetectionDetailsFlaggedEntity

# TODO update the JSON string below
json = "{}"
# create an instance of PiiDetectionDetailsFlaggedEntity from a JSON string
pii_detection_details_flagged_entity_instance = PiiDetectionDetailsFlaggedEntity.from_json(json)
# print the JSON string representation of the object
print(PiiDetectionDetailsFlaggedEntity.to_json())

# convert the object into a dict
pii_detection_details_flagged_entity_dict = pii_detection_details_flagged_entity_instance.to_dict()
# create an instance of PiiDetectionDetailsFlaggedEntity from a dict
pii_detection_details_flagged_entity_from_dict = PiiDetectionDetailsFlaggedEntity.from_dict(pii_detection_details_flagged_entity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

