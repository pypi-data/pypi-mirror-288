import re
import json
from murnitur.main import GuardConfig
from .prompt_injection import generate_response


class HallucinationDetector:
    def __init__(self, config: GuardConfig):
        self.config = config
        self.system_prompt = """
NOTE: Only return a JSON response.

Given the contexts and actual output, generate a JSON object with 2 fields: 'verdict' and 'score'.
- 'verdict': "yes" or "no" indicating if there is hallucination.
- 'score': A float from 0 to 1. Closer to 1 means more hallucination.

**
Example contexts: ["Einstein won the Nobel Prize for his discovery of the photoelectric effect.", "Einstein won the Nobel Prize in 1968."]
Example actual output: "Einstein won the Nobel Prize in 1969 for his discovery of the photoelectric effect."

Example JSON:
{
  "verdict": "no",
  "score": 0.2,
  "reason": "Yes, Einstein won the Nobel Prize for his discovery of the photoelectric effect but it was in 1968."
}

===== END OF EXAMPLE ======

**
IMPORTANT: Only return in JSON format with 'verdict' as either "yes" or "no". Do not use any prior knowledge, and take each context at face value. Provide a 'no' verdict only if there is a contradiction.

Contexts:
{{contexts}}

Actual Output:
{{output}}

JSON:

If no hallucination is detected, return {"score": 0, "verdict": "no"}.

"""

    def detect_hallucination(self, contexts: list[str], output: str):
        prompt = self.system_prompt
        contexts_str = "\n".join(contexts)
        prompt = re.sub(r"{{contexts}}", contexts_str, prompt)
        prompt = re.sub(r"{{output}}", output, prompt)
        response = generate_response(prompt=prompt, config=self.config)
        return json.loads(response)
