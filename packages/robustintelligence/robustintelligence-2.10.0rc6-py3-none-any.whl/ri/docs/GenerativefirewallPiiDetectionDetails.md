# GenerativefirewallPiiDetectionDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**flagged_entities** | [**List[PiiDetectionDetailsFlaggedEntity]**](PiiDetectionDetailsFlaggedEntity.md) | Flagged entities are the entities that were detected in the text(s). | [optional] 
**sanitized_text** | **str** | Sanitized text is the original text with the flagged entities redacted. | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_pii_detection_details import GenerativefirewallPiiDetectionDetails

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallPiiDetectionDetails from a JSON string
generativefirewall_pii_detection_details_instance = GenerativefirewallPiiDetectionDetails.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallPiiDetectionDetails.to_json())

# convert the object into a dict
generativefirewall_pii_detection_details_dict = generativefirewall_pii_detection_details_instance.to_dict()
# create an instance of GenerativefirewallPiiDetectionDetails from a dict
generativefirewall_pii_detection_details_from_dict = GenerativefirewallPiiDetectionDetails.from_dict(generativefirewall_pii_detection_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

