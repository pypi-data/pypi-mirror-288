import oci

class OCIinference:
    def __init__(self, oci_compartment_id, oci_config_profile, oci_endpoint_id, oci_model_id):
        self.oci_compartment_id = oci_compartment_id
        self.oci_model_id = oci_model_id
        self.oci_endpoint_id = oci_endpoint_id
        self.oci_config_profile = oci_config_profile
        self.max_tokens = 1000
        self.temperature = 0.1
        self.frequency_penalty = 0
        self.top_p = 0.75
        self.top_k = 0

    def chat(self, message):
        compartment_id = self.oci_compartment_id
        config_profile = self.oci_config_profile
        config = oci.config.from_file('~/.oci/config', config_profile)
        generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=self.oci_endpoint_id, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))
        chat_detail = oci.generative_ai_inference.models.ChatDetails()
        chat_request = oci.generative_ai_inference.models.CohereChatRequest()
        chat_request.message = message
        chat_request.max_tokens = self.max_tokens
        chat_request.temperature = self.temperature
        chat_request.frequency_penalty = self.frequency_penalty
        chat_request.top_p = self.top_p
        chat_request.top_k = self.top_k
        chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id=self.oci_model_id)
        chat_detail.chat_request = chat_request
        chat_detail.compartment_id = compartment_id
        try:
            chat_response = generative_ai_inference_client.chat(chat_detail)
            return chat_response.data
        except oci.exceptions.ServiceError as e:
            return "Exception occured ==> " + "Error type ==> " + str(e.type) + " Error message ==> " + str(e.message) 
    
