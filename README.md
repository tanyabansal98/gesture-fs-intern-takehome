# Full Stack Intern Take-Home Assignment — Marketing Agency Q&A Chatbot

An interactive, fully local Q&A chatbot for a marketing agency. Clients can ask about
services, pricing, and process, and get answers retrieved from the agency's own
documents — no API keys, no GPU required.

## 🧰 Tech Stack

| Component     | Library / Tool                          |
|---------------|------------------------------------------|
| Framework     | LangChain (v0.3.x)                       |
| Embeddings    | HuggingFace `all-MiniLM-L6-v2` (local)   |
| Vector Store  | FAISS (local, in-memory)                 |
| LLM           | `google/flan-t5-base` (local, CPU)       |
| Testing       | pytest                                   |

## ✅ Prerequisites

- Python 3.10+
- ~1.2GB free disk space (for model downloads on first run, then cached)
- No API keys or GPU needed

## 🚀 Setup

```bash
git clone https://github.com/tanyabansal98/gesture-fs-intern-takehome.git
cd gesture-fs-intern-takehome

python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## ▶️ Running

**Interactive mode:**
```bash
python -m src.pipeline
```
Ask questions at the `>` prompt, type `quit` to exit.

**Single-question mode (bonus feature):**
```bash
python -m src.pipeline --query "How much does the Growth package cost?"
```
Answers one question and exits — useful for scripting or quick checks.

## 🧪 Running Tests

```bash
pytest tests/ -v
```
12 tests total, all passing. First run downloads ~1.2GB of models (embedding model +
flan-t5-base), cached afterward.

## 📁 Project Structure

```
gesture-fs-intern-takehome/
├── data/                     ← knowledge base docs: services.txt, pricing.txt, faq.txt,
│                                company_handbook.txt, product_faq.txt
├── src/
│   ├── knowledge_base.py     ← pre-built: loading, chunking, embeddings, FAISS (not modified)
│   ├── pipeline.py           ← implemented: retrieval + generation + CLI
│   └── cli_utils.py          ← added: CLI argument parsing & validation
├── tests/
│   └── test_pipeline.py      ← pre-built tests + 2 added edge-case tests
└── requirements.txt
```

## 🛠️ What Was Implemented

### `ask_question()` (src/pipeline.py)
1. Retrieves the top 3 most relevant chunks from the FAISS vector store via
   `vector_store.similarity_search(question, k=3)`.
2. Extracts each chunk's `.page_content` into a `sources` list.
3. Joins the chunks into a single `context` string.
4. Formats `PROMPT_TEMPLATE` with the context and question.
5. Passes the formatted prompt to the local LLM and extracts the generated text.
6. Returns `{"answer": str, "sources": list[str]}`.

### `main()` (src/pipeline.py)
- Builds the knowledge base and loads the LLM once, before entering the loop
  (both are expensive to reload per question).
- Runs an interactive loop: prompts for input, exits on `quit`, calls
  `ask_question()`, and prints numbered sources + the answer.
- Supports a `--query` flag for one-shot, non-interactive use.

## 🎁 Bonus Features Implemented

- **Error handling:**
  - Missing `data/` directory is detected and reported with a clear message
    instead of crashing with a raw traceback.
  - Empty/whitespace input at the prompt is caught, with an explicit message
    ("Please enter a question before proceeding.") instead of silently looping.
- **`--query` CLI flag** for single-question, non-interactive mode — useful for
  scripting or quick manual checks.
- **Type hints** added across `ask_question()`, `get_llm()`, `main()`, and
  `cli_utils.py` for clarity and easier static analysis.
- **Extracted CLI concerns** (`argparse` setup, directory validation) into a
  separate `src/cli_utils.py` module, keeping `pipeline.py` focused on the
  retrieval/generation logic.
- **2 additional test cases:**
  - `test_sources_are_non_empty_strings` — verifies every retrieved chunk is a
    non-empty string, not just that the list is non-empty.
  - `test_out_of_scope_question_still_returns_valid_structure` — verifies the
    pipeline returns a well-formed `dict` even for questions with no relevant
    answer in the knowledge base (e.g. "What is the capital of France?").

## ⚠️ Known Limitations

- **Model terseness:** `flan-t5-base` is a small (~250M parameter) local model.
  It sometimes gives correct but overly brief answers (e.g. answering "Yes." to
  "Can I cancel early?" instead of including the 50% early-termination fee that
  was present in the retrieved context). This is a model-capacity limitation,
  not a retrieval or logic bug — the correct information is present in
  `sources` even when the generated `answer` doesn't fully surface it.
- **Fixed top-k retrieval:** `similarity_search(question, k=3)` always returns
  exactly 3 chunks, even when fewer (or none) are truly relevant to the
  question. There's no similarity-score threshold or filtering, so a loosely
  related or borderline chunk can occasionally appear alongside the correct
  ones (e.g. a policy-related chunk from an unrelated document surfacing
  alongside a genuinely relevant contract-cancellation chunk, since both share
  similar "contract/policy" language at the embedding level).

## 📊 Test Results

```
12 passed in ~15s
```
