#!/usr/bin/env python3
"""
Quick start guide for training the melanoma detection model
This script helps you verify setup and start training
"""

import os
import sys
import argparse
import json
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n" + "="*60)
    print("CHECKING DEPENDENCIES")
    print("="*60)
    
    required_packages = {
        'tensorflow': 'TensorFlow',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'sklearn': 'Scikit-learn',
        'cv2': 'OpenCV',
        'PIL': 'Pillow',
        'matplotlib': 'Matplotlib'
    }
    
    missing = []
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} is NOT installed")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("\n✓ All dependencies installed!")
    return True

def check_dataset(dataset_path):
    """Check if dataset is in correct format"""
    print("\n" + "="*60)
    print("CHECKING DATASET")
    print("="*60)
    
    dataset_path = Path(dataset_path)
    
    if not dataset_path.exists():
        print(f"✗ Dataset path does not exist: {dataset_path}")
        return False
    
    print(f"✓ Dataset path exists: {dataset_path}")
    
    # Check for class directories
    classes = {}
    for class_dir in dataset_path.iterdir():
        if class_dir.is_dir():
            images = list(class_dir.glob('*.jpg')) + \
                    list(class_dir.glob('*.jpeg')) + \
                    list(class_dir.glob('*.png'))
            classes[class_dir.name] = len(images)
    
    if not classes:
        print(f"✗ No class directories found in {dataset_path}")
        print("Expected structure:")
        print("  dataset/")
        print("    ├── melanoma/")
        print("    │   ├── image1.jpg")
        print("    │   └── ...")
        print("    └── benign/")
        print("        ├── image1.jpg")
        print("        └── ...")
        return False
    
    print(f"\n✓ Found {len(classes)} classes:")
    total_images = 0
    for class_name, count in classes.items():
        print(f"  - {class_name}: {count} images")
        total_images += count
    
    if total_images == 0:
        print("✗ No images found in classes")
        return False
    
    print(f"\n✓ Total images: {total_images}")
    
    # Check for balanced dataset
    if len(classes) == 2:
        counts = list(classes.values())
        imbalance_ratio = max(counts) / min(counts)
        if imbalance_ratio > 2:
            print(f"⚠️  Dataset is imbalanced (ratio: {imbalance_ratio:.1f}:1)")
            print("   Consider collecting more images of the minority class")
        else:
            print(f"✓ Dataset is well balanced (ratio: {imbalance_ratio:.1f}:1)")
    
    return True

def check_configuration(config_path='training_config.json'):
    """Check training configuration"""
    print("\n" + "="*60)
    print("CHECKING CONFIGURATION")
    print("="*60)
    
    if not os.path.exists(config_path):
        print(f"⚠️  Config file not found: {config_path}")
        print("   Using default configuration")
        return True
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print(f"✓ Configuration file loaded")
        print(f"  - Model type: {config.get('model_type', 'custom_cnn')}")
        print(f"  - Epochs: {config.get('epochs', 50)}")
        print(f"  - Batch size: {config.get('batch_size', 32)}")
        print(f"  - Learning rate: {config.get('learning_rate', 0.001)}")
        
        return True
    except Exception as e:
        print(f"✗ Error loading configuration: {e}")
        return False

def check_directories():
    """Check if required directories exist"""
    print("\n" + "="*60)
    print("CHECKING DIRECTORIES")
    print("="*60)
    
    required_dirs = ['logs', 'model', 'model/checkpoints', 'model/history', 'model/plots']
    
    for dir_name in required_dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✓ {dir_name}/ exists")
    
    return True

def run_quick_train(dataset_path, epochs=5, batch_size=32):
    """Run a quick training session to verify everything works"""
    print("\n" + "="*60)
    print("RUNNING QUICK TRAINING")
    print("="*60)
    
    try:
        from train_pipeline import TrainingPipeline
        
        config = {
            'model_type': 'custom_cnn',
            'epochs': epochs,
            'batch_size': batch_size,
            'learning_rate': 0.001
        }
        
        print(f"\nStarting training with {epochs} epochs...")
        print(f"Dataset: {dataset_path}")
        
        pipeline = TrainingPipeline(config)
        dataset_info = pipeline.load_dataset(dataset_path)
        pipeline.build_model()
        results = pipeline.train(
            dataset_info['train_ds'],
            dataset_info['val_ds'],
            dataset_info['test_ds']
        )
        
        pipeline.save_model('model/test_model.h5')
        pipeline.save_history()
        pipeline.plot_history()
        
        print("\n✓ Quick training completed successfully!")
        print(f"Model saved to: model/test_model.h5")
        
        return True
    except Exception as e:
        print(f"\n✗ Error during quick training: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Melanoma Detection Model - Quick Start Guide',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check setup only
  python train_quick_start.py --check-only

  # Run full setup and quick training
  python train_quick_start.py --dataset /path/to/dataset --train

  # Run quick training with 10 epochs
  python train_quick_start.py --dataset /path/to/dataset --train --epochs 10
        """
    )
    
    parser.add_argument('--dataset', type=str, default=None,
                       help='Path to dataset directory')
    parser.add_argument('--check-only', action='store_true',
                       help='Only check setup, do not train')
    parser.add_argument('--train', action='store_true',
                       help='Run quick training after setup check')
    parser.add_argument('--epochs', type=int, default=5,
                       help='Number of epochs for quick training')
    parser.add_argument('--batch-size', type=int, default=32,
                       help='Batch size for training')
    
    args = parser.parse_args()
    
    print("\n" + "█"*60)
    print("█  MELANOMA DETECTION MODEL - QUICK START GUIDE  █")
    print("█"*60)
    
    # Always check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again.")
        sys.exit(1)
    
    # Check directories
    check_directories()
    
    # Check configuration
    check_configuration()
    
    # Check dataset if provided
    if args.dataset:
        if not check_dataset(args.dataset):
            print("\n❌ Dataset check failed. Please fix dataset structure and try again.")
            sys.exit(1)
        
        # Run quick training if requested
        if args.train:
            if not run_quick_train(args.dataset, args.epochs, args.batch_size):
                print("\n❌ Training failed.")
                sys.exit(1)
    else:
        if not args.check_only:
            print("\n⚠️  No dataset provided. Use --dataset to specify dataset path.")
            print("   Or use --check-only to just verify setup.")
    
    # Print next steps
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    
    if args.train:
        print("""
✓ Setup verified and quick training completed!

For full training:
  python train_pipeline.py \\
    --dataset /path/to/dataset \\
    --epochs 100 \\
    --batch-size 32

Or via web interface:
  1. python app.py
  2. Login as admin
  3. Visit http://localhost:5000/training/dashboard
        """)
    else:
        print("""
✓ Setup verified!

To train your model:

Option 1 - Command Line (Recommended):
  python train_pipeline.py \\
    --dataset /path/to/dataset \\
    --epochs 50 \\
    --batch-size 32

Option 2 - Web Interface:
  1. python app.py
  2. Login as admin
  3. Visit http://localhost:5000/training/dashboard

Option 3 - Python Script:
  See TRAINING_GUIDE.md for examples
        """)
    
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
