# RimeSafeURL

SafeURL represents a URL that has been safely constructed. e.g. a user clicking on this link is guaranteed to land on the RIME web app. We use this instead of a raw str so that application code can generate SafeURL messages in certain ways -> this provides stronger typing than just using a string.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | A safely constructed URL. | [optional] 

## Example

```python
from ri.apiclient.models.rime_safe_url import RimeSafeURL

# TODO update the JSON string below
json = "{}"
# create an instance of RimeSafeURL from a JSON string
rime_safe_url_instance = RimeSafeURL.from_json(json)
# print the JSON string representation of the object
print(RimeSafeURL.to_json())

# convert the object into a dict
rime_safe_url_dict = rime_safe_url_instance.to_dict()
# create an instance of RimeSafeURL from a dict
rime_safe_url_from_dict = RimeSafeURL.from_dict(rime_safe_url_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

