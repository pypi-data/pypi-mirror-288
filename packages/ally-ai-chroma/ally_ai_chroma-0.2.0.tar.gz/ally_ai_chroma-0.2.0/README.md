# Ally AI

## How to use

### Config File

#### Use API

```yaml
chromadb:
  host: "<endpoint>"
  port: 8000
  ssl: False
```

#### Use Local
```yaml
chromadb:
  persist_directory: './chroma/chroma'
```


### Initialize

```python
from ally_ai_chroma import Chroma

chroma = Chroma()
```

### Visualise Embeddings

```python
from ally_ai_chroma.ChromaEmbeddingsVisualisation import Chroma, ChromaEmbeddingsVisualisation

chroma = Chroma()
visualise = ChromaEmbeddingsVisualisation(chroma=chroma, limit=100)
query = 'what is an ally?'
visualise(query=query)
```



