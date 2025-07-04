import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	NodeOperationError,
} from 'n8n-workflow';

import {
	KubeConfig,
	CoreV1Api,
	BatchV1Api,
	V1Job,
	V1Pod,
} from '@kubernetes/client-node';

export class KubernetesJobSubmitter implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Kubernetes Job Submitter',
		name: 'kubernetesJobSubmitter',
		group: ['platforms'],
		version: 1,
		description: 'Creates and monitors a Kubernetes Job for running containerized tasks.',
		defaults: {
			name: 'K8s Job Submitter',
			color: '#326ce5',
		},
		inputs: ['main'],
		outputs: ['main'],
		properties: [
			{
				displayName: 'Job Name Prefix',
				name: 'jobNamePrefix',
				type: 'string',
				required: true,
				default: 'creative-gen-',
				description: 'A prefix for the job name. A unique ID will be appended.',
			},
			{
				displayName: 'Namespace',
				name: 'namespace',
				type: 'string',
				default: 'ai-jobs',
				description: 'The Kubernetes namespace to create the job in.',
			},
			{
				displayName: 'Container Image',
				name: 'containerImage',
				type: 'string',
				required: true,
				default: '',
				description: 'The Docker image URL for the AI model container.',
			},
			{
				displayName: 'Command (JSON Array)',
				name: 'command',
				type: 'string',
				typeOptions: {
					rows: 2,
				},
				default: '[]',
				description: 'The command to run in the container, as a JSON array of strings.',
				placeholder: '["python", "main.py"]',
			},
			{
				displayName: 'Arguments (JSON Array)',
				name: 'args',
				type: 'string',
				typeOptions: {
					rows: 2,
				},
				default: '[]',
				description: 'The arguments for the command, as a JSON array of strings.',
				placeholder: '["--input", "/data/input.json"]',
			},
			{
				displayName: 'Input Data (as ENV var)',
				name: 'inputData',
				type: 'json',
				required: true,
				default: '{}',
				description: 'JSON data to be passed to the job as an environment variable named INPUT_JSON.',
			},
			{
				displayName: 'GPU Request',
				name: 'gpuRequest',
				type: 'number',
				default: 1,
				description: 'Number of GPUs to request (e.g., nvidia.com/gpu). Use 0 for no GPU.',
			},
			{
				displayName: 'CPU Request',
				name: 'cpuRequest',
				type: 'string',
				default: '1',
				description: 'CPU resource request (e.g., "500m", "1").',
			},
			{
				displayName: 'Memory Request',
				name: 'memoryRequest',
				type: 'string',
				default: '2Gi',
				description: 'Memory resource request (e.g., "1Gi", "4Gi").',
			},
			{
				displayName: 'Wait for Completion',
				name: 'waitForCompletion',
				type: 'boolean',
				default: true,
				description: 'If enabled, the node will wait for the job to complete or fail. If disabled, it returns immediately after submission.',
			},
			{
				displayName: 'Polling Interval (s)',
				name: 'pollingInterval',
				type: 'number',
				default: 10,
				description: 'How often to check the job status if waiting.',
				displayOptions: {
					show: {
						waitForCompletion: [true],
					},
				},
			},
			{
				displayName: 'Timeout (s)',
				name: 'timeout',
				type: 'number',
				default: 600,
				description: 'Maximum time to wait for job completion before failing.',
				displayOptions: {
					show: {
						waitForCompletion: [true],
					},
				},
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const jobNamePrefix = this.getNodeParameter('jobNamePrefix', 0) as string;
		const namespace = this.getNodeParameter('namespace', 0) as string;
		const containerImage = this.getNodeParameter('containerImage', 0) as string;
		const commandStr = this.getNodeParameter('command', 0) as string;
		const argsStr = this.getNodeParameter('args', 0) as string;
		const inputData = this.getNodeParameter('inputData', 0) as object;
		const gpuRequest = this.getNodeParameter('gpuRequest', 0) as number;
		const cpuRequest = this.getNodeParameter('cpuRequest', 0) as string;
		const memoryRequest = this.getNodeParameter('memoryRequest', 0) as string;
		const waitForCompletion = this.getNodeParameter('waitForCompletion', 0) as boolean;
		const pollingInterval = (this.getNodeParameter('pollingInterval', 0) as number) * 1000;
		const timeout = (this.getNodeParameter('timeout', 0) as number) * 1000;

		const kc = new KubeConfig();
		// loadFromDefault() will check KUBECONFIG env var, then ~/.kube/config
		// For in-cluster, use kc.loadFromCluster()
		try {
			kc.loadFromDefault();
		} catch (e) {
			kc.loadFromCluster();
		}

		const k8sCoreApi = kc.makeApiClient(CoreV1Api);
		const k8sBatchApi = kc.makeApiClient(BatchV1Api);

		const jobName = `${jobNamePrefix}${this.getExecutionId()}`;
		
		let command: string[];
		try {
			command = JSON.parse(commandStr);
			if (!Array.isArray(command)) throw new Error();
		} catch (error) {
			throw new NodeOperationError(this.getNode(), 'Command must be a valid JSON array of strings.');
		}

		let args: string[];
		try {
			args = JSON.parse(argsStr);
			if (!Array.isArray(args)) throw new Error();
		} catch (error) {
			throw new NodeOperationError(this.getNode(), 'Arguments must be a valid JSON array of strings.');
		}

		const jobManifest: V1Job = {
			apiVersion: 'batch/v1',
			kind: 'Job',
			metadata: {
				name: jobName,
				namespace: namespace,
			},
			spec: {
				template: {
					spec: {
						containers: [
							{
								name: `${jobNamePrefix}container`,
								image: containerImage,
								command: command.length > 0 ? command : undefined,
								args: args.length > 0 ? args : undefined,
								env: [
									{
										name: 'INPUT_JSON',
										value: JSON.stringify(inputData),
									},
								],
								resources: {
									requests: {
										cpu: cpuRequest,
										memory: memoryRequest,
									},
									limits: {
										cpu: cpuRequest,
										memory: memoryRequest,
										...(gpuRequest > 0 && { 'nvidia.com/gpu': String(gpuRequest) }),
									},
								},
							},
						],
						restartPolicy: 'OnFailure',
					},
				},
				backoffLimit: 4,
			},
		};

		try {
			const createResponse = await k8sBatchApi.createNamespacedJob(namespace, jobManifest);
			const createdJob = createResponse.body;

			if (!waitForCompletion) {
				const returnData = this.helpers.returnJsonArray([{
					status: 'submitted',
					jobName: createdJob.metadata?.name,
					namespace: createdJob.metadata?.namespace,
				}]);
				return [returnData];
			}
			
			// --- Wait for Completion Logic ---
			const result = await this.waitForJobCompletion(k8sBatchApi, k8sCoreApi, namespace, jobName, pollingInterval, timeout);
			return [this.helpers.returnJsonArray([result])];

		} catch (error: any) {
			if (error.response && error.response.body) {
				throw new NodeOperationError(this.getNode(), `K8s API Error: ${error.response.body.message}`, {
					itemIndex: 0,
				});
			}
			throw new NodeOperationError(this.getNode(), error, { itemIndex: 0 });
		}
	}

	private async waitForJobCompletion(
		k8sBatchApi: BatchV1Api,
		k8sCoreApi: CoreV1Api,
		namespace: string,
		jobName: string,
		interval: number,
		timeout: number
	): Promise<INodeExecutionData['json']> {
		const startTime = Date.now();

		const getPodLogs = async (podName: string): Promise<string> => {
			try {
				const logResponse = await k8sCoreApi.readNamespacedPodLog(podName, namespace);
				return logResponse.body || '';
			} catch (logError) {
				return `Could not retrieve logs for pod ${podName}.`;
			}
		};

		const getPodForJob = async (): Promise<V1Pod | undefined> => {
			const labelSelector = `job-name=${jobName}`;
			const res = await k8sCoreApi.listNamespacedPod(namespace, undefined, undefined, undefined, undefined, labelSelector);
			return res.body.items[0];
		};

		return new Promise((resolve, reject) => {
			const poll = async () => {
				if (Date.now() - startTime > timeout) {
					const pod = await getPodForJob();
					const logs = pod ? await getPodLogs(pod.metadata!.name!) : 'No pod found.';
					reject(new NodeOperationError(this.getNode(), `Job timed out after ${timeout / 1000}s.`, {
						json: {
							status: 'timeout',
							jobName,
							logs,
						}
					}));
					return;
				}

				try {
					const statusResponse = await k8sBatchApi.readNamespacedJobStatus(jobName, namespace);
					const jobStatus = statusResponse.body.status;

					if (jobStatus?.succeeded && jobStatus.succeeded > 0) {
						const pod = await getPodForJob();
						if (!pod || !pod.metadata?.name) {
							resolve({ status: 'succeeded', jobName, logs: 'Could not find associated pod to retrieve logs.' });
							return;
						}
						const logs = await getPodLogs(pod.metadata.name);
						resolve({ status: 'succeeded', jobName, logs });
						return;
					}

					if (jobStatus?.failed && jobStatus.failed > 0) {
						const pod = await getPodForJob();
						const logs = pod ? await getPodLogs(pod.metadata!.name!) : 'No pod found for failed job.';
						reject(new NodeOperationError(this.getNode(), `Job failed.`, {
							json: {
								status: 'failed',
								jobName,
								reason: jobStatus.conditions?.[0]?.message,
								logs,
							}
						}));
						return;
					}

					setTimeout(poll, interval);
				} catch (error: any) {
					reject(new NodeOperationError(this.getNode(), `Error polling job status: ${error.message}`, {
						json: { error: error.response?.body ?? error }
					}));
				}
			};
			poll();
		});
	}
}