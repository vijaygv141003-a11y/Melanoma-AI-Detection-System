"""Generate sample dataset for training"""
import os
import numpy as np
from PIL import Image

def create_sample_dataset():
    """Create sample melanoma and benign images"""
    
    # Create directory structure
    os.makedirs('sample_dataset/melanoma', exist_ok=True)
    os.makedirs('sample_dataset/benign', exist_ok=True)
    
    print("Creating sample dataset...\n")
    
    # Create sample melanoma images (darker, with simulated lesions)
    print("Melanoma images:")
    for i in range(5):
        img_array = np.random.rand(224, 224, 3)
        # Make it darker and add some pattern
        img_array = img_array * 0.4 + 0.2  # Darker base
        # Add some spots (simulated lesions)
        for _ in range(3):
            x, y = np.random.randint(50, 174, 2)
            img_array[x:x+30, y:y+30] = np.random.rand(30, 30, 3) * 0.3
        
        img = Image.fromarray((img_array * 255).astype(np.uint8))
        img.save(f'sample_dataset/melanoma/sample_melanoma_{i+1}.jpg')
        print(f"  ✓ Created melanoma image {i+1}/5")
    
    # Create sample benign images (lighter, uniform)
    print("\nBenign images:")
    for i in range(5):
        img_array = np.random.rand(224, 224, 3)
        # Make it lighter and more uniform
        img_array = img_array * 0.2 + 0.7  # Lighter base
        
        img = Image.fromarray((img_array * 255).astype(np.uint8))
        img.save(f'sample_dataset/benign/sample_benign_{i+1}.jpg')
        print(f"  ✓ Created benign image {i+1}/5")
    
    print("\n" + "="*60)
    print("✓ Sample dataset created successfully!")
    print("="*60)
    print("Location: sample_dataset/")
    print("  - melanoma/: 5 images")
    print("  - benign/: 5 images")
    print("\nReady for training!")

if __name__ == '__main__':
    create_sample_dataset()
