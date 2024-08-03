# RimeSeverity

Severity specifies the severity level of an event. Depending on the direction of degradation, a metric going below or above a threshold will trigger a higher severity level.   - SEVERITY_UNSPECIFIED: Indicates that no test runs for the specified metric.  - SEVERITY_PASS: Indicates that the specified metric is lower than the low threshold in the case where the Monitor is configured to trigger on an increase of a metric.  - SEVERITY_WARNING: Indicates that the specified metric is higher than the low threshold but still lower than the high threshold, in the case that a Monitor is configured to trigger on an increase of a metric. Warning and Alert severity levels will trigger a Degradation event.  - SEVERITY_ALERT: Indicates that the specified metric is higher than the high threshold in the case that the Monitor is configured to trigger on an increase of a metric. Warning and Alert severity level will trigger a Degradation event.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

