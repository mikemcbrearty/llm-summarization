# llm-summarization

    to make a long story short

Summarize a book using a large language model.

Here, I generate a summary of MacGregor's _The Story of Rome_ ([ref](https://www.heritage-history.com/index.php?c=read&author=macgregor&book=rome&story=_front)) using Llama 3.1.


## Set up

### python virtual environment
```
python3 -m venv virtual_environment_path
source virtual_environment_path/bin/activate
pip install -r requirements.txt
```

### Ollama
This project uses the Ollama REST API. See https://github.com/ollama/ollama for set up details.

## Example

```
>>> python3 summarize.py
The Lady Roma
Prince Æneas, one of the bravest Trojans who had defended their city against
the Greeks, fled Troy with his father and son Ascanius after it was taken by
the enemy...
```