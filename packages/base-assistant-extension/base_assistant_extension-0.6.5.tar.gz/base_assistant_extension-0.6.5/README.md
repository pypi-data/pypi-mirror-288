# Assistant Base Extension

Use this library to add extension to https://github.com/samuelint/ai-assistant.

## How to use
1. Add the library to your project
```bash
poetry add base-assistant-extension
```

2. At the base of your project export a class Called `Extension`
```python
# extension.py
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable
from base_assistant_extension.base_extension import (
    BaseExtension,
)
from langchain_core.prompts import PromptTemplate


class Extension(BaseExtension):
    def name(self) -> str:
        return "joker"

    def description(self) -> str:
        return "Tell jokes."

    def create_runnable(self, llm: BaseChatModel) -> Runnable:
        prompt = PromptTemplate.from_template(
            "You tell jokes. No matter the question. You have to tell a joke."
            "{messages}"
        )

        return prompt | llm
```

```python
# __init__.py
from .extension import Extension

__all__ = ["Extension"]
```

3. Build
```bash
poetry build
```
will produce a `.whl` file. Which is the extension to be used.
