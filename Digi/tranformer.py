import pandas as pd
import numpy as np
from PIL import Image
import torch
import os

# Create a directory for dummy images
os.makedirs("dummy_images", exist_ok=True)

# Generate 100 fake/real news samples
def generate_dummy_dataset(samples=100):
    data = []
    for i in range(samples):
        # Randomly assign label (0=real, 1=fake)
        label = np.random.randint(0, 2)
        
        # Generate text
        if label == 1:  # Fake news
            text = f"BREAKING: Scientist discover {np.random.choice(['aliens', 'cure for cancer', 'time travel'])} " \
                   f"in {np.random.choice(['NASA', 'a secret lab', 'the ocean'])}. " \
                   f"{np.random.choice(['Official confirmation pending', 'Government denies', 'Photos leaked'])}"
        else:  # Real news
            text = f"New study shows {np.random.choice(['climate change', 'economic growth', 'vaccine efficacy'])} " \
                   f"{np.random.choice(['improving', 'worsening'])} " \
                   f"in {np.random.choice(['Europe', 'Asia', 'North America'])}"
        
        # Create dummy image (random noise with different patterns for real/fake)
        img_array = np.random.rand(224, 224, 3) * 255
        if label == 1:  # Add "fake" pattern
            img_array[50:70, :] = [255, 0, 0]  # Red bar
        img = Image.fromarray(img_array.astype('uint8'))
        img_path = f"dummy_images/sample_{i}.jpg"
        img.save(img_path)
        
        data.append({
            "text": text,
            "image_path": img_path,
            "label": label
        })
    
    return pd.DataFrame(data)

# Generate and save dataset
df = generate_dummy_dataset()
df.to_csv("fake_news_dummy.csv", index=False)
print("✅ Dummy dataset generated:")
print(df.head())