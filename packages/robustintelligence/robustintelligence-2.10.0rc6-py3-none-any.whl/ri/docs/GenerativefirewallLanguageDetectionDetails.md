# GenerativefirewallLanguageDetectionDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**flagged_language_substrings** | [**List[LanguageDetectionDetailsLanguageSubstring]**](LanguageDetectionDetailsLanguageSubstring.md) | Flagged language substrings are the substrings that were detected as a language outside of the whitelist. | [optional] 

## Example

```python
from ri.fwclient.models.generativefirewall_language_detection_details import GenerativefirewallLanguageDetectionDetails

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativefirewallLanguageDetectionDetails from a JSON string
generativefirewall_language_detection_details_instance = GenerativefirewallLanguageDetectionDetails.from_json(json)
# print the JSON string representation of the object
print(GenerativefirewallLanguageDetectionDetails.to_json())

# convert the object into a dict
generativefirewall_language_detection_details_dict = generativefirewall_language_detection_details_instance.to_dict()
# create an instance of GenerativefirewallLanguageDetectionDetails from a dict
generativefirewall_language_detection_details_from_dict = GenerativefirewallLanguageDetectionDetails.from_dict(generativefirewall_language_detection_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

