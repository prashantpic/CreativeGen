import { INodeTypeDescription } from 'n8n-workflow';

export const creativeFlowModelSelectorDescription: INodeTypeDescription = {
	displayName: 'CreativeFlow AI Model Selector',
	name: 'creativeFlowModelSelector',
	group: ['CreativeFlow AI'],
	version: 1,
	description: 'Selects an AI model and provider based on task type, user context, and business rules.',
	defaults: {
		name: 'AI Model Selector',
	},
	inputs: ['main'],
	outputs: ['main'],
	properties: [
		{
			displayName: 'Task Type',
			name: 'taskType',
			type: 'string',
			default: 'image_generation_from_text',
			required: true,
			description: "The type of task to perform, e.g., 'image_generation_from_text'.",
		},
		{
			displayName: 'User Tier',
			name: 'userTier',
			type: 'string',
			default: 'Free',
			required: true,
			description: "The user's subscription tier, e.g., 'Free', 'Pro', 'Enterprise'.",
		},
		{
			displayName: 'User ID',
			name: 'userId',
			type: 'string',
			default: '',
			description: 'The unique ID of the user, used for A/B testing user-stickiness.',
		},
		{
			displayName: 'Additional Parameters',
			name: 'additionalParameters',
			type: 'json',
			default: '{}',
			description: 'Any other parameters that might influence model selection, e.g., `desired_quality`, `cost_sensitivity`.',
		},
		{
			displayName: 'Rules Config Source',
			name: 'rulesConfigSource',
			type: 'string',
			default: '',
			description: 'Optional path to a JSON/YAML rules file or an API endpoint. If empty, uses internal logic.',
		},
		{
			displayName: 'A/B Test Config ID',
			name: 'abTestConfigId',
			type: 'string',
			default: '',
			description: 'Optional identifier for an active A/B test configuration.',
		},
	],
};