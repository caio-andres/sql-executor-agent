# Arquitetura do Projeto

Este arquivo descreve, em formato de diagrama Mermaid, a arquitetura completa do sistema implementado em código (Terraform + Lambdas + API Gateway).

```mermaid
flowchart LR
  U[Usuário]
  APIGW["API Gateway<br>ai-agents-api"]
  subgraph Lambdas
    L1["Agent1<br>Gera SQL"]
    L2["Executor<br>Executa Athena"]
    L3["Agent2<br>Formata Resposta"]
  end
  SM["AWS Secrets Manager<br>(openai-api-key)"]
  OAI[OpenAI API]
  ATH[Athena]
  CW[CloudWatch Logs]

  U -->|POST /generate-sql| APIGW
  APIGW -->|invoke| L1
  L1 -->|GetSecretValue| SM
  L1 -->|completions| OAI
  OAI -->|SQL Gerado| L1
  L1 -->|POST /execute-query| APIGW
  APIGW -->|invoke| L2
  L2 -->|StartQueryExecution| ATH
  ATH -->|GetQueryResults| L2
  L2 -->|POST /format-response| APIGW
  APIGW -->|invoke| L3
  L3 -->|completions| OAI
  OAI -->|Texto Formatado| L3
  L3 -->|200 OK| APIGW
  APIGW -->|Resposta| U

  L1 & L2 & L3 --> CW
```

## Componentes

- **API Gateway (`ai-agents-api`)**

  - Roteia tudo através de três rotas:
    - `POST /generate-sql` → invoca **Agent1**
    - `POST /execute-query` → invoca **Executor**
    - `POST /format-response` → invoca **Agent2**

- **Lambda Functions**

  - **Agent1:** Gera a query SQL com base no prompt do usuário, usando OpenAI.
  - **Executor:** Executa a query no Athena e retorna resultados.
  - **Agent2:** Gera a resposta humanizada com base nos dados da query.

- **AWS Secrets Manager**

  - Armazena a chave `openai-api-key` usada pelas Lambdas.

- **OpenAI API**

  - Modelo de linguagem (por exemplo, `gpt-4` ou `gpt-3.5-turbo`).

- **Amazon Athena**

  - Executa queries SQL sobre dados armazenados no S3.

- **CloudWatch Logs**
  - Coleta logs de todas as funções para monitoramento e depuração.

---

Este diagrama e descrição refletem o código Terraform e a implementação das Lambdas, facilitando a compreensão da infraestrutura e dos fluxos de dados.
