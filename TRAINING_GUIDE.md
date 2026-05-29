# Model Training Guide

This guide explains how to train the melanoma detection model in your project.

## Overview

The training system includes:
- **Data Loader** (`ai_models/data_loader.py`): Loads and prepares data from a directory structure
- **Training Pipeline** (`train_pipeline.py`): Complete training workflow with model building, training, and evaluation
- **Training Routes** (`routes/training_routes.py`): Flask API endpoints for training via the web interface
- **Configuration** (`training_config.json`): Training hyperparameters and settings

## Dataset Structure

Your dataset should be organized in the following directory structure:

```
dataset/
├── melanoma/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ... (more melanoma images)
└── benign/
    ├── image1.jpg
    ├── image2.jpg
    └── ... (more benign images)
```

**Supported image formats:** JPG, JPEG, PNG

## Training Methods

### Method 1: Command Line Interface (Recommended for Full Training)

Train the model from the command line with maximum control:

```bash
python train_pipeline.py \
    --dataset /path/to/dataset \
    --model-type custom_cnn \
    --epochs 50 \
    --batch-size 32 \
    --learning-rate 0.001 \
    --output-model model/melanoma_model.h5
```

#### Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--dataset` | str | **Required** | Path to dataset directory |
| `--model-type` | str | `custom_cnn` | Model type: `custom_cnn` or `efficientnet` |
| `--epochs` | int | 50 | Number of training epochs |
| `--batch-size` | int | 32 | Batch size for training |
| `--learning-rate` | float | 0.001 | Learning rate for optimizer |
| `--output-model` | str | `model/melanoma_model.h5` | Path to save trained model |
| `--config` | str | None | Path to config JSON file |

#### Example Commands

**Quick test training (10 epochs):**
```bash
python train_pipeline.py \
    --dataset ./data/melanoma_images \
    --epochs 10 \
    --batch-size 16
```

**Production training with full epochs:**
```bash
python train_pipeline.py \
    --dataset ./data/melanoma_images \
    --model-type custom_cnn \
    --epochs 100 \
    --batch-size 32 \
    --learning-rate 0.0005
```

**Using custom configuration file:**
```bash
python train_pipeline.py \
    --dataset ./data/melanoma_images \
    --config custom_training_config.json
```

### Method 2: Python Script

Use Python to train programmatically:

```python
from train_pipeline import TrainingPipeline
import json

# Load or create configuration
config = {
    'model_type': 'custom_cnn',
    'epochs': 50,
    'batch_size': 32,
    'learning_rate': 0.001,
    'input_shape': (224, 224, 3),
    'num_classes': 2
}

# Create pipeline
pipeline = TrainingPipeline(config)

# Load dataset
dataset_info = pipeline.load_dataset('path/to/dataset')

# Build model
pipeline.build_model(model_type='custom_cnn')

# Train model
results = pipeline.train(
    dataset_info['train_ds'],
    dataset_info['val_ds'],
    dataset_info['test_ds']
)

# Save outputs
pipeline.save_model('model/melanoma_model.h5')
pipeline.save_history()
pipeline.plot_history()

# Print summary
pipeline.print_summary()
```

### Method 3: Web Interface

Start the Flask application and access the training dashboard:

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Login to your admin account**

3. **Navigate to:** `/training/dashboard` or use the menu

4. **Fill in training parameters:**
   - Dataset path
   - Model type
   - Number of epochs
   - Batch size
   - Learning rate

5. **Click "Start Training"** and monitor progress in real-time

6. **Download outputs** after training completes:
   - Trained model (.h5)
   - Training history (.json)
   - Training plots (.png)

## Configuration

### Default Configuration (`training_config.json`)

```json
{
  "model_type": "custom_cnn",
  "input_shape": [224, 224, 3],
  "num_classes": 2,
  "epochs": 50,
  "batch_size": 32,
  "learning_rate": 0.001,
  "validation_split": 0.2,
  "test_split": 0.1,
  "optimizer": "adam",
  "loss_function": "categorical_crossentropy",
  "metrics": ["accuracy", "precision", "recall", "auc"],
  "early_stopping_patience": 10,
  "reduce_lr_patience": 5,
  "reduce_lr_factor": 0.5,
  "model_name": "melanoma_model"
}
```

### Custom Configuration

Create your own `config.json`:

```json
{
  "model_type": "custom_cnn",
  "epochs": 100,
  "batch_size": 16,
  "learning_rate": 0.0005,
  "early_stopping_patience": 15,
  "reduce_lr_patience": 8
}
```

Use it with:
```bash
python train_pipeline.py \
    --dataset ./data \
    --config custom_config.json
```

## Model Types

### Custom CNN (Recommended for beginners)

```python
pipeline.build_model('custom_cnn')
```

- **Architecture:** 4 convolutional blocks with batch normalization
- **Parameters:** ~2.5M
- **Training Time:** ~10-30 minutes (depends on dataset size)
- **Best for:** Small to medium datasets

### EfficientNet (Transfer Learning)

```python
pipeline.build_model('efficientnet')
```

- **Architecture:** Pre-trained EfficientNetB0 with custom head
- **Parameters:** ~4M
- **Training Time:** ~5-15 minutes (faster due to pre-trained weights)
- **Best for:** Limited training data, better accuracy

## Data Augmentation

The data loader automatically applies augmentation to training data:

- Random rotation (±20°)
- Random flips (horizontal and vertical)
- Random brightness adjustment
- Random contrast adjustment
- Random hue and saturation changes
- Random zoom (0.8-1.2x)

Validation and test data are **not** augmented to ensure fair evaluation.

## Training Monitoring

