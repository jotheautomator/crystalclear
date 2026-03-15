# Naming Conventions — CrystalClear

## General Rule
All code, comments, documentation, commit messages, and API contracts are in **English**. Domain terminology follows the glossary in `domain/glossary.md`.

## Python (Backend)

| Element           | Convention        | Example                            |
|-------------------|-------------------|------------------------------------|
| Module/file       | snake_case        | `declaration_service.py`           |
| Class             | PascalCase        | `DeclarationService`               |
| Function/method   | snake_case        | `get_active_positions()`           |
| Variable          | snake_case        | `total_income`                     |
| Constant          | UPPER_SNAKE_CASE  | `MAX_PAGE_SIZE`                    |
| Pydantic model    | PascalCase        | `DeclarationCreate`                |
| Test function     | snake_case        | `test_submit_declaration_valid()`  |
| Private method    | _snake_case       | `_validate_dates()`               |

## TypeScript (Frontend)

| Element           | Convention        | Example                            |
|-------------------|-------------------|------------------------------------|
| File (component)  | PascalCase        | `DeclarationForm.tsx`              |
| File (utility)    | camelCase         | `formatDate.ts`                    |
| Component         | PascalCase        | `DeclarationForm`                  |
| Function          | camelCase         | `getActivePositions()`             |
| Variable          | camelCase         | `totalIncome`                      |
| Constant          | UPPER_SNAKE_CASE  | `API_BASE_URL`                     |
| Type/Interface    | PascalCase        | `DeclarationFormProps`             |
| Hook              | camelCase (use*)  | `useDeclarations()`                |
| Test file         | *.test.tsx        | `DeclarationForm.test.tsx`         |

## Database

### Neo4j
| Element           | Convention        | Example                            |
|-------------------|-------------------|------------------------------------|
| Node label        | PascalCase        | `Person`, `Institution`            |
| Relationship type | UPPER_SNAKE_CASE  | `HOLDS_POSITION`, `OWNS_ASSET`     |
| Property          | snake_case        | `valid_from`, `full_name`          |

### PostgreSQL
| Element           | Convention        | Example                            |
|-------------------|-------------------|------------------------------------|
| Table             | snake_case plural | `users`, `declarations`            |
| Column            | snake_case        | `created_at`, `password_hash`      |
| Index             | idx_table_column  | `idx_users_role`                   |
| Foreign key       | fk_table_ref      | `fk_declarations_user`             |

## API
| Element           | Convention        | Example                            |
|-------------------|-------------------|------------------------------------|
| URL path          | kebab-case        | `/api/v1/declarations`             |
| Query param       | snake_case        | `?reference_date=2024-01-01`       |
| JSON field        | snake_case        | `{ "full_name": "..." }`          |
| Enum values       | UPPER_SNAKE_CASE  | `"POLITICAL_AGENT"`, `"SUBMITTED"` |
