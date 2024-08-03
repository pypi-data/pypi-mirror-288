# LanguageDetectionDetailsLanguageSubstring


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**language_code** | **str** | Language code is the language code of the detected language according to the ISO 639-3 standard. | [optional] 
**flagged_substring** | [**GenerativefirewallFlaggedSubstring**](GenerativefirewallFlaggedSubstring.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.language_detection_details_language_substring import LanguageDetectionDetailsLanguageSubstring

# TODO update the JSON string below
json = "{}"
# create an instance of LanguageDetectionDetailsLanguageSubstring from a JSON string
language_detection_details_language_substring_instance = LanguageDetectionDetailsLanguageSubstring.from_json(json)
# print the JSON string representation of the object
print(LanguageDetectionDetailsLanguageSubstring.to_json())

# convert the object into a dict
language_detection_details_language_substring_dict = language_detection_details_language_substring_instance.to_dict()
# create an instance of LanguageDetectionDetailsLanguageSubstring from a dict
language_detection_details_language_substring_from_dict = LanguageDetectionDetailsLanguageSubstring.from_dict(language_detection_details_language_substring_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

