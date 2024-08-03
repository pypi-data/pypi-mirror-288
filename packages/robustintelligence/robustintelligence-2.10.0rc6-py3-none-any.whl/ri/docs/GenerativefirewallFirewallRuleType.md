# GenerativefirewallFirewallRuleType

FirewallRuleType specifies the different rules for the firewall.   - FIREWALL_RULE_TYPE_TOXICITY: Toxicity checks for toxic text in the model's output.  - FIREWALL_RULE_TYPE_PII_DETECTION: PII detection validates that the model does not leak personal information.  - FIREWALL_RULE_TYPE_PROMPT_INJECTION: Prompt injection flags user input text that contain prompt injection attacks.  - FIREWALL_RULE_TYPE_FACTUAL_INCONSISTENCY: Factual inconsistency verifies the model output does not contradict the input context documents. In a RAG application the context will be the documents loaded during the RAG Retrieval phase to augment the LLM's response.  - FIREWALL_RULE_TYPE_OFF_TOPIC: Off topic flags user inputs that are out of distribution.  - FIREWALL_RULE_TYPE_INDIRECT_PROMPT_INJECTION: Indirect prompt injection flags contexts that contain prompt injection attacks.  - FIREWALL_RULE_TYPE_UNKNOWN_EXTERNAL_SOURCE: Unknown external source flags inputs that contain potentially malicious resources, such as urls that are not configured to be whitelisted.  - FIREWALL_RULE_TYPE_LANGUAGE_DETECTION: Language detection flags inputs that contain any language other than those that are whitelisted.  - FIREWALL_RULE_TYPE_CODE_DETECTION: Code detection flags inputs that contain code snippets.  - FIREWALL_RULE_TYPE_TOKEN_COUNTER: Token counter flags model inputs/outputs that attempt to overload the model. This rule ensures large inputs are blocked if they exceed a configurable number of tokens.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

