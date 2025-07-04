import triton_python_backend_utils as pb_utils
import torch
import json
import numpy as np
# from transformers import GPT2Tokenizer, GPT2LMHeadModel # Example for a full implementation

class TritonPythonModel:
    """
    Your Python model must use the same class name (`TritonPythonModel`)
    and implement the same methods.
    """

    def initialize(self, args):
        """
        `initialize` is called only once when the model is loaded.
        Implementing `initialize` is optional. This method allows the model
        to intialize any state associated with this model.
        """
        print('GPT-2 Python backend initializing...')
        self.model_config = json.loads(args['model_config'])
        
        # # Example of parsing output configuration
        # output0_config = pb_utils.get_output_config_by_name(self.model_config, "OUTPUT__0")
        # self.output_dtype = pb_utils.triton_string_to_numpy(output0_config['data_type'])
        
        # # Example of loading model and tokenizer
        # device = "cuda" if args['model_instance_kind'] == 'GPU' else "cpu"
        # # Assumes tokenizer and model files are in the model directory
        # self.tokenizer = GPT2Tokenizer.from_pretrained("./") 
        # self.model = GPT2LMHeadModel.from_pretrained("./").to(device)
        # self.tokenizer.pad_token = self.tokenizer.eos_token

    def execute(self, requests):
        """
        `execute` must be implemented in every Python model. `execute`
        is called whenever an inference request is made for this model.
        """
        responses = []
        
        # # --- Full Implementation Example ---
        # # This commented-out block shows a more complete implementation
        # for request in requests:
        #     # Get input tensors
        #     input_ids_tensor = pb_utils.get_input_tensor_by_name(request, "INPUT__0")
        #     attention_mask_tensor = pb_utils.get_input_tensor_by_name(request, "INPUT__1")
            
        #     input_ids = input_ids_tensor.as_numpy()
        #     attention_mask = attention_mask_tensor.as_numpy()
            
        #     # Perform inference
        #     with torch.no_grad():
        #         outputs = self.model(
        #             input_ids=torch.tensor(input_ids).to(self.model.device), 
        #             attention_mask=torch.tensor(attention_mask).to(self.model.device)
        #         )
        #         logits = outputs.logits.cpu().numpy()

        #     # Create output tensor
        #     output_tensor = pb_utils.Tensor("OUTPUT__0", logits.astype(self.output_dtype))
        #     inference_response = pb_utils.InferenceResponse(output_tensors=[output_tensor])
        #     responses.append(inference_response)

        # --- Placeholder Implementation ---
        # This implementation returns a dummy response to make the backend functional
        # for testing purposes without needing a fully implemented model.
        for request in requests:
            # Create a dummy output tensor that matches the shape and type
            # defined in config.pbtxt. This may need adjustment.
            dummy_output = np.array([[[1.0]]], dtype=np.float32) 
            output_tensor = pb_utils.Tensor("OUTPUT__0", dummy_output)
            inference_response = pb_utils.InferenceResponse(output_tensors=[output_tensor])
            responses.append(inference_response)

        return responses

    def finalize(self):
        """
        `finalize` is called only once when the model is unloaded.
        Implementing `finalize` is optional. This method allows the model to
        perform any necessary clean-up before exit.
        """
        print('GPT-2 Python backend cleaning up...')