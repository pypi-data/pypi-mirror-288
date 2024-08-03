# RimeImageReference

A reference to another image, managed or not.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the image being referenced. For a managed image, this is the &#x60;name&#x60; record of the &#x60;ManagedImage&#x60; object. For an external image, this is the full name of that image. | [optional] 
**reference_type** | [**ImageReferenceReferenceType**](ImageReferenceReferenceType.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_image_reference import RimeImageReference

# TODO update the JSON string below
json = "{}"
# create an instance of RimeImageReference from a JSON string
rime_image_reference_instance = RimeImageReference.from_json(json)
# print the JSON string representation of the object
print(RimeImageReference.to_json())

# convert the object into a dict
rime_image_reference_dict = rime_image_reference_instance.to_dict()
# create an instance of RimeImageReference from a dict
rime_image_reference_from_dict = RimeImageReference.from_dict(rime_image_reference_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

