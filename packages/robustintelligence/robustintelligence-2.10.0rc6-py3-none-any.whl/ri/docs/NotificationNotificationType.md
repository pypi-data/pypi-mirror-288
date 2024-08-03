# NotificationNotificationType

The type of the notification setting (e.g. Monitoring, Daily Digest, etc.) Each notification setting is triggered on a different cadence and different criteria. For example, daily digests are sent once a day and contain a summary of Stress Tests.   - NOTIFICATION_TYPE_DIGEST: Digest notifications will send a summary of activity for a given project on a given cadence.  - NOTIFICATION_TYPE_JOB_ACTION: Job action will send alerts to users for job events, such as completion or failure. Applies to jobs for stress testing and continuous testing.  - NOTIFICATION_TYPE_MONITORING: When a CT job completes, monitoring notifications trigger when bins contain degradation events. The sensitivity of these alerts is configurable to change alert frequency.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

