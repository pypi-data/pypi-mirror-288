# ValidationValidateDatasetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_valid** | **bool** |  | [optional] 
**error_message** | **str** |  | [optional] 
**validation_status** | [**RegistryValidityStatus**](RegistryValidityStatus.md) |  | [optional] 
**size_bytes** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.validation_validate_dataset_response import ValidationValidateDatasetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ValidationValidateDatasetResponse from a JSON string
validation_validate_dataset_response_instance = ValidationValidateDatasetResponse.from_json(json)
# print the JSON string representation of the object
print(ValidationValidateDatasetResponse.to_json())

# convert the object into a dict
validation_validate_dataset_response_dict = validation_validate_dataset_response_instance.to_dict()
# create an instance of ValidationValidateDatasetResponse from a dict
validation_validate_dataset_response_from_dict = ValidationValidateDatasetResponse.from_dict(validation_validate_dataset_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

