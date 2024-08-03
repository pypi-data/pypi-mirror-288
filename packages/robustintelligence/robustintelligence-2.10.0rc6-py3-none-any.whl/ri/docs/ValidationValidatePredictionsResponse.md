# ValidationValidatePredictionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_valid** | **bool** |  | [optional] 
**error_message** | **str** |  | [optional] 
**validation_status** | [**RegistryValidityStatus**](RegistryValidityStatus.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.validation_validate_predictions_response import ValidationValidatePredictionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ValidationValidatePredictionsResponse from a JSON string
validation_validate_predictions_response_instance = ValidationValidatePredictionsResponse.from_json(json)
# print the JSON string representation of the object
print(ValidationValidatePredictionsResponse.to_json())

# convert the object into a dict
validation_validate_predictions_response_dict = validation_validate_predictions_response_instance.to_dict()
# create an instance of ValidationValidatePredictionsResponse from a dict
validation_validate_predictions_response_from_dict = ValidationValidatePredictionsResponse.from_dict(validation_validate_predictions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

