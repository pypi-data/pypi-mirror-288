# Ally AI

## How to use

### Config File

```yaml
langsmith:
  langchain_tracing_v2: 'true'
  langchain_endpoint: "https://api.smith.langchain.com"
  langchain_api_key: "<your-api-key>"
  langchain_project: "future-press-release"
```

### Update api key in k8s

with using double underscore '__'
```yaml
env:
  - name: langsmith__langchain_api_key
    valueFrom:
      secretKeyRef:
        name: ...
        key: ...
```

### Create an instance

```python
from ally_ai_langsmith import Langsmith

Langsmith()
```


