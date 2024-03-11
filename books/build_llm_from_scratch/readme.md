# Build LLM from scratch - Sebastian Raschka

## 1. Understanding Large Language **Models**

- Before LLM tasks such as text classification needed handcrafted features, but they underperform LLM for complex understanding tasks
- Deeplearning advancement, compute capacity and vast amount of data caused LLM to significantly improved performance
- earlier NLP models were task specific, and LLM allows general capabilities
- Significant improvement is due to Transformer architecture
### 1.1 What is an LLM?

- Large in LLM is both model's size and immense dataset on which its trained
- Most LLM works on next token prediction - its sensible as it harness the inherent sequential nature of language
- Transformer architecture allows model to play selective attention to different parts of the input while making predictions
- Since LLMs are capable of generating text --> generative AI
- ML --> DL --> GENAI --> LLM

### 1.3 stages of building LLM

- Why to build LLM?
	- Understand better, learn its limitations and strength
	- Learn more about how to finetune it better for your given task
- Task Specific LLM outperforms general purpose LLM

- Stages
- Pre- training
	- Unsupervised, on large text data corpus
	- next token prediction
	- Text completion
- Instruction fine tuning
	- Training on task specific
	- finetuning for classification task

### 1.4 Using LLM for different task

[[_resources/Chapters/a61a61ca87317de4cb109f4d30a34df0_MD5.jpeg|Open: Pasted image 20240310232943.png]]
![[_resources/Chapters/a61a61ca87317de4cb109f4d30a34df0_MD5.jpeg]]
Encoder - Decoder framework
Attention is all you need -2017 paper (encoder, decoder framework)
Variants of Transformers - BERT(Encoder only), GPT (Decoder only)
BERT- classification task. Twitter uses bert to detect toxic content
GPT - taxt completion, zero shot and few shot learning

### 1.6 Closer look at GPT architecture

- GPT 3 - scaled up version of this model (GPT) has more parameter, more data
- Chat-gpt - gpt 3.5 turbo = GPT 3 + instruct tuning (RLHF)

- Next token prediction is - ssl - self supervised learning
- Emergent property - Decoder only models are essentially next token prediction, however as size and scale increased, it showed significant improvements in performance. 
	- Task like translation are encoder-decoder model envisioned for, decoder model can solve and do the same. 
- Natural consequence to get exposure to large data, and it taught model general language capabilities. 
[[_resources/Chapters/741d95a4b96218920effb483ff82c0e6_MD5.jpeg|Open: Pasted image 20240310234046.png]]
![[_resources/Chapters/741d95a4b96218920effb483ff82c0e6_MD5.jpeg]]

## Chapter 2 Working with text data

### 2.1 Understanding word embeddings

language of neural networks is vectors, how to represent text as a vector?
Conversion of any modality(text, image, video) of discrete objects to a continuous vector format(space) is called embedding
- Using a specific NN layer, we can embed different data types
![[_resources/Chapters/c75daddcf34fd9d7bb8201acd7fd2ef2_MD5.jpeg]]
- Different type of embeddings for text data
	- word embeddings, sentence/paragraph embeddings, 
- Word Embeddings (used specifically in training of GPT style LLM)
	- word2vec -earlier and most popular algorithm
		- Similar context words should appear closer in the latent space
	- We can chose 2 dim for viz purposes, however higher dimension embedddings can capture more nuanced relationship at expense of computational efficiency
	- You can train embeddings separately, however LLM produce theri own embeddings as part of the model training
		- Why? since its part of training of LLM it produces embeddings specific to task and data at the hand
- Embeddings size
	- GPT 2 - 768
	- GPT 3 (12,288)
	- GPT 3.5-4 (100k)
	- GEMMA - 256k

## 2.2 Tokenizing text

- GPT style models dont directly put words into embedding models, they go through a necessary processed called tokenization first.
- Tokenization is the process of converting text into smaller units called tokens
- Tokens can be words, subwords, characters or even part of words

