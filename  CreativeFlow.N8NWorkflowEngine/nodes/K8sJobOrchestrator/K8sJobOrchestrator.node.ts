import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	NodeOperationError,
} from 'n8n-workflow';
import { k8sJobOrchestratorDescription as description } from './description';
import {
	KubeConfig,
	BatchV1Api,
	CoreV1Api,
	V1Job,
	V1Pod,
} from '@kubernetes/client-node';

export class K8sJobOrchestrator implements INodeType {
	description = description;

	private getKubeConfig(kubeConfigPath?: string): KubeConfig {
		const kc = new KubeConfig();
		if (kubeConfigPath) {
			kc.loadFromFile(kubeConfigPath);
		} else {
			try {
				// Try in-cluster config first
				kc.loadFromCluster();
			} catch {
				// Fallback to default local config
				kc.loadFromDefault();
			}
		}
		return kc;
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const successData: INodeExecutionData[] = [];
		const errorData: INodeExecutionData[] = [];

		for (let i = 0; i < items.length; i++) {
			try {
				const kubeConfigPath = this.getNodeParameter('kubeConfig', i, '') as string;
				const namespace = this.getNodeParameter('namespace', i, 'default') as string;
				const jobManifestStr = this.getNodeParameter('jobManifest', i, '{}') as string;
				const options = this.getNodeParameter('options', i, {}) as any;

				const kc = this.getKubeConfig(kubeConfigPath);
				const batchV1Api = kc.makeApiClient(BatchV1Api);
				const coreV1Api = kc.makeApiClient(CoreV1Api);

				// Prepare and create the job
				const jobManifest = JSON.parse(jobManifestStr) as V1Job;
				if (!jobManifest.metadata?.name) {
					throw new NodeOperationError(this.getNode(), 'Job manifest must include metadata.name');
				}
				const jobName = jobManifest.metadata.name;

				await batchV1Api.createNamespacedJob(namespace, jobManifest);

				if (!options.waitForCompletion) {
					successData.push({ json: { jobStatus: 'submitted', jobName }, pairedItem: i });
					continue;
				}

				// Wait for job completion
				const jobResult = await new Promise<any>((resolve, reject) => {
					const timeout = setTimeout(() => {
						clearInterval(interval);
						reject(new Error(`Timeout: Job '${jobName}' did not complete within ${options.timeoutSeconds} seconds.`));
					}, options.timeoutSeconds * 1000);

					const interval = setInterval(async () => {
						try {
							const { body: jobStatus } = await batchV1Api.readNamespacedJobStatus(jobName, namespace);
							if (jobStatus.status?.succeeded) {
								clearInterval(interval);
								clearTimeout(timeout);
								resolve({ jobStatus: 'succeeded', job: jobStatus });
							} else if (jobStatus.status?.failed) {
								clearInterval(interval);
								clearTimeout(timeout);
								resolve({ jobStatus: 'failed', job: jobStatus, errorMessage: jobStatus.status.conditions?.[0]?.message ?? 'Job failed' });
							}
						} catch (error) {
							clearInterval(interval);
							clearTimeout(timeout);
							reject(error);
						}
					}, options.pollingIntervalSeconds * 1000);
				});

				// Retrieve logs if requested
				let logs: string | undefined;
				if (options.retrieveLogs && jobResult.jobStatus !== 'submitted') {
					const { body: podList } = await coreV1Api.listNamespacedPod(namespace, undefined, undefined, undefined, undefined, `job-name=${jobName}`);
					if (podList.items.length > 0) {
						const podName = podList.items[0].metadata?.name!;
						try {
							const { body: podLogs } = await coreV1Api.readNamespacedPodLog(podName, namespace);
							logs = podLogs;
						} catch (logError) {
							logs = `Could not retrieve logs: ${logError.message}`;
						}
					}
				}
				
				const finalResult = {
					jobStatus: jobResult.jobStatus,
					jobName,
					resultData: {
						logs,
						// In a real scenario, this would be populated with paths to outputs from a PVC or object store
					},
					errorMessage: jobResult.errorMessage,
				};

				if (jobResult.jobStatus === 'succeeded') {
					successData.push({ json: finalResult, pairedItem: i });
				} else {
					errorData.push({ json: finalResult, pairedItem: i });
				}

			} catch (error) {
				if (this.continueOnFail()) {
					errorData.push({ json: { error: error.message }, pairedItem: i });
					continue;
				}
				throw new NodeOperationError(this.getNode(), error, { itemIndex: i });
			}
		}

		return [successData, errorData];
	}
}