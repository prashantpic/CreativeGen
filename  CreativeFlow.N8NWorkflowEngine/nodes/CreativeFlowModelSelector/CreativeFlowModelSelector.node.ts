import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	NodeOperationError,
} from 'n8n-workflow';
import { creativeFlowModelSelectorDescription as description } from './description';
import crypto from 'crypto';

export class CreativeFlowModelSelector implements INodeType {
	description = description;

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];

		for (let i = 0; i < items.length; i++) {
			try {
				const taskType = this.getNodeParameter('taskType', i, '') as string;
				const userTier = this.getNodeParameter('userTier', i, 'Free') as string;
				const userId = this.getNodeParameter('userId', i, '') as string;
				const abTestConfigId = this.getNodeParameter('abTestConfigId', i, '') as string;
				// const rulesConfigSource = this.getNodeParameter('rulesConfigSource', i, '') as string;
				// const additionalParameters = this.getNodeParameter('additionalParameters', i, {}) as object;

				let selectedProvider: string;
				let selectedModelId: string;
				let providerSpecificParams: object = {};

				const enableAbTesting = process.env.ENABLE_AB_TESTING_MODEL_SELECTOR === 'true';

				// 1. A/B Testing Logic
				if (enableAbTesting && abTestConfigId && userId) {
					// In a real scenario, this would fetch config from a service.
					// Mock config for a test named 'text-to-image-v2-test'
					if (abTestConfigId === 'text-to-image-v2-test') {
						const hash = crypto.createHash('sha256').update(userId).digest('hex');
						const groupNumber = parseInt(hash.substring(0, 2), 16);

						if (groupNumber % 2 === 0) { // Group A (50%)
							selectedProvider = 'OpenAI';
							selectedModelId = 'dall-e-3';
							providerSpecificParams = { quality: 'hd' };
						} else { // Group B (50%)
							selectedProvider = 'StabilityAI';
							selectedModelId = 'stable-diffusion-xl-1024-v1-0';
							providerSpecificParams = { steps: 40 };
						}
					}
				}

				// 2. Rule-Based Selection (if not in A/B test)
				if (!selectedProvider) {
					// In a real scenario, this would be a more complex rules engine,
					// possibly loaded from `rulesConfigSource`.
					if (taskType === 'image_generation_from_text') {
						switch (userTier.toLowerCase()) {
							case 'enterprise':
							case 'pro':
								selectedProvider = 'OpenAI';
								selectedModelId = 'dall-e-3';
								providerSpecificParams = { quality: 'standard' };
								break;
							case 'free':
							default:
								selectedProvider = 'StabilityAI';
								selectedModelId = 'stable-diffusion-v1-6';
								providerSpecificParams = { steps: 25 };
								break;
						}
					}
				}

				// 3. Default Fallback
				if (!selectedProvider) {
					selectedProvider = 'StabilityAI';
					selectedModelId = 'stable-diffusion-v1-6';
				}

				returnData.push({
					json: {
						...items[i].json,
						selectedProvider,
						selectedModelId,
						providerSpecificParams,
					},
				});

			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({ json: { error: error.message }, pairedItem: i });
					continue;
				}
				throw error;
			}
		}

		return [returnData];
	}
}