# CodeDetectionDetailsCodeSubstring


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**language** | **str** | Language is the programmatic language name of the detected code snippet. | [optional] 
**flagged_substring** | [**GenerativefirewallFlaggedSubstring**](GenerativefirewallFlaggedSubstring.md) |  | [optional] 

## Example

```python
from ri.fwclient.models.code_detection_details_code_substring import CodeDetectionDetailsCodeSubstring

# TODO update the JSON string below
json = "{}"
# create an instance of CodeDetectionDetailsCodeSubstring from a JSON string
code_detection_details_code_substring_instance = CodeDetectionDetailsCodeSubstring.from_json(json)
# print the JSON string representation of the object
print(CodeDetectionDetailsCodeSubstring.to_json())

# convert the object into a dict
code_detection_details_code_substring_dict = code_detection_details_code_substring_instance.to_dict()
# create an instance of CodeDetectionDetailsCodeSubstring from a dict
code_detection_details_code_substring_from_dict = CodeDetectionDetailsCodeSubstring.from_dict(code_detection_details_code_substring_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

