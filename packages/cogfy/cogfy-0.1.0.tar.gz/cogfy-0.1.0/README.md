# Cogfy Python Lib

Cogfy é um cliente Python e CLI para a API Cogfy. Ele permite que você interaja com a API Cogfy para gerenciar coleções, registros e obter respostas de chat.

## Instalação

### Via pip

Você pode instalar o pacote diretamente do repositório usando pip:

```sh
pip install cogfy
```

### Via setup.py

Clone o repositório e instale o pacote:

```sh
git clone https://github.com/IndigoHive/cogfy-python.git
cd cogfy
pip install .
```

## Configuração

Cogfy CLI usa variáveis de ambiente para configurar a URL base e a chave da API. Você pode definir essas variáveis de ambiente no seu sistema:

```sh
export COGFY_BASE_URL=https://api.cogfy.com
export COGFY_API_KEY=your_api_key
```

## Uso

### Como Biblioteca

Você pode usar o Cogfy como uma biblioteca em seu código Python:

```python
import cogfy

client = cogfy.CogfyClient(base_url='https://api.cogfy.com', api_key='your_api_key')

# Obter todas as coleções

collections = client.get_collections()

print(collections)

# Obter uma coleção específica

collection = client.get_collection('collection_id')

print(collection)
```

### Como CLI

Cogfy também pode ser usado como uma ferramenta de linha de comando (CLI). Após a instalação, você pode usar o comando cogfy:

```sh
cogfy collections list
```

#### Comandos Disponíveis

```sh
collections list: Obter todas as coleções.

collections get <collection_id>: Obter uma coleção específica.

records list <collection_id>: Obter todos os registros em uma coleção.

records create <collection_id> <properties>: Criar um novo registro em uma coleção. As propriedades devem ser fornecidas em formato JSON.

records delete <collection_id> <record_id>: Excluir um registro específico.

chats response <collection_id> <message> [--message_data <message_data>] [--chat_id <chat_id>]: Obter resposta de chat. message_data deve ser fornecido em formato JSON, se necessário.
```

#### Exemplo de Uso da CLI

```sh
# Obter todas as coleções

cogfy collections list

# Obter uma coleção específica

cogfy collections get collection_id

# Obter todos os registros em uma coleção

cogfy records list collection_id

# Criar um novo registro em uma coleção

cogfy records create collection_id '{"property": "value"}'

# Excluir um registro específico

cogfy records delete collection_id record_id

# Obter resposta de chat

cogfy chats response collection_id "Hello world!" --message_data '{"key": "value"}' --chat_id chat_id
```


## Testes

Para executar os testes, você pode usar o unittest:

```sh
python -m unittest discover -s tests
```