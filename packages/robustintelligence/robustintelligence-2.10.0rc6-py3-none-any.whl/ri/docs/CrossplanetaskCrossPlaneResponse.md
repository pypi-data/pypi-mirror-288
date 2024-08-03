# CrossplanetaskCrossPlaneResponse

CrossPlaneResponse encompasses the set of responses from cross-plane services.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category_config_generation_service_response** | [**ConfigGenerationCategoryConfigGenerationServiceResponse**](ConfigGenerationCategoryConfigGenerationServiceResponse.md) |  | [optional] 
**profiling_config_generation_service_response** | [**ConfigGenerationProfilingConfigGenerationServiceResponse**](ConfigGenerationProfilingConfigGenerationServiceResponse.md) |  | [optional] 
**test_suite_config_generation_service_response** | [**ConfigGenerationTestSuiteConfigGenerationServiceResponse**](ConfigGenerationTestSuiteConfigGenerationServiceResponse.md) |  | [optional] 
**check_object_exists_response** | [**FileserverCheckObjectExistsResponse**](FileserverCheckObjectExistsResponse.md) |  | [optional] 
**delete_object_response** | **object** |  | [optional] 
**get_read_object_presigned_link_response** | [**FileserverGetReadObjectPresignedLinkResponse**](FileserverGetReadObjectPresignedLinkResponse.md) |  | [optional] 
**get_upload_object_presigned_link_response** | [**FileserverGetUploadObjectPresignedLinkResponse**](FileserverGetUploadObjectPresignedLinkResponse.md) |  | [optional] 
**list_objects_response** | [**FileserverListObjectsResponse**](FileserverListObjectsResponse.md) |  | [optional] 
**validate_dataset_response** | [**ValidationValidateDatasetResponse**](ValidationValidateDatasetResponse.md) |  | [optional] 
**validate_model_response** | [**ValidationValidateModelResponse**](ValidationValidateModelResponse.md) |  | [optional] 
**validate_predictions_response** | [**ValidationValidatePredictionsResponse**](ValidationValidatePredictionsResponse.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.crossplanetask_cross_plane_response import CrossplanetaskCrossPlaneResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CrossplanetaskCrossPlaneResponse from a JSON string
crossplanetask_cross_plane_response_instance = CrossplanetaskCrossPlaneResponse.from_json(json)
# print the JSON string representation of the object
print(CrossplanetaskCrossPlaneResponse.to_json())

# convert the object into a dict
crossplanetask_cross_plane_response_dict = crossplanetask_cross_plane_response_instance.to_dict()
# create an instance of CrossplanetaskCrossPlaneResponse from a dict
crossplanetask_cross_plane_response_from_dict = CrossplanetaskCrossPlaneResponse.from_dict(crossplanetask_cross_plane_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

