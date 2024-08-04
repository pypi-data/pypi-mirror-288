# Midfield Documentation

## Introduction

Midfield is a Python package designed to validate prompts using an external API. It ensures the quality and reliability of text outputs from large language models (LLMs) by providing a suite of pre-built and custom validators.

## Features

- Easy integration with any Python application.
- Validators are associated with the API key and managed through the Midfield website.
- User-friendly interface to validate prompts.

## Installation

You can install the `midfield` package via pip:

```bash
pip install midfield
```

## Usage

### Step 1: Obtain an API Key

To use Midfield, you need an API key. Sign up at [midfield.ai](https://midfield.ai) and obtain your API key. During the signup process, you will associate the necessary checks with your API key.

### Step 2: Initialize the Package

```python
from midfield import Midfield

midfield = Midfield(api_key='your-api-key')
```

### Step 3: Validate the Prompt

Use the `validate` method to validate your prompt. The associated checks will be retrieved automatically based on your API key.

```python
prompt = "Your prompt text here"

try:
    result = midfield.validate(prompt)
    print(result)
except Exception as e:
    print(f"Validation failed: {e}")
```

### Example Responses

#### Invalid API Key

If the API key provided is invalid, you will get the following error:

```plaintext
Validation failed: Error: Provided API KEY is invalid
```

#### Validation Error

If the prompt does not pass the validation checks associated with the API key, you will get an error message similar to the following:

```plaintext
Validation failed: Error: Validation failed for field with errors: Result must match \(?\d{3}\)?-? *\d{3}-? *-?\d{4}
```

#### Successful Validation

If the prompt passes all the validation checks, you will get a success message:

```json
{
    "message": "Prompt validated successfully!"
}
```

## Detailed Documentation

For more detailed documentation, visit [midfield.ai/docs](https://midfield.ai/docs).

## Examples

### Basic Example

```python
from midfield import Midfield

midfield = Midfield(api_key='your-api-key')

prompt = "Call me at 123-456-7890."

try:
    result = midfield.validate(prompt)
    print(result)
except Exception as e:
    print(f"Validation failed: {e}")
```

## API Reference

The `midfield` package provides the following main components:

- `Midfield`: The main class to initialize with your API key and use for validating prompts.

### Midfield Class

- `Midfield(api_key: str)`: Initializes the Midfield instance with the provided API key.
- `validate(prompt: str)`: Validates the given prompt. The checks associated with the API key will be used automatically.

## Available Validators

Midfield supports a wide range of validators. Here is a detailed list of available validators and their parameters:

1. **regex_match**
   - **Parameters**: `regex` (str)
   - **Description**: Validates that the input matches the specified regular expression.

2. **toxic_language**
   - **Parameters**: `validation_method` (str, optional), `threshold` (float, optional)
   - **Description**: Checks for toxic language in the input.

3. **mentions_drugs**
   - **Parameters**: None
   - **Description**: Checks if the input mentions drugs.

4. **competitor_check**
   - **Parameters**: `competitors` (list of str)
   - **Description**: Checks if the input mentions any competitors from the specified list.

5. **valid_length**
   - **Parameters**: `min` (int, optional), `max` (int, optional)
   - **Description**: Validates that the input length is within the specified range.

6. **valid_url**
   - **Parameters**: None
   - **Description**: Checks if the input is a valid URL.

7. **valid_json**
   - **Parameters**: None
   - **Description**: Checks if the input is a valid JSON string.

8. **valid_python**
   - **Parameters**: None
   - **Description**: Checks if the input is valid Python code.

9. **valid_sql**
   - **Parameters**: None
   - **Description**: Checks if the input is valid SQL.

10. **web_sanitization**
    - **Parameters**: None
    - **Description**: Sanitizes the input to prevent web vulnerabilities.

11. **valid_address**
    - **Parameters**: None
    - **Description**: Checks if the input is a valid address.

12. **unusual_prompt**
    - **Parameters**: None
    - **Description**: Checks for unusual prompts.

13. **sql_column_presence**
    - **Parameters**: `columns` (list of str)
    - **Description**: Ensures the presence of specified columns in SQL.

14. **responsiveness_check**
    - **Parameters**: None
    - **Description**: Checks for responsiveness.

15. **regex_match**
    - **Parameters**: `regex` (str)
    - **Description**: Validates that the input matches the specified regular expression.

16. **reading_time**
    - **Parameters**: None
    - **Description**: Estimates reading time for the input.

17. **quotes_price**
    - **Parameters**: None
    - **Description**: Checks for quoted prices in the input.

18. **one_line**
    - **Parameters**: None
    - **Description**: Ensures the input is a single line of text.

19. **lower_case**
    - **Parameters**: None
    - **Description**: Ensures the input is in lower case.

20. **has_url**
    - **Parameters**: None
    - **Description**: Checks if the input contains a URL.

21. **exclude_sql_predicates**
    - **Parameters**: None
    - **Description**: Ensures the input does not contain SQL predicates.

22. **endpoint_is_reachable**
    - **Parameters**: None
    - **Description**: Checks if a given endpoint is reachable.

23. **similar_to_document**
    - **Parameters**: None
    - **Description**: Checks if the input is similar to a given document.

24. **saliency_check**
    - **Parameters**: None
    - **Description**: Checks for salient information in the input.

25. **relevancy_evaluator**
    - **Parameters**: None
    - **Description**: Evaluates the relevancy of the input.

26. **provenance_llm**
    - **Parameters**: None
    - **Description**: Checks for provenance in LLM-generated text.

27. **profanity_free**
    - **Parameters**: None
    - **Description**: Ensures the input is free from profanity.

28. **logic_check**
    - **Parameters**: None
    - **Description**: Checks the logical consistency of the input.

29. **gibberish_text**
    - **Parameters**: None
    - **Description**: Checks if the input is gibberish.

30. **extracted_summary_sentences_match**
    - **Parameters**: None
    - **Description**: Validates that extracted summary sentences match the input.

31. **detect_pii**
    - **Parameters**: None
    - **Description**: Detects personally identifiable information (PII) in the input.

## Conclusion

The `midfield` package simplifies the process of validating prompts. By following the steps and examples provided, you can easily integrate it into your Python applications to ensure the quality and reliability of your LLM outputs.

For more information and detailed documentation, visit [midfield.ai/docs](https://midfield.ai/docs). If you have any questions or need further assistance, feel free to reach out to our support team.