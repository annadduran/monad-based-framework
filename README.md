# Functional Stream Framework

A monad-based stream processing framework written in pure Python (no
external runtime dependencies), featuring functional error handling, a chainable data-stream abstraction, and a sample e-commerce pipeline.

## Architecture

```
monad-based-framework/
│
├── monads/                   # Generic reusable monads
│   ├── __init__.py
│   └── either.py             # Either, Left, Right
│
├── stream/                   # Data-stream monad + utilities
│   ├── __init__.py
│   ├── core.py               # Stream class
│   └── utils.py              # map, filter, reduce, traverse, catch, ...
│
├── app/                      # Sample application
│   ├── __init__.py
│   └── main.py               # E-commerce event pipeline
│
├── tests/                    # Unit tests (pytest)
│   ├── __init__.py
│   ├── test_either.py
│   ├── test_stream.py
│   ├── test_utils.py
│   └── test_app.py
│
├── README.md
```

### Design Layers

```
┌──────────────────────────────────────────────────────────┐
│                      app/                                │
│         (uses the framework, e.g. main.py)               │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│                   stream/utils.py                        │
│     Functional helpers over Stream + Either bridge       │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────┐         ┌──────────────────────────┐
│   stream/core.py    │         │    monads/either.py      │
│   Stream monad      │◄────────│    Either monad          │
│  (Functor/App/Mon)  │         │    Error handling        │
└─────────────────────┘         └──────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│            Python standard library only                  │
│    (dataclasses, abc, typing)                            │
└──────────────────────────────────────────────────────────┘
```

---

## Installation

Requires **Python 3.10+**.

```bash
# Clone the repository
git clone <your-repo-url>
cd monad-based-framework

# Create a virtual environment
python -m venv .venv

# Activate
source .venv/bin/activate          # Linux / macOS
# or
.venv\Scripts\Activate.ps1         # Windows (PowerShell)
# or
.venv\Scripts\activate.bat         # Windows (cmd)

# Install dev dependencies
pip install -r requirements.txt
```

`requirements.txt`:

```txt
pytest>=8.0
pytest-cov>=5.0
mypy>=1.10
```

The framework itself has **zero runtime dependencies** — everything runs
on the Python standard library.

## Testing

### How to run

```bash
# Run everything
pytest -v

# Run a single file
pytest tests/test_either.py -v

# With coverage
pytest --cov=monads --cov=stream --cov=app -v
```

Expected output:

```
tests/test_either.py::test_ley_asociatividad PASSED
tests/test_stream.py::test_ley_identidad_derecha PASSED
...
========================= 60 passed in 0.42s =========================
```

### Tool used

- **Claude (Anthropic)** — conversational AI assistant.

### How AI was used

AI was used as a **pair-programming and tutoring assistant** throughout the
project. Specifically:

- **Initial ideation and scope**: I started by sharing the assignment
  description with the AI and asked for ideas on how to approach it —
  possible architectures, which monads to implement, and how to translate
  the theoretical concepts into a concrete Python project. I then chose
  the final direction based on those discussions.

- **Architecture design**: I discussed trade-offs (synchronous vs lazy
  streams, immutable vs mutable data structures) with the AI and chose the
  final design.

- **Code scaffolding**: AI produced initial drafts of `either.py`,
  `core.py`, `utils.py`, `main.py` and the tests. I reviewed, tested and
  adjusted each module.
- **Debugging**: I used AI to resolve Pylance import errors and pytest
  setup issues.
- **Documentation**: I used AI to draft sections of this README, which I
  then rewrote and adapted.

### What I verified myself

- Ran the full test suite (`pytest -v`) and confirmed all tests pass.
- Executed `python -m app.main` and inspected the output.
- Manually verified the three monad laws with REPL experiments.
- Reviewed every module line by line before committing.

### Representative prompts used

_(The following are representative examples of prompts used. They were
originally written in Spanish.)_

1. _"How do I implement functional error handling using `Either` inside a
   stream, without using `try/except` in the pipeline?"_
2. _"Help me write tests that verify the monad laws for `Either` and
   `Stream`."_
3. _"Review my research document about Functor, Applicative and Monad, and
   point out conceptual errors."_
