# GenerativefirewallCodeDetectionDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**flagged_code_substrings** | [**List[CodeDetectionDetailsCodeSubstring]**](CodeDetectionDetailsCodeSubstring.md) | Flagged code substrings are the substrings that were detected as a code snippet. | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_code_detection_details import GenerativefirewallCodeDetectionDetails

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallCodeDetectionDetails from a JSON string
generativefirewall_code_detection_details_instance = GenerativefirewallCodeDetectionDetails.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallCodeDetectionDetails.to_json())

# convert the object into a dict
generativefirewall_code_detection_details_dict = generativefirewall_code_detection_details_instance.to_dict()
# create an instance of GenerativefirewallCodeDetectionDetails from a dict
generativefirewall_code_detection_details_from_dict = GenerativefirewallCodeDetectionDetails.from_dict(generativefirewall_code_detection_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

