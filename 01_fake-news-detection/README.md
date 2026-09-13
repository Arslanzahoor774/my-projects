# 🕵️ Fake News Detection — Multimodal AI System

A deep learning system that detects fake news by analyzing **both text and images simultaneously** using a multimodal architecture.

## 🧠 What Makes This Advanced
Unlike basic fake news detectors that only analyze text, this system combines:
- **BERT** (Bidirectional Encoder Representations from Transformers) for text understanding
- **CNN** (Convolutional Neural Network) for image analysis
- Both signals are **fused together** for a final real/fake classification

## 🏗️ Architecture

## 📁 Project Files
| File | Description |
|------|-------------|
| `pipeline.py` | Main model — BERT + CNN multimodal architecture, training loop, evaluation |
| `data_generator.py` | Generates dummy dataset with fake/real news samples and images |
| `fake_news_dummy.csv` | Sample dataset for testing |

## 🛠️ Tech Stack
- Python 3.x
- PyTorch
- Hugging Face Transformers (BERT)
- Torchvision
- Scikit-learn
- Pandas, NumPy, Pillow

## ⚙️ How to Run

### 1. Install dependencies
```bash
pip install torch transformers torchvision scikit-learn pandas numpy pillow
```

### 2. Generate the dataset
```bash
python data_generator.py
```

### 3. Train and evaluate the model
```bash
python pipeline.py
```

## 📊 Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1-Score

## 🎯 Key Concepts Demonstrated
- Multimodal deep learning
- Transfer learning with BERT
- CNN-based image feature extraction
- Feature fusion and classification
- Model training and evaluation pipeline
