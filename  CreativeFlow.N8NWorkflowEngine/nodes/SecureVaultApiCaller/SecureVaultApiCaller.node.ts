import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	NodeOperationError,
} from 'n8n-workflow';
import { secureVaultApiCallerDescription as description } from './description';
import vault from 'node-vault';
import axios, { AxiosRequestConfig, Method } from 'axios';

export class SecureVaultApiCaller implements INodeType {
	description = description;

	private async getVaultClient(this: IExecuteFunctions): Promise<vault.client> {
		const vaultAddress = process.env.VAULT_ADDR;
		if (!vaultAddress) {
			throw new NodeOperationError(this.getNode(), 'VAULT_ADDR environment variable is not set.');
		}

		const options: vault.VaultOptions = {
			apiVersion: 'v1',
			endpoint: vaultAddress,
		};

		const vaultClient = vault(options);

		const roleId = process.env.VAULT_APPROLE_ID;
		const secretId = process.env.VAULT_APPROLE_SECRET_ID;

		if (roleId && secretId) {
			const result = await vaultClient.approleLogin({
				role_id: roleId,
				secret_id: secretId,
			});
			vaultClient.token = result.auth.client_token;
		} else if (process.env.VAULT_TOKEN) {
			vaultClient.token = process.env.VAULT_TOKEN;
		} else {
			throw new NodeOperationError(this.getNode(), 'Vault authentication not configured. Set VAULT_APPROLE_ID and VAULT_APPROLE_SECRET_ID, or VAULT_TOKEN.');
		}
		return vaultClient;
	}

	private async delay(ms: number): Promise<void> {
		return new Promise(resolve => setTimeout(resolve, ms));
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const successData: INodeExecutionData[] = [];
		const fallbackData: INodeExecutionData[] = [];

		const makeApiCall = async (
			apiUrl: string,
			httpMethod: string,
			headers: object,
			body: object,
			vaultClient: vault.client,
			vaultPath: string,
			vaultKey: string,
			apiKeyHeader: string,
			apiKeyPrefix: string,
		): Promise<any> => {
			if (!vaultPath) {
				throw new NodeOperationError(this.getNode(), 'Vault path is not defined for this call.');
			}
			const secret = await vaultClient.read(vaultPath);
			const apiKey = secret.data.data[vaultKey];
			if (!apiKey) {
				throw new NodeOperationError(this.getNode(), `Key '${vaultKey}' not found in Vault secret at '${vaultPath}'.`);
			}

			const requestHeaders = {
				...headers,
				[apiKeyHeader]: `${apiKeyPrefix}${apiKey}`,
			};

			const config: AxiosRequestConfig = {
				method: httpMethod as Method,
				url: apiUrl,
				headers: requestHeaders,
				data: body,
				timeout: 30000, // 30 second timeout
			};

			const response = await axios(config);
			return response.data;
		};

		for (let i = 0; i < items.length; i++) {
			let lastError: Error | undefined;

			try {
				const vaultClient = await this.getVaultClient();

				const apiUrl = this.getNodeParameter('apiUrl', i, '') as string;
				const httpMethod = this.getNodeParameter('httpMethod', i, 'POST') as string;
				const body = this.getNodeParameter('body', i, {}) as object;
				const headers = this.getNodeParameter('headers', i, {}) as object;
				const vaultSecretPath = this.getNodeParameter('vaultSecretPath', i, '') as string;
				const vaultSecretKey = this.getNodeParameter('vaultSecretKey', i, 'api_key') as string;
				const apiKeyHeaderName = this.getNodeParameter('apiKeyHeaderName', i, 'Authorization') as string;
				const apiKeyPrefix = this.getNodeParameter('apiKeyPrefix', i, 'Bearer ') as string;
				const options = this.getNodeParameter('options', i, {}) as any;

				// Primary API Call with Retries
				let primarySuccess = false;
				for (let attempt = 0; attempt <= (options.retries ?? 3); attempt++) {
					try {
						const result = await makeApiCall(apiUrl, httpMethod, headers, body, vaultClient, vaultSecretPath, vaultSecretKey, apiKeyHeaderName, apiKeyPrefix);
						successData.push({ json: result, pairedItem: i });
						primarySuccess = true;
						break;
					} catch (error) {
						lastError = error;
						if (axios.isAxiosError(error) && error.response && error.response.status >= 500) {
							if (attempt < (options.retries ?? 3)) {
								const delayMs = (options.retryDelayMs ?? 1000) * Math.pow(2, attempt);
								await this.delay(delayMs);
								continue; // Retry
							}
						}
						// Not a retryable error or last attempt failed
						break;
					}
				}

				if (primarySuccess) continue;

				// Fallback API Call
				if (options.enableFallback) {
					const fallbackApiUrl = options.fallbackApiUrl as string;
					const fallbackVaultPath = options.fallbackVaultSecretPath as string;
					const fallbackVaultKey = options.fallbackVaultSecretKey as string;

					if (!fallbackApiUrl || !fallbackVaultPath) {
						throw new NodeOperationError(this.getNode(), 'Fallback is enabled, but Fallback API URL or Vault Path is missing.');
					}

					try {
						const fallbackResult = await makeApiCall(fallbackApiUrl, httpMethod, headers, body, vaultClient, fallbackVaultPath, fallbackVaultKey, apiKeyHeaderName, apiKeyPrefix);
						fallbackData.push({ json: fallbackResult, pairedItem: i });
						continue; // Fallback succeeded
					} catch (error) {
						lastError = new Error(`Primary call failed with: ${lastError?.message}. Fallback call also failed with: ${error.message}`);
					}
				}

				if (lastError) {
					throw lastError;
				}

			} catch (error) {
				if (this.continueOnFail()) {
					const errorJson = { error: error.message };
					if (axios.isAxiosError(error) && error.response) {
						errorJson['response'] = error.response.data;
						errorJson['status'] = error.response.status;
					}
					successData.push({ json: errorJson, pairedItem: i });
					continue;
				}
				if (error instanceof NodeOperationError) throw error;
				throw new NodeOperationError(this.getNode(), error, { itemIndex: i });
			}
		}

		return [successData, fallbackData];
	}
}