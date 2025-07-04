# Custom n8n Nodes for CreativeFlow AI

This directory contains custom n8n nodes developed specifically for the CreativeFlow AI platform. These nodes provide specialized functionality that is either not available in the standard n8n node set or requires a more streamlined, secure, and integrated approach for our platform.

## Overview of Custom Nodes

### 1. CreativeFlow: Secrets Manager

*   **Purpose:** To provide a dedicated and secure n8n node for fetching secrets (e.g., API keys, database credentials) from HashiCorp Vault.
*   **Why it's needed:** While n8n's built-in HTTP Request node can interact with Vault, this custom node abstracts the API complexity, centralizes the interaction logic, and provides a more user-friendly interface for workflow developers. It also leverages n8n's own credential system for storing the Vault access token or AppRole credentials, ensuring they are managed securely within n8n.

---

## Installation

To use these custom nodes, they must be made available to your n8n instance.

1.  **Build the Nodes:**
    Navigate to each node's directory (e.g., `secrets_manager_node`) and run the build command:
    ```bash
    npm install
    npm run build
    ```
    This will compile the TypeScript (`.node.ts`) files into JavaScript (`.node.js`) in a `dist` directory.

2.  **Deploy to n8n:**
    The recommended method is to mount the custom nodes directory into the n8n Docker container.

    Update your `docker-compose.yml` for the n8n service:

    ```yaml
    services:
      n8n:
        image: n8nio/n8n
        ...
        volumes:
          - ~/.n8n:/home/node/.n8n
          - ./custom_nodes:/home/node/.n8n/custom # Mount this directory
        ...
    ```

3.  **Restart n8n:**
    After updating the volume mounts, restart your n8n container for the changes to take effect.
    ```bash
    docker-compose up -d --force-recreate n8n
    ```
    n8n will automatically detect and load the custom nodes from the `/home/node/.n8n/custom` directory upon startup.

---

## Node: CreativeFlow: Secrets Manager

### Configuration

1.  **Create a Vault Credential:**
    *   In n8n, go to `Credentials` > `Add credential`.
    *   Search for and select `Vault API` (this credential type is defined by the node).
    *   **Name:** Give your credential a descriptive name (e.g., "CreativeFlow Vault Production").
    *   **Vault Address:** Enter the full URL of your Vault instance (e.g., `https://vault.yourdomain.com`).
    *   **Vault Token:** Enter a valid Vault token with permissions to read the required secrets.
    *   Save the credential.

2.  **Add the Node to a Workflow:**
    *   Search for `CreativeFlow: Secrets Manager` in the nodes panel and drag it onto the canvas.
    *   **Credential for Vault API:** Select the credential you created in the previous step.
    *   **Secret Path:** Enter the full path to the secret in Vault (e.g., `kv/data/creativeflow/ai_services/openai`).
    *   **Secret Key (Optional):** If you want to retrieve a specific key from the secret's data, enter its name here (e.g., `apiKey`). If left blank, the node will return the entire data object.

### Usage Example

Imagine you need to get the OpenAI API key before calling the OpenAI DALL-E sub-workflow.

1.  **Secrets Manager Node:**
    *   **Credential:** `CreativeFlow Vault Production`
    *   **Secret Path:** `kv/data/creativeflow/ai_services/openai`
    *   **Secret Key:** `apiKey`

2.  **Execute Workflow Node (for DALL-E):**
    *   Connect the Secrets Manager node to the Execute Workflow node.
    *   In the parameters for the DALL-E workflow, you can now reference the output of the Secrets Manager node.
    *   **Parameter `apiKey`:** `{{ $('CreativeFlow: Secrets Manager').item.json.secretValue }}`

This securely fetches the key at runtime and passes it to the next step without exposing it in the workflow's JSON definition.

---

## Contributing

If you need to develop a new custom node:

1.  Create a new directory under `custom_nodes/` (e.g., `my_new_node/`).
2.  Follow the structure of `secrets_manager_node/` with a `package.json` and a `.node.ts` file.
3.  Use the `n8n-workflow` interfaces (`INodeType`, `INodeTypeDescription`, `IExecuteFunctions`, etc.) to build your node.
4.  Define the node's properties, inputs, outputs, and execution logic.
5.  Add build scripts to your `package.json`.
6.  Remember to document the new node in this README file.