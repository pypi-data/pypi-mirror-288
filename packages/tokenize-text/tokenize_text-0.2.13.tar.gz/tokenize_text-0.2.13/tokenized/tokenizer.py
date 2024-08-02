import os
import sys
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, AutoTokenizer
from textblob import TextBlob
import logging
import warnings
import requests
import json

class tokenize_transformed:
    def __init__(self, model_name='tuner007/pegasus_paraphrase', checkpoint='bigscience/mt0-base'):
        # Suppress warnings
        warnings.filterwarnings("ignore")
        # Set logging level to error to suppress unnecessary messages
        logging.getLogger("transformers").setLevel(logging.ERROR)
        # Redirect stdout and stderr to /dev/null
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
        # Initialize model and tokenizer as Nones
        self.tokenizer_default = None
        self.model_default = None
        self.secondary_tokenizer = None
        # Load Pegasus model and tokenizer
        torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.load_model_and_tokenizer(model_name, checkpoint)

    def load_model_and_tokenizer(self, model_name, tokenizerSeq2SeqIntial):
        if self.secondary_tokenizer is None:
            # self.tokenizer_default = PegasusTokenizer.from_pretrained(model_name)
            # self.model_default = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
            self.secondary_tokenizer = AutoTokenizer.from_pretrained(tokenizerSeq2SeqIntial)

    # def get_response(self, input_text, num_return_sequences, num_beams):
    #     input_ids = self.tokenizer_default(input_text, return_tensors='pt', max_length=len(input_text), truncation=True).input_ids.to(torch_device)
    #     input_length = input_ids.shape[-1]
    #     translated = self.model_default.generate(
    #         input_ids,
    #         max_length=input_length,
    #         num_beams=num_beams,
    #         num_return_sequences=num_return_sequences,
    #         temperature=1.5,
    #         early_stopping=True
    #     )
    #     paraphrased_texts = self.tokenizer_default.batch_decode(translated, skip_special_tokens=True)
    #     return paraphrased_texts

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
                {"role": "user", "content": f"Paraphrase this urdu sentence in simple english: {text}"}
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

            return(content_str)
        else:
            # print(f"Error: {response.status_code}")
            return("Max_tokens limit exceeded")


    def tokenize_inputs(self, text):
        try:
            # english_text = TextBlob(text).translate(from_lang='ur', to='en')
            # num_beams = 50
            # num_return_sequences = 23
            # paraphrased_texts = self.get_response(str(english_text), num_return_sequences, num_beams)
            # longest_paraphrased_text = max(paraphrased_texts, key=len)
            urdu_text = TextBlob(self.xx_response_xx(text)).translate(from_lang='en', to='ur')
            inputs = self.secondary_tokenizer.encode(str(urdu_text), return_tensors="pt")
            return [inputs, self.secondary_tokenizer]
        except Exception as e:
            print("Error:", e)
            return None

# Example usage
# pegasus_paraphraser = PegasusParaphraser()
# urdu_text = "وہ اپنے وقت کا ایک معروف شخص تھا اس کے گرد ایک ہجوم رہتا وہ جنہیں دوست سمجھتا تھا جونہی اچھا وقت ختم ہوا سب غائب ہوگئے ‘سالوں کی دوستیاں گھنٹوں میں بھلادی گئیں یہاں تک جنہ
