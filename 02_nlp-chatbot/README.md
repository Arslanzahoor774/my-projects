# 🤖 NLP Chatbot — PyTorch Neural Network

A conversational AI chatbot built from scratch using Natural Language Processing and a custom-trained neural network in PyTorch.

## 💡 How It Works
1. User types a message
2. Message is tokenized and converted to a bag-of-words vector
3. Trained neural network predicts the intent
4. If confidence > 75%, a relevant response is returned
5. Otherwise, the bot admits it doesn't understand

## 📁 Project Files
| File | Description |
|------|-------------|
| `chat.py` | Main chatbot — loads model and runs conversation loop |
| `model.py` | Neural network architecture (3-layer feedforward) |
| `NLTKFinal.py` | Training script — trains the model on intents data |
| `nltk_utils.py` | NLP utilities — tokenizer and bag-of-words functions |
| `intents.json` | Training data — all intents, patterns, and responses |

## 🏗️ Model Architecture
- 3-layer fully connected neural network
- ReLU activation
- Softmax output with confidence thresholding

## 🛠️ Tech Stack
- Python 3.x
- PyTorch
- NLTK
- NumPy

## ⚙️ How to Run

### 1. Install dependencies
```bash
pip install torch nltk numpy
```

### 2. Train the model
```bash
python NLTKFinal.py
```
This generates `data.pth` — the trained model file.

### 3. Start chatting
```bash
python chat.py
```
Type your message and press Enter. Type `quit` to exit.

## 🎯 Key Concepts Demonstrated
- Natural Language Processing (NLP)
- Intent classification
- Neural network design and training from scratch
- Bag-of-words text representation
- Model serialization and loading
- Real-time inference