### Log Files

Training logs are saved in `logs/` directory:
- `training.log` - Main training log
- `tensorboard_*` - TensorBoard logs for visualization

### Training Outputs

After training completes, check `model/` directory:

```
model/
├── melanoma_model.h5          # Trained model
├── checkpoints/
│   └── best_model_*.h5        # Best checkpoint during training
├── history/
│   └── history_*.json         # Training history
└── plots/
    └── history_*.png          # Training plots (accuracy, loss, etc.)
```

### Viewing Results

**Training plots show:**
- Accuracy (train vs validation)
- Loss (train vs validation)
- Precision (train vs validation)
- AUC (train vs validation)

Open the PNG files in any image viewer to see the plots.

## Training Process

### Data Flow

1. **Load Dataset** → Images loaded from directory structure
2. **Prepare Data** → Split into train/val/test sets
3. **Preprocess** → Resize to 224×224, normalize, augment
4. **Build Model** → Create CNN architecture and compile
5. **Train** → Train for specified epochs with callbacks
6. **Evaluate** → Test on validation and test sets
7. **Save** → Save model, history, and plots

### Callbacks

During training, the following callbacks are active:

| Callback | Purpose |
|----------|---------|
| **ModelCheckpoint** | Saves best model based on validation loss |
| **EarlyStopping** | Stops training if validation loss doesn't improve |
| **ReduceLROnPlateau** | Reduces learning rate if loss plateaus |
| **TensorBoard** | Logs for visualization in TensorBoard |

## Hyperparameter Tuning

### Learning Rate

- **Too high:** Model diverges, loss becomes NaN
- **Too low:** Training is very slow
- **Recommended:** Start with 0.001, adjust if needed

```python
config['learning_rate'] = 0.0005  # Lower for small datasets
```

### Batch Size

- **Larger batches:** Faster training, less memory efficient
- **Smaller batches:** Slower training, more noise in gradients
- **Recommended:** 16-32 for most cases

```python
config['batch_size'] = 32
```

### Epochs

- **More epochs:** Better convergence, risk of overfitting
- **Fewer epochs:** Faster training, potential underfitting
- **Recommended:** Start with 50, use early stopping

```python
config['epochs'] = 50
```

### Patience Values

```python
config['early_stopping_patience'] = 10  # Stop after 10 epochs without improvement
config['reduce_lr_patience'] = 5        # Reduce LR after 5 epochs without improvement
```

## Troubleshooting

### Issue: Training is slow

**Solutions:**
- Reduce batch size (uses more GPU memory but faster)
- Use transfer learning model instead of custom CNN
- Reduce image resolution (currently 224×224)
- Use GPU: Ensure TensorFlow is configured for GPU

```bash
# Check GPU availability
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### Issue: Out of memory errors

**Solutions:**
- Reduce batch size: `--batch-size 16`
- Reduce image size in code
- Close other applications

### Issue: Model accuracy is low

**Solutions:**
- **More data:** Collect more images
- **More epochs:** Train longer with early stopping
- **Better hyperparameters:** Try different learning rates
- **Data augmentation:** Already enabled, but can be increased
- **Transfer learning:** Use EfficientNet model type

### Issue: Model is overfitting

**Solutions:**
- **More data:** Collect more diverse images
- **Data augmentation:** Already enabled with dropout
- **Reduce model complexity:** Use smaller model
- **Early stopping:** Already configured with patience=10
- **Regularization:** Add L1/L2 regularization in config

## Web Interface API

### Start Training

```bash
curl -X POST http://localhost:5000/training/api/start \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_path": "/path/to/dataset",
    "model_type": "custom_cnn",
    "config_path": "training_config.json"
  }'
```

### Get Training Status

```bash
curl http://localhost:5000/training/api/status
```

Response:
```json
{
  "in_progress": true,
  "current_epoch": 5,
  "total_epochs": 50,
  "status": "training",
  "progress": 10,
  "error": null
}
```

### Download Model

```bash
curl http://localhost:5000/training/api/download-model \
  -o melanoma_model.h5
```

### Get Training History

```bash
curl http://localhost:5000/training/api/history
```

## Performance Expectations

### With Custom CNN Model

| Dataset Size | Training Time | Expected Accuracy |
|--------------|---------------|-------------------|
| 100 images | ~5 min | 70-80% |
| 500 images | ~15 min | 80-85% |
| 1000+ images | ~30 min | 85-92% |

### With Transfer Learning (EfficientNet)

| Dataset Size | Training Time | Expected Accuracy |
|--------------|---------------|-------------------|
| 100 images | ~3 min | 80-85% |
| 500 images | ~8 min | 85-90% |
| 1000+ images | ~15 min | 90-95% |

## Best Practices

1. **Use a balanced dataset** - Similar number of melanoma and benign images
2. **Use high-quality images** - Clear, well-lit images improve model
3. **Stratified splits** - Ensures each set has similar class distribution
4. **Monitor validation loss** - Not just training loss
5. **Save checkpoints** - Best model is automatically saved
6. **Use early stopping** - Prevents overfitting
7. **Test on new data** - Validate on images not seen during training
8. **Document your setup** - Note hyperparameters used for reproducibility

## Next Steps

1. Prepare your dataset in the required directory structure
2. Choose training method (CLI, Python, or Web)
3. Run training with appropriate hyperparameters
4. Evaluate model on test set
5. Deploy trained model to production
6. Monitor model performance over time

## Support

For issues or questions:
- Check the training logs: `logs/training.log`
- Review error messages in the output
- Ensure dataset is in correct format
- Verify image files are readable

Happy training! 🎉
