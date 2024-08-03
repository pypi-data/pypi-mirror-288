# GenerativefirewallToxicityDetectionDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | [**RimeToxicityThreatCategory**](RimeToxicityThreatCategory.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_toxicity_detection_details import GenerativefirewallToxicityDetectionDetails

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallToxicityDetectionDetails from a JSON string
generativefirewall_toxicity_detection_details_instance = GenerativefirewallToxicityDetectionDetails.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallToxicityDetectionDetails.to_json())

# convert the object into a dict
generativefirewall_toxicity_detection_details_dict = generativefirewall_toxicity_detection_details_instance.to_dict()
# create an instance of GenerativefirewallToxicityDetectionDetails from a dict
generativefirewall_toxicity_detection_details_from_dict = GenerativefirewallToxicityDetectionDetails.from_dict(generativefirewall_toxicity_detection_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

