# Final Reflection

## From classical ML to Transformers

In Lab 1 I built a sentiment classifier with Bag-of-Words and Logistic Regression. It reached about 82% accuracy, and tuning with TF-IDF only raised it slightly to 83%. That showed me how far simple word counts can go, but also their limits: the model has no idea of word order, so negation like "not good" and sarcasm are hard for it. In Lab 3 I built a small Transformer from scratch and saw how masked self-attention lets each word look at the words before it. That is exactly what Bag-of-Words is missing, and it helped me understand why Transformers replaced older methods.

## Building a model vs adapting one

Training my own 12M-parameter model on TinyStories (Lab 3) took around 16 minutes on a GPU and produced short, simple stories with a perplexity of about 6.25. I learned that the tokenizer, model depth and number of training epochs all make a big difference, and that switching from characters to BPE improved the stories more than anything else. In Lab 4, instead of training from scratch, I fine-tuned an existing 0.5B model with QLoRA. Only 1.75% of the parameters were trained, and it took about 30 seconds on a free T4 GPU. This made it clear why parameter-efficient fine-tuning is so useful when computing power is limited.

## Fine-tuning vs RAG

The most important lesson for me came from comparing Labs 4 and 5. After fine-tuning, the model answered like the computer shop, but it still got some facts wrong and confidently made up answers to questions it was never trained on, such as keyboard brands and CCTV prices. In Lab 5, the RAG system answered from the actual university documents and could say when the information wasn't there. I now see fine-tuning as better for teaching style and format, and RAG as better for facts that need to be accurate or that change often. Extending the RAG system to Sinhala and Tamil questions also showed me that translation needs context, and that combining searches (Reciprocal Rank Fusion) can make retrieval more reliable.

## From answering to acting

In Lab 6 the model went from only answering questions to taking actions: using tools, remembering information and working with Google Calendar, both in Python and in n8n. This was the most interesting lab, but it also showed the risks. In my n8n test, the agent said it had created an event at the time I asked for, but because of how the node was set up, the event was actually created at a different time. This taught me that an agent's reply can't always be trusted, and that tool outputs need to be checked.

## Using LLMs responsibly

Across the labs I saw the same problem several times: LLMs can sound confident even when they are wrong. Grounding answers in documents, checking tool outputs and keeping a human in control all help reduce this. Privacy also matters, especially when an agent can access personal data like a calendar or uploaded documents, and language support for Sinhala and Tamil is still weaker than for English.

## Skills gained and next steps

During this module I gained practical experience with scikit-learn, PyTorch, Hugging Face Transformers, PEFT and TRL, LangChain, Ollama, ChromaDB, Streamlit, n8n and Git/GitHub. Group work in Lab 2 also showed me the value of starting from the user's real needs and comparing ideas before choosing a solution. Next, I would like to improve my RAG system with better evaluation, and build agents that check their own actions before reporting back to the user.
