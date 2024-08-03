# ValidateResponseProductMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**vendor_name** | **str** |  | [optional] 
**product** | **str** |  | [optional] 
**firewall_instance_id** | **str** | ID of the firewall instance the request is sent to. | [optional] 
**version** | **str** | Firewall semantic version. | [optional] 

## Example

```python
from ri.fwclient.models.validate_response_product_metadata import ValidateResponseProductMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of ValidateResponseProductMetadata from a JSON string
validate_response_product_metadata_instance = ValidateResponseProductMetadata.from_json(json)
# print the JSON string representation of the object
print(ValidateResponseProductMetadata.to_json())

# convert the object into a dict
validate_response_product_metadata_dict = validate_response_product_metadata_instance.to_dict()
# create an instance of ValidateResponseProductMetadata from a dict
validate_response_product_metadata_from_dict = ValidateResponseProductMetadata.from_dict(validate_response_product_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

