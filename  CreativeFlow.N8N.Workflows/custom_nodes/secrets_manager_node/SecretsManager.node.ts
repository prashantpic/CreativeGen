import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	NodeApiError,
	INodeProperties,
} from 'n8n-workflow';
import vaultClient from 'node-vault';

export class CreativeFlowSecretsManager implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'CreativeFlow: Secrets Manager',
		name: 'creativeFlowSecretsManager',
		group: ['CreativeFlow'],
		version: 1,
		description: 'Fetches secrets from HashiCorp Vault',
		defaults: {
			name: 'Vault Secret',
		},
		inputs: ['main'],
		outputs: ['main'],
		credentials: [
			{
				name: 'vaultApi',
				required: true,
			},
		],
		properties: [
			{
				displayName: 'Secret Path',
				name: 'secretPath',
				type: 'string',
				default: '',
				required: true,
				description: 'The full path to the secret in Vault (e.g., kv/data/creativeflow/ai_services/openai)',
			},
			{
				displayName: 'Secret Key (Optional)',
				name: 'secretKey',
				type: 'string',
				default: '',
				description: 'The specific key within the secret to retrieve. If empty, returns the entire data object.',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];

		for (let itemIndex = 0; itemIndex < items.length; itemIndex++) {
			try {
				const secretPath = this.getNodeParameter('secretPath', itemIndex, '') as string;
				const secretKey = this.getNodeParameter('secretKey', itemIndex, '') as string;
				const credentials = await this.getCredentials('vaultApi');

				if (!credentials.vaultAddress || !credentials.vaultToken) {
					throw new NodeApiError(this.getNode(), {}, { message: 'Vault credentials are not configured correctly.' });
				}

				const options = {
					apiVersion: 'v1',
					endpoint: credentials.vaultAddress as string,
					token: credentials.vaultToken as string,
				};

				const vault = vaultClient(options);
				const response = await vault.read(secretPath);

				if (!response || !response.data || !response.data.data) {
					throw new NodeApiError(this.getNode(), response, { message: 'Secret not found or empty at specified path.' });
				}

				let secretValue: any = response.data.data;

				if (secretKey) {
					if (secretValue.hasOwnProperty(secretKey)) {
						secretValue = secretValue[secretKey];
					} else {
						throw new NodeApiError(this.getNode(), response, { message: `Key "${secretKey}" not found in secret.` });
					}
				}

				returnData.push({
					json: {
						...items[itemIndex].json,
						secretValue: secretValue,
					},
					pairedItem: {
						item: itemIndex,
					},
				});
			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({
						json: {
							...items[itemIndex].json,
							error: error.message,
						},
						pairedItem: {
							item: itemIndex,
						},
					});
					continue;
				}
				throw error;
			}
		}

		return [returnData];
	}
}