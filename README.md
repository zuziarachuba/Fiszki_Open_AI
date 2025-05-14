This script processes a .jsonl file and filters entries to determine whether a given text is suitable for creating a flashcard (fiszka), particularly in the medical education domain.
Features:
- Uses an LLM via OpenAI-compatible API to evaluate flashcard suitability.
- Filters out entries containing specific keywords (e.g., "table", "figure", "algorithm").
- Only includes entries exceeding a minimum character length.
- Cleans up accepted entries and saves them to an output .jsonl file.
  Requirements:
  - Python 3.8+
  - Packages: openai, pydantic, argparse, tqdm, jsonlines
  Usage: python script.py <input_file.jsonl> <output_file.jsonl> <base_url> <model_name> <char_limit>, ex. python script.py data/input.jsonl data/valid.jsonl http://localhost:8000/v1 my-model-name 300
