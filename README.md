# LLM Practical Portfolio - PUSL3205

Practical portfolio (P1) for PUSL3205 (Large Language Models and Generative AI)

| | |
|---|---|
| Student | Pinnagodage Menadi |
| Student number | 10967094 |
| Module leader | Ms. Thilini Bakmeedeniya |

Each lab has its own folder with a `README.md` covering: laboratory session, objective, tasks and implementation, results and evidence, observations, and learning outcomes.

## Laboratory activities

| Lab | Title | Main work | Tools |
|:-:|---|---|---|
| 1 | [Sentiment Analysis Using Traditional ML](Lab-01-Sentiment-Analysis-ML/) | Text preprocessing, Bag-of-Words, classical classifier | pandas, NLTK, scikit-learn |
| 2 | [AI in Everyday Challenges](Lab-02-LLM-Everyday-Life/) | Group product concept: **Sipwise**, a timetable-aware hydration app and smart bottle cap with an LLM inside | Claude (design partner), pitch deck |
| 3 | [Tiny Transformer Language Model](Lab-03-Tiny-Transformer/) | GPT-style Transformer built from scratch and trained on TinyStories (12.3M parameters, perplexity 6.25) | PyTorch, Hugging Face, Gradio |
| 4 | [Fine-Tuning with LoRA / QLoRA](Lab-04-Fine-Tuning-LoRA/) | QLoRA fine-tuning of Qwen2.5-0.5B-Instruct on a custom computer-shop dataset; original vs fine-tuned comparison | transformers, PEFT, TRL, bitsandbytes |
| 5 | [RAG Pipeline](Lab-05-RAG-Pipeline/) | Local RAG over university PDFs with upload, duplicate prevention and multilingual (Sinhala/Tamil) retrieval | LangChain, Ollama, ChromaDB, Streamlit |
| 6 | [AI Agents](Lab-06-AI-Agents/) | Tool-using agent with memory, RAG search and Google Calendar; n8n workflow | LangChain, Ollama, SQLite, Google Calendar API |

**[Final reflection](Final-Reflection.md)**

## Repository structure

```
PUSL3205_P1_Portfolio/
├── README.md
├── Lab-01-Sentiment-Analysis-ML/
├── Lab-02-LLM-Everyday-Life/
│   ├── group-activity/
│   ├── presentation/
│   └── screenshots/
├── Lab-03-Tiny-Transformer/
│   ├── notebooks/
│   └── results/
├── Lab-04-Fine-Tuning-LoRA/
│   ├── notebooks/
│   └── results/
├── Lab-05-RAG-Pipeline/
│   ├── documents/
│   └── experiments/
├── Lab-06-AI-Agents/
└── Final-Reflection.md
```

## Running the code

- **Labs 1, 3, 4:** Jupyter notebooks. Labs 3 and 4 were run on Google Colab with a T4 GPU, and their saved outputs are in the notebooks.
- **Labs 5 and 6:** run locally with Python 3.12 and [Ollama](https://ollama.com) (`llama3.2:3b`, `qwen3-embedding:0.6b`). See each lab's README. Lab 6's memory agent uses the database built in Lab 5.

## Version history

Labs 3 and 5 were first developed in their own repositories, and their full commit history is kept there.

- Lab 3: [Tiny-transformer-tinystories](https://github.com/MenadiDev/Tiny-transformer-tinystories)
- Lab 5: [University-Knowledge-RAG](https://github.com/MenadiDev/University-Knowledge-RAG)

The final versions were then copied into this portfolio and documented, so this repository's commit history covers the portfolio's assembly, not the original development.
