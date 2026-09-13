import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from transformers import BertModel, BertTokenizer
from PIL import Image
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import os

# ======================
# 1. Data Loading (Fixed)
# ======================
class FakeNewsDataset(Dataset):
    def __init__(self, csv_file, tokenizer, max_length=128):
        self.data = pd.read_csv(csv_file)
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        text = str(self.data.iloc[idx]['text'])  # Ensure text is string
        image_path = self.data.iloc[idx]['image_path']
        
        # Handle image loading with path verification
        try:
            image = Image.open(image_path).convert('RGB')
        except:
            print(f"Warning: Could not load {image_path}, using blank image")
            image = Image.new('RGB', (224, 224))
        
        label = int(self.data.iloc[idx]['label'])
        
        text_encoded = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        image = self.transform(image)
        return {
            'text': text_encoded,
            'image': image,
            'label': torch.tensor(label, dtype=torch.long)
        }

# ======================
# 2. Model Architecture (Fixed)
# ======================
class MultimodalFakeNewsDetector(nn.Module):
    def __init__(self):
        super().__init__()
        # Text branch
        self.text_encoder = BertModel.from_pretrained('bert-base-uncased')
        self.text_proj = nn.Linear(768, 256)
        
        # Image branch (simplified for dummy data)
        self.image_encoder = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(64*28*28, 256)  # Adjusted for 224x224 input
        )
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 2)
        )
        
    def forward(self, text, image):
        # Text features
        text_outputs = self.text_encoder(
            input_ids=text['input_ids'].squeeze(1),
            attention_mask=text['attention_mask'].squeeze(1)
        )
        text_features = self.text_proj(text_outputs.pooler_output)
        
        # Image features
        image_features = self.image_encoder(image)
        
        # Combined features
        combined = torch.cat([text_features, image_features], dim=1)
        return self.classifier(combined)

# ======================
# 3. Training Loop (Fixed)
# ======================
def train_model(model, train_loader, val_loader, epochs=5):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        for batch in train_loader:
            optimizer.zero_grad()
            
            text = {k: v.to(device) for k, v in batch['text'].items()}
            images = batch['image'].to(device)
            labels = batch['label'].to(device)
            
            outputs = model(text, images)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        # Validation
        val_metrics = evaluate_model(model, val_loader, device)
        print(f"Epoch {epoch+1}/{epochs} | Loss: {total_loss/len(train_loader):.4f} | "
              f"Val Acc: {val_metrics['accuracy']:.4f} | "
              f"Val F1: {val_metrics['f1']:.4f}")

# ======================
# 4. Evaluation (Fixed)
# ======================
def evaluate_model(model, dataloader, device):
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for batch in dataloader:
            text = {k: v.to(device) for k, v in batch['text'].items()}
            images = batch['image'].to(device)
            labels = batch['label'].to(device)
            
            outputs = model(text, images)
            preds = torch.argmax(outputs, dim=1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    return {
        'accuracy': accuracy_score(all_labels, all_preds),
        'precision': precision_score(all_labels, all_preds, zero_division=0),
        'recall': recall_score(all_labels, all_preds, zero_division=0),
        'f1': f1_score(all_labels, all_preds, zero_division=0)
    }

# ======================
# 5. Main Execution (Fixed Path)
# ======================
if __name__ == "__main__":
    # Initialize
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    # Verify dataset file exists
    csv_path = "fake_news_dummy.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file not found at {csv_path}. "
                             f"Please ensure 'fake_news_dummy.csv' is in the same directory.")
    
    # Create datasets
    full_dataset = FakeNewsDataset(csv_path, tokenizer)
    
    # Split train/val (80/20)
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        full_dataset, [train_size, val_size])
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=8)
    
    # Initialize and train model
    model = MultimodalFakeNewsDetector()
    print("✅ Model initialized. Starting training...")
    train_model(model, train_loader, val_loader, epochs=5)
    
    # Final evaluation
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    metrics = evaluate_model(model, val_loader, device)
    print("\n=== Final Validation Metrics ===")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1-Score:  {metrics['f1']:.4f}")