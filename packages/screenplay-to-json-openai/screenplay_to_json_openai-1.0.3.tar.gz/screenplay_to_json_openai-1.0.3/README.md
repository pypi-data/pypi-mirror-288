# Screenplay PDF to JSON Converter

## Description

After years of trying to convert screenplay PDFs to a machine-readable format consistently using Final Draft and PDF Python tools, we decided to create our own screenplay PDF to JSON converter using OpenAI vision transformers. The results are much more reliable for our purposes.

The package converts a Screenplay PDF into a JSON file using the OpenAI API, returns JSON and writes it to a local file whose name is the screenplay filename.json. The process currently costs about 50 cents via the OpenAI API to convert an hour-long pilot, but will no doubt go down in price exponentially over time.

Below is an example of the JSON structure output to file:
```json
[
    {
        "type": "dialogue",
        "name": "JOHN",
        "modifier": "(V.O.)",
        "content": "Hello, how are you?",
        "page": 1
    },
    {
        "type": "action",
        "content": "John walks into the room.",
        "page": 3
    },
    {
        "type": "dialogue",
        "name": "MARY",
        "modifier": "(smiling)",
        "content": "I'm good, thank you!",
        "page": 4
    },
    {
        "type": "dialogue",
        "name": "JOHN",
        "content": "That's great to hear.",
        "page": 4
    },
    {
        "type": "scene",
        "content": "INT. LIVING ROOM - DAY",
        "page": 5
    }
]
```

## Getting Started

### Installation
```bash
pip install screenplay-pdf-to-json-openai
```

### OpenAI
You will need to provide your own OpenAI key. Follow the instructions [here](https://platform.openai.com/docs/quickstart).

### Known Issues
- Because it uses a statistical model, sometimes split action lines will be combined into a single JSON Action element and sometimes into multiple Action elements.
- If slug-lines are used WITHOUT INT and EXT then their behaviour is unpredictable but easily detectable.

## Quickstart

### 1. Convert Whole Screenplay and Save to JSON File
```python
from screenplay_pdf_to_json import ScreenplayPDFToJSON
sptj = ScreenplayPDFToJSON(api_key=<your_openai_key>)
data = sptj.convert('TheEmpireStrikesBack.pdf')
```

### 2. Convert First 3 Pages of a Screenplay and Save to JSON File
```python
from screenplay_pdf_to_json import ScreenplayPDFToJSON
sptj = ScreenplayPDFToJSON(api_key=<your_openai_key>)
data = sptj.convert('TheEmpireStrikesBack.pdf', end_page=3)
```

### 3. Estimate Cost of Converting a Screenplay
```python
from screenplay_pdf_to_json import ScreenplayPDFToJSON
sptj = ScreenplayPDFToJSON(api_key=<your_openai_key>)
cost = sptj.estimate_cost('TheEmpireStrikesBack.pdf')
print(f"Estimated cost to convert screenplay: ${cost:.2f}")
```

### 4. Convert Screenplay with No Title Page and Save to JSON File
```python
from screenplay_pdf_to_json import ScreenplayPDFToJSON
sptj = ScreenplayPDFToJSON(api_key=KEY, skip_title_page=False)
data3 = sptj.convert('screenplay_with_no_title_page.pdf')
```
