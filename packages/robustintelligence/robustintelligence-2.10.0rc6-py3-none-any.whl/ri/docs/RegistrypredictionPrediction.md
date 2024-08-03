# RegistrypredictionPrediction

Prediction represents a full entry in the Predictions Registry, with info, metadata, and tags used to identify the predictions both internally and to an external user.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_id** | **str** | The dataset_id and model_id are used to uniquely identify a prediction. These must be provided by the user. | [optional] 
**model_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**project_ids** | [**List[RimeUUID]**](RimeUUID.md) | For now, a pred will only have one project_id associated with it. We make this an array to allow pred&#39;s to be shared in the future. | [optional] 
**creator_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**creation_time** | **datetime** |  | [optional] 
**user_metadata** | [**RegistryMetadata**](RegistryMetadata.md) |  | [optional] 
**integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**pred_info** | [**RegistryPredInfo**](RegistryPredInfo.md) |  | [optional] 
**validity_status** | [**RegistryValidityStatus**](RegistryValidityStatus.md) |  | [optional] 
**marked_for_delete_at** | **datetime** | If marked_for_delete_at is set, the document will be deleted after a TTL. | [optional] 
**validity_status_message** | **str** | Information about the validity status of the predictions, such as why it is invalid. A Case where this would be populated is when the ValidityStatus is not explicitly set to valid by the XP validation task and additional details are required to convey to the user why the predictions are not valid. | [optional] 

## Example

```python
from ri.apiclient.models.registryprediction_prediction import RegistrypredictionPrediction

# TODO update the JSON string below
json = "{}"
# create an instance of RegistrypredictionPrediction from a JSON string
registryprediction_prediction_instance = RegistrypredictionPrediction.from_json(json)
# print the JSON string representation of the object
print(RegistrypredictionPrediction.to_json())

# convert the object into a dict
registryprediction_prediction_dict = registryprediction_prediction_instance.to_dict()
# create an instance of RegistrypredictionPrediction from a dict
registryprediction_prediction_from_dict = RegistrypredictionPrediction.from_dict(registryprediction_prediction_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

