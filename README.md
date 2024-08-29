# Word-Embedding

# Word Embedding Project

This project provides a Python implementation for creating word embeddings, a fundamental technique in natural language processing (NLP). It includes functions for preprocessing text, tokenizing, mapping words to indices, and generating one-hot encoded vectors to facilitate training of word embedding models.

## Features

- **Text Preprocessing**: Removes non-alphabetic characters and converts text to lowercase.
- **Tokenization**: Splits the input text into individual tokens (words).
- **Mapping Functions**: Maps tokens to unique indices and vice versa.
- **One-Hot Encoding**: Generates one-hot encoded vectors for tokens.

## Installation

To use this project, make sure you have the required libraries installed:

```bash
pip install numpy nltk matplotlib
```

## Usage

1. **Preprocess and Tokenize Text**:  
   Use the `preprocess_and_tokenize` function to clean and tokenize the input text.

   ```python
   from WordEmbedding import preprocess_and_tokenize

   text = "Sample text for word embedding."
   tokens = preprocess_and_tokenize(text)
   print("Tokens:", tokens)


2. **Map Tokens to Indices**:  
   Create mappings between words and their respective indices.

   ```python
   from WordEmbedding import mapping

   word_to_id, id_to_word = mapping(tokens)
   print("Word to ID:", word_to_id)
   print("ID to Word:", id_to_word)

3. **One-Hot Encode Tokens:
   Generate one-hot encoded vectors for tokens.

   ```pythyon
   from WordEmbedding import one_hot_encode
   vocab_len = len(word_to_id)
   encoded_vector = one_hot_encode(word_to_id['sample'], vocab_len)
   print("One-Hot Encoded Vector:", encoded_vector)


Credit: https://github.com/Eligijus112/word-embedding-creation/blob/master/master.py 



