# pactify

> **Detect breaking REST API contract changes before they reach production.**

**pactify** is a Python library that helps teams **detect, classify, and prevent breaking REST API contract changes**. It compares API contracts across versions, identifies schema drift, and clearly labels changes as **safe**, **risky**, or **breaking** — making it ideal for **CI/CD pipelines**, **code reviews**, and **API governance**.

Unlike traditional validation libraries that focus only on runtime data checks, pactify focuses on **contract evolution**.

---

## Why pactify?

Modern REST APIs evolve continuously. Without strong contract governance:

* Breaking changes slip into production unnoticed
* API consumers fail silently or weeks later
* Debugging becomes slow and political
* Teams lose confidence in API stability

**pactify makes contract changes explicit, measurable, and enforceable — before deployment.**

---

## Core Concepts

### Contract

A **Contract** represents the request or response schema of a REST API endpoint.

```python
from pactify import Contract, Field

class CreateUserRequest(Contract):
    id = Field(int)
    email = Field(str, format="email")
    age = Field(int, optional=True)
```

Contracts are:

* Class-based and Pythonic
* Immutable once defined
* Comparable across versions

---

### Field

A **Field** defines metadata about an API field.

Supported attributes (v1):

| Attribute   | Description                              |
| ----------- | ---------------------------------------- |
| type        | Python type (`int`, `str`, `list`, etc.) |
| optional    | Whether the field is optional            |
| nullable    | Whether `None` is allowed                |
| default     | Default value                            |
| constraints | Format, min/max, regex, etc.             |

---

## What pactify Detects

pactify detects and classifies **schema drift**, including:

* Field added
* Field removed
* Field type changed
* Required → optional (and vice versa)
* Nullable → non-nullable (and vice versa)
* Constraint changes

Each change is classified as:

* ✅ **SAFE** – backward compatible
* ⚠️ **RISKY** – potentially breaking
* ❌ **BREAKING** – will break consumers

---

## Example: Detecting Breaking Changes

```python
from pactify import Contract, Field

class UserV1(Contract):
    id = Field(int)
    email = Field(str)

class UserV2(Contract):
    id = Field(str)                 # ❌ breaking
    email = Field(str)
    age = Field(int, optional=True) # ✅ safe
```

```bash
pactify diff UserV1 UserV2
```

Output:

```text
❌ BREAKING: field 'id' type changed int → str
✅ SAFE: optional field added 'age'
```

---

## Backward Compatibility Rules (v1)

Some examples of built-in rules:

| Change                           | Severity | Reason                          |
| -------------------------------- | -------- | ------------------------------- |
| Add optional field               | SAFE     | Consumers ignore unknown fields |
| Add required field               | BREAKING | Old consumers won’t send it     |
| Remove field                     | BREAKING | Consumers may rely on it        |
| Change type                      | BREAKING | Deserialization failure         |
| Required → optional              | SAFE     | Loosens contract                |
| Optional → required              | BREAKING | Tightens contract               |
| Narrow constraint (max_length ↓) | RISKY    | Valid data may now fail         |
| Widen constraint (max_length ↑)  | SAFE     | More permissive                 |
| Nullable → non-nullable          | BREAKING | Existing nulls break            |
| Non-nullable → nullable          | SAFE     | Loosens contract                |


These rules are deterministic and CI-friendly.

---

## CLI Usage

### Compare two contract files

```bash
pactify diff api_v1.py api_v2.py
```

### Exit codes

| Exit Code | Meaning                   |
| --------- | ------------------------- |
| 0         | Fully compatible          |
| 1         | Risky changes detected    |
| 2         | Breaking changes detected |

Perfect for CI/CD pipelines.

---

### JSON Output (for CI bots)

```bash
pactify diff api_v1.py api_v2.py --json
```

```json
{
  "compatible": false,
  "breaking": 1,
  "risky": 0,
  "safe": 1,
  "changes": []
}
```

---

## CI/CD Example (GitHub Actions)

```yaml
- name: Check API contract compatibility
  run: pactify diff api_v1.py api_v2.py
```

The build fails automatically on breaking changes.

---

## Who Should Use pactify

* Backend engineers building REST APIs
* Tech leads and architects
* Platform and API governance teams
* Microservice-based organizations

If you have ever said:

> "This change shouldn’t have broken anything"

pactify is for you.

---

## Project Philosophy

* **Contracts over assumptions**
* **Fail early, not in production**
* **Backward compatibility by default**
* **Clear explanations over clever abstractions**

---

## Roadmap

* FastAPI integration
* OpenAPI import/export
* Runtime validation modes
* Event schema support (Kafka / PubSub)
* Observability and metrics

---

## Installation

```bash
pip install pactify
```

---

## Status

🚧 **Early-stage project** — APIs may evolve rapidly until v1.0.

Feedback, issues, and contributions are welcome.

---

## License

MIT License
