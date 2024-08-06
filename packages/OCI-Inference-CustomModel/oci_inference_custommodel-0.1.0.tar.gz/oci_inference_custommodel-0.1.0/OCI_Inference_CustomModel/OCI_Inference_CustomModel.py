import oci
import json
import requests
from datetime import datetime
from typing import List, Dict, Any, Union

class OCIinference_customModel:
    def __init__(self, url: str, token: str, model_id: str, temperature = 0.1, top_p = 0.75, max_tokens = 1000, stop = "<|im_end|>"):
        self.url = url
        self.token = token
        self.model_id = model_id
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.stop = stop
        self.url_suffix = "/chat/completions"

    def chat(self, messages: List[Dict[str, Union[str, Any]]]) -> Union[List[Any], str]:
        print(f"{datetime.now()} ==> Inferencing the custom hosted model {self.url + self.url_suffix} api via http request")
        headers = {
        "Authorization": f'Bearer {self.token}',
        "accept": "application/json",
        "content-type": "application/json"
                }
        payload = json.dumps({
        "model": self.model_id,
        "messages": messages,
        "temperature": self.temperature,
        "top_p": self.top_p,
        "max_tokens": self.max_tokens,
        "stop": "<|im_end|>"
        })
        url = self.url + self.url_suffix
        http_output = {}
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()  # Raise exception for unsuccessful requests
            response_json = response.json()
            print("response receieved from http reqeust")
            if 'choices' in response_json:
                answer = response_json['choices'][0]['message']['content'].strip()
                prompt_tokens = int(response_json["usage"]["prompt_tokens"])
                completion_tokens = int(response_json["usage"]["completion_tokens"])
                total_tokens = int(response_json["usage"]["total_tokens"])
                http_output["answer"]=answer
                http_output["prompt_tokens"]=prompt_tokens
                http_output["completion_tokens"]=completion_tokens
                http_output["total_tokens"]=total_tokens
                return http_output
            else:
                print('Error in http request')
                return 'Error occured in received http response == ' + str(response_json)
            
        except Exception as e:
            return 'Exception occured in http request ' + str(e)
        

    def show_input_parameters(self) -> dict[str, Any]:
        """
        Returns a dictionary describing the input parameters and their expected formats.
        
        :return: A dictionary with details about input parameters.
        """
        return {
            "url": {
                "type": "str",
                "description": "The URL of the custom hosted llm end point."
            },
            "token": {
                "type": "str",
                "description": "The authorization token."
            },
            "model_id": {
                "type": "str",
                "description": "Moded ID to be used"
            },
            "messages": {
                "type": "List[Dict[str, Union[str, Any]]]",
                "description": "A list of messages in the format: "
                               "[{'role': 'system', 'content': system_prompt}, "
                               "{'role': 'user', 'content': user_prompt}]"
            },
            "temperature": {
                "type": "float",
                "description": "Sampling temperature."
            },
            "top_p": {
                "type": "float",
                "description": "Top-p sampling value."
            },
            "max_tokens": {
                "type": "int",
                "description": "Maximum number of tokens to generate."
            },
            "stop": {
                "type": "str",
                "description": "Stop sequence for generation."
            }
        }
    