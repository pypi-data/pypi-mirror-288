import os
import sys
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, AutoTokenizer
from textblob import TextBlob
import logging
import warnings
import requests
import json

class TokenizeTransformed:
    def __init__(self, model_name='tuner007/pegasus_paraphrase', checkpoint='bigscience/mt0-base'):
        # Suppress warnings
        warnings.filterwarnings("ignore")
        # Set logging level to error to suppress unnecessary messages
        logging.getLogger("transformers").setLevel(logging.ERROR)
        # Redirect stdout and stderr to /dev/null
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
        # Initialize model and tokenizer as None
        self.tokenizer_default = None
        self.model_default = None
        self.secondary_tokenizer = None
        self.torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # Load Pegasus model and tokenizer
        self.load_model_and_tokenizer(model_name, checkpoint)

    def load_model_and_tokenizer(self, model_name, tokenizerSeq2SeqIntial):
        if self.secondary_tokenizer is None:
            self.secondary_tokenizer = AutoTokenizer.from_pretrained(tokenizerSeq2SeqIntial)

    def xx_response_xx(self, text):
        # Define the API endpoint and your API key
        url = "https://openrouter.ai/api/v1/chat/completions"
        api_key = "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"

        # Define optional headers, replace these with your actual values if needed
        YOUR_SITE_URL = "https://your-site-url.com"
        YOUR_APP_NAME = "YourAppName"

        # Define the data payload
        payload = {
            "model": "openai/gpt-4o-mini-2024-07-18",  # Optional
            "messages": [
                {"role": "user", "content": f"Paraphrase this Urdu sentence in simple English: {text}"}
            ],
            "top_p": 0.99,
            "temperature": 0.9,
            "frequency_penalty": 1.53,
            "presence_penalty": 1.7,
            "repetition_penalty": 1,
            "top_k": 50,
        }

        # Make the POST request
        response = requests.post(
            url=url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": f"{YOUR_SITE_URL}",  # Optional
                "X-Title": f"{YOUR_APP_NAME}",  # Optional
            },
            data=json.dumps(payload)
        )

        content_str = ""

        # Check if the request was successful
        if response.status_code == 200:
            response_json = response.json()
            content = response_json['choices'][0]['message']['content']

            try:
                # Try to parse the content as JSON
                parsed_content = json.loads(content)
                content_str += json.dumps(parsed_content, indent=4)
            except json.JSONDecodeError:
                # If content is not JSON, use it as is
                content_str += content

            return content_str
        else:
            return "Max_tokens limit exceeded"

    def tokenized_inputs(self, text):
        try:
            urdu_text = TextBlob(self.xx_response_xx(text)).translate(from_lang='en', to='ur')
            inputs = self.secondary_tokenizer.encode(str(urdu_text), return_tensors="pt")
            return [inputs, self.secondary_tokenizer]
        except Exception as e:
            print("Error:", e)
            return None

# Example usage
# tokenizer_transformed = TokenizeTransformed()
# urdu_text = "وہ اپنے وقت کا ایک معروف شخص تھا اس کے گرد ایک ہجوم رہتا وہ جنہیں دوست سمجھتا تھا جونہی اچھا وقت ختم ہوا سب غائب ہوگئے ‘سالوں کی دوستیاں گھنٹوں میں بھلادی گئیں یہاں تک جنہ
