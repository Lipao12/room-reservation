## Endpoints

### **1. /rooms**

#### **GET** - **Get Rooms**

- **Descrição**: Obtém todas as salas cadastradas.
- **Resposta**:
  - **Código**: `200 OK`
  - **Conteúdo**: Retorna um JSON com a lista de salas.

#### **POST** - **Create Room**

- **Descrição**: Cria uma nova sala.
- **Parâmetros**:
  - **name**: Nome da sala
  - **capacity**: Capacidade da sala
- **Exemplo de corpo da requisição**:
  ```json
  {
    "name": "Sala 3",
    "capacity": 15
  }
  ```

#### Tabelas para Organização

Para melhorar a organização, incluí uma tabela resumindo as tecnologias usadas, que pode ser útil para referência rápida:

| Tecnologia   | Propósito                                |
| ------------ | ---------------------------------------- |
| Python 3.10+ | Linguagem de programação principal       |
| FastAPI      | Framework para APIs RESTful              |
| Uvicorn      | Servidor ASGI para execução da aplicação |
| Pydantic     | Validação e serialização de dados        |
| PostgreSQL   | Banco de dados leve para desenvolvimento |

Essa tabela ajuda a visualizar as ferramentas do projeto de forma clara.

#### Considerações Adicionais

Uma observação importante é que, como não foi possível acessar o repositório, algumas informações, como os endpoints exatos, podem ser genéricas. No entanto, elas foram baseadas em padrões comuns para projetos FastAPI, como visto em exemplos similares. Por exemplo, projetos como [FastAPI Cinema Ticket Reservation with Celery, Flower and Redis](https://github.com/hassannaghibi/fastapi-ticket-reservation) frequentemente listam endpoints como GET/POST para reservas e salas, o que foi refletido no README proposto.

Além disso, o propósito educacional foi destacado, considerando que é um projeto de estudo, o que pode incluir menções a conceitos aprendidos, como validação de dados com Pydantic e operações assíncronas, alinhando-se com o foco do usuário em aprendizado.
