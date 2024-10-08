# -*- coding: utf-8 -*-
"""GROUP_11_Assignment 2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Aop1WktNHLXM2FbcP1SXed4i6MhOd_pr
"""

# prompt: create a function that preprocess a text and tokenize it

import re
import nltk
nltk.download('punkt')
import numpy as np
import matplotlib.pyplot as plt


def preprocess_and_tokenize(text):
  # Remove non-alphabetic characters
  text = re.sub(r'[^a-zA-Z\s]', '', text)

  # Convert to lowercase
  text = text.lower()

  # Tokenize the text
  tokens = nltk.word_tokenize(text)

  return tokens

# prompt: create a function mapping to map between tokens and indices, and vice versa

def mapping(tokens):
    word_to_id = {}
    id_to_word = {}

    for i, token in enumerate(set(tokens)):
        word_to_id[token] = i
        id_to_word[i] = token

    return word_to_id, id_to_word

def one_hot_encode(id, vocab_len):
    ans = [0] * vocab_len
    ans[id] = 1
    return ans

def generate_training_data(tokens, word_to_id, window):
    X = []
    y = []
    n_tokens = len(tokens)

    for i in range(n_tokens):
        start = max(0, i - window)
        end = min(n_tokens, i + window + 1)

        idx = list(range(start, i)) + list(range(i + 1, end))

        for j in idx:
          if i == j:
            continue
          X.append(one_hot_encode(word_to_id[tokens[i]], len(word_to_id)))
          y.append(one_hot_encode(word_to_id[tokens[j]], len(word_to_id)))

    return np.asarray(X), np.asarray(y)

# prompt: create a function that initializes a neural network model with random weights
def init_network(vocab_size, n_embedding): # n_embedding -> number of different aspect or feature of the word's meaning or context eg. gender, age, royal, food
    model = {
        "w1": np.random.randn(vocab_size, n_embedding),
        "w2": np.random.randn(n_embedding, vocab_size)
    }
    return model

# prompt: create a function that performs a forward pass through a neural network model


def forward_pass(model, X, return_store=True):
    store = {}
    W1, W2 = model['w1'], model['w2']
    store["a1"] = np.dot(X, W1)
    store["a2"] = np.dot(store["a1"], W2)
    store["y"] = softmax(store["a2"])

    if not return_store:
      return store["y"]
    return store

def softmax(x):
    ls = []
    for i in x:
        exp_x = np.exp(i)
        ls.append(exp_x / np.sum(exp_x))
    return ls

# prompt: create a cross entropy loss function
def cross_entropy(y_pred, y_true):
    return -np.sum(y_true * np.log(y_pred))

# prompt: create a function that performs backpropagation algorithm to update the weights of the neural network

def backprop(model, X, y, learning_rate, niter):
    loss = []
    for i in range(niter):
        store = forward_pass(model, X)

        # Calculate the gradient of the output layer
        grad_y = store["y"] - y

        # Calculate the gradient of the hidden layer
        grad_w2 = np.dot(store["a1"].T, grad_y)
        grad_a1 = np.dot(grad_y, model["w2"].T)

        # Calculate the gradient of the input layer
        grad_w1 = np.dot(X.T, grad_a1)

        #ensure that the shape is consistent
        assert(grad_w2.shape == model["w2"].shape)
        assert(grad_w1.shape == model["w1"].shape)

        # Update the weights
        model["w1"] -= learning_rate * grad_w1
        model["w2"] -= learning_rate * grad_w2

        loss.append(cross_entropy(store["y"],y))

    return loss

def plot_loss(model, X, y, learning_rate, niter):
  loss = backprop(model, X, y, learning_rate, niter)
  plt.plot(loss)
  plt.xlabel("Iteration")
  plt.ylabel("Loss")
  plt.show()

# prompt: define a function get_embedding to input a word through a function and receive as output the embedding vector for that given word

def get_embedding(model, word):
  """
  Get the embedding vector for a given word.

  Args:
    model: The trained model.
    word: The word to get the embedding vector for.

  Returns:
    The embedding vector for the given word.
  """
  try:
      index = word_to_id[word]
  except KeyError:
      print("`word` not in corpus")

  # Get the one-hot encoding of the word.
  one_hot = one_hot_encode(index, len(word_to_id))

  # Perform the forward pass to get the embedding vector.
  embedding = forward_pass(model, one_hot)["a1"]

  return embedding

"""# EXAMPLE 1"""

text= '''Procrastination, often viewed as the thief of time, is a universal human tendency characterized by delaying or postponing tasks despite knowing the negative consequences. It manifests in various forms, from putting off important work assignments to avoiding mundane chores. While occasional procrastination is normal, chronic procrastination can become a significant obstacle to personal and professional growth. The allure of procrastination lies in its temporary relief from stress or discomfort, offering a momentary escape from the pressure of responsibilities. However, the price paid for this fleeting respite is often steep, resulting in missed deadlines, increased stress levels, and diminished productivity. Despite its detrimental effects, overcoming procrastination requires self-awareness, discipline, and effective time management strategies. By breaking tasks into smaller, manageable steps, setting clear goals, and cultivating a proactive mindset, individuals can gradually reduce their propensity to procrastinate and reclaim control over their time and productivity.'''

text ='''Machine learning is the study of computer algorithms that \
improve automatically through experience. It is seen as a \
subset of artificial intelligence. Machine learning algorithms \
build a mathematical model based on sample data, known as \
training data, in order to make predictions or decisions without \
being explicitly programmed to do so. Machine learning algorithms \
are used in a wide variety of applications, such as email filtering \
and computer vision, where it is difficult or infeasible to develop \
conventional algorithms to perform the needed tasks.'''

text = '''apple, banana, orange, cat, dog, phone, woman, man, king, queen'''

text = '''A cat is an animal. A dog is an animal. A king is a man. A queen is a woman.'''

token = preprocess_and_tokenize(text)

word_to_id, id_to_word = mapping(token)

X, y = generate_training_data(token, word_to_id, 3)

print(X)

model = init_network(len(word_to_id), 10)

store = forward_pass(model, X, return_store=True)

loss = backprop(model, X, y, 0.05, 2000)
print(loss)

plot_loss(model, X, y, 0.05, 2000)

apple = one_hot_encode(word_to_id["cat"], len(word_to_id))
result = forward_pass(model, [apple], return_store=False)[0]

for word in (id_to_word[id] for id in np.argsort(result)[::-1]):
    print(word)

model["w1"]

model["w2"]

get_embedding(model, "apple")

get_embedding(model, "dog")

def cosine_similarity(embedding1, embedding2):
  return np.dot (embedding1, embedding2) / (np. linalg.norm(embedding1) * np. linalg.norm(embedding2))

similarity = cosine_similarity(get_embedding (model, "cat"), get_embedding (model, "animal"))
print(similarity)

for i in id_to_word:
  print(id_to_word[i])

sim = []
for id in id_to_word:
  sim.append(cosine_similarity(get_embedding (model, i), get_embedding (model, (i+1))))