# Tech Stack — CrystalClear

## Backend

| Componente         | Tecnologia       | Justificação                                                        |
|--------------------|------------------|---------------------------------------------------------------------|
| Linguagem          | Python 3.12+     | Ecossistema rico para análise de grafos e dados                     |
| Framework web      | FastAPI           | Async, tipagem forte (Pydantic), docs automáticas (OpenAPI)        |
| Análise de grafos  | NetworkX          | Algoritmos de centralidade, caminhos, clustering out-of-the-box    |
| ORM relacional     | SQLAlchemy 2.0    | Async support, migrations com Alembic                              |
| Driver Neo4j       | neo4j (oficial)   | Driver async oficial para Python                                   |
| Autenticação       | JWT (PyJWT)       | Stateless, role-based access control                               |
| Hashing            | bcrypt (passlib)  | Standard para hashing de passwords                                 |
| Validação          | Pydantic v2       | Integrado no FastAPI, validação de schemas de entrada/saída        |
| Testes             | pytest            | Standard Python, fixtures, parametrize, async support              |
| Cobertura          | pytest-cov        | Relatórios de cobertura integrados com pytest                      |
| Linter/Formatter   | Ruff              | Rápido, substitui flake8+isort+black                               |
| Type checking      | mypy              | Verificação estática de tipos                                      |

## Frontend

| Componente         | Tecnologia        | Justificação                                                       |
|--------------------|-------------------|--------------------------------------------------------------------|
| Framework          | React 18+         | Componentes, ecosystem maduro, boa integração com libs de grafos   |
| Linguagem          | TypeScript        | Tipagem estática, reduz erros, melhor DX                           |
| Build tool         | Vite              | Fast HMR, configuração mínima                                      |
| Visualização grafos| Cytoscape.js      | Layouts automáticos, extensões, bom para grafos médios/grandes     |
| UI components      | Shadcn/ui         | Componentes acessíveis, customizáveis, não é dependência pesada    |
| Styling            | Tailwind CSS      | Utility-first, consistente com shadcn                              |
| State management   | Zustand           | Leve, simples, sem boilerplate                                     |
| HTTP client        | Axios             | Interceptors para auth, error handling centralizado                |
| Router             | React Router v6   | Standard para SPAs React                                           |
| Testes             | Vitest + Testing Library | Rápido, compatível com Vite, testing-library para componentes |
| Linter/Formatter   | ESLint + Prettier | Standard do ecossistema                                            |

## Base de Dados

| Componente         | Tecnologia        | Justificação                                                       |
|--------------------|-------------------|--------------------------------------------------------------------|
| Grafo              | Neo4j 5+          | Modelação natural de redes de influência, queries Cypher           |
| Relacional         | PostgreSQL 16+    | Dados estruturados (users, declarações), robusto, extensível       |
| Migrations         | Alembic           | Versionamento de schema PostgreSQL                                 |

## Infraestrutura de Desenvolvimento

| Componente         | Tecnologia        | Justificação                                                       |
|--------------------|-------------------|--------------------------------------------------------------------|
| Containerização    | Docker + Compose  | Ambiente reprodutível (Neo4j, PostgreSQL, backend, frontend)       |
| CI/CD              | GitHub Actions    | Integrado com repositório, corre testes e linting em cada push     |
| Documentação API   | Swagger/ReDoc     | Gerado automaticamente pelo FastAPI                                |
| Diagramas          | SVG (Mermaid)     | Versionáveis em Git, geráveis a partir de código                   |
