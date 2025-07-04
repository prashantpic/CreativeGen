import { INodeTypeDescription } from 'n8n-workflow';

export const k8sJobOrchestratorDescription: INodeTypeDescription = {
	displayName: 'Kubernetes AI Job Orchestrator',
	name: 'k8sJobOrchestrator',
	group: ['CreativeFlow AI'],
	version: 1,
	description: 'Submits and monitors AI inference jobs on a Kubernetes cluster.',
	defaults: {
		name: 'K8s AI Job Orchestrator',
		namespace: 'ai-jobs',
		options: {
			waitForCompletion: true,
			pollingIntervalSeconds: 10,
			timeoutSeconds: 300,
			retrieveLogs: true,
		},
	},
	inputs: ['main'],
	outputs: ['main', 'error'],
	outputNames: ['Success', 'Failure'],
	properties: [
		{
			displayName: 'Kubeconfig Path',
			name: 'kubeConfig',
			type: 'string',
			default: '',
			description: 'Path to kubeconfig file. If empty, uses in-cluster config or default local config.',
		},
		{
			displayName: 'Namespace',
			name: 'namespace',
			type: 'string',
			required: true,
			default: 'ai-jobs',
			description: 'The Kubernetes namespace to create the job in.',
		},
		{
			displayName: 'Job Manifest',
			name: 'jobManifest',
			type: 'json',
			required: true,
			default: '{}',
			typeOptions: {
				rows: 15,
			},
			description: 'The Kubernetes Job manifest template (JSON). Use n8n expressions for dynamic values.',
		},
		{
			displayName: 'Options',
			name: 'options',
			type: 'collection',
			placeholder: 'Add Option',
			default: {},
			options: [
				{
					displayName: 'Wait for Completion',
					name: 'waitForCompletion',
					type: 'boolean',
					default: true,
					description: 'Whether the node should wait for the job to complete before finishing.',
				},
				{
					displayName: 'Polling Interval (s)',
					name: 'pollingIntervalSeconds',
					type: 'number',
					typeOptions: { minValue: 1 },
					default: 10,
					description: 'If waiting for completion, how often to poll the job status.',
					displayOptions: {
						show: {
							waitForCompletion: [true],
						},
					},
				},
				{
					displayName: 'Timeout (s)',
					name: 'timeoutSeconds',
					type: 'number',
					typeOptions: { minValue: 1 },
					default: 300,
					description: 'Maximum time to wait for the job to complete.',
					displayOptions: {
						show: {
							waitForCompletion: [true],
						},
					},
				},
				{
					displayName: 'Retrieve Logs',
					name: 'retrieveLogs',
					type: 'boolean',
					default: true,
					description: 'Whether to retrieve logs from the completed or failed pod.',
					displayOptions: {
						show: {
							waitForCompletion: [true],
						},
					},
				},
			],
		},
	],
};