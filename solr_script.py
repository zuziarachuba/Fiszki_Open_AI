import openai
from pydantic import BaseModel
import argparse
from tqdm import tqdm
import jsonlines

KEY_WORDS = ["tabela", "rycina", "algorytm", "ryc"]

parser = argparse.ArgumentParser(description="Mając plik .jsonl zdecyduj, czy dany tekst nadaje się na fiszkę")

parser.add_argument('file', type=str, help='ścieżka do pliku wejściowego')
parser.add_argument('output', type=str, help='ścieżka do pliku wyjściowego')
parser.add_argument('url', type=str, help="base url", default="http://10.64.0.6:6666/v1")
parser.add_argument('model', type=str, help="model", default="speakleash/Bielik-4.5B-v3.0-Instruct")
parser.add_argument('limit', type=int, help="limit znaków, żeby json mógł być brany pod uwagę")

args = parser.parse_args()

file_path = args.file
valid_json = args.output
url = args.url
model = args.model
limit = args.limit

client = openai.OpenAI(base_url=url, api_key="blablabla")


SYSTEM_PROMPT = """
Kontekst: Jesteś ekspertem w sprawie edukacji w dziedzinach medycyny. 
Zdecyduj, czy dany tekst nadaje się na zrobienie z niego fiszki ułatwiającej zrozumienie danego zagadnienia.
Tekst: 
"""


class Classification(BaseModel):
    is_valid_for_fiszka: bool


def is_the_sentence_valid(input_text):
    response = client.beta.chat.completions.parse(model=model, messages=[
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': input_text}
    ], response_format=Classification)

    answer: Classification = response.choices[0].message.parsed
    result = answer.is_valid_for_fiszka
    return result
    
def main():
    with jsonlines.open(file_path) as reader:
        for obj in tqdm(reader):
            x = f'"{str(obj)}"'
            if not is_the_sentence_valid(x):
                continue
            if any(keyword in x.lower() for keyword in KEY_WORDS): 
                continue
            if not len(x) > limit:
                continue
            with jsonlines.open(valid_json, mode='a') as writer:
                obj[0]["body"] = obj[0]["body"].strip().replace("\u00A0"," ").replace("\u2012", "-").replace("\u2013", "-")
                writer.write(obj)

if __name__ == "__main__":
    main()
      
                    

