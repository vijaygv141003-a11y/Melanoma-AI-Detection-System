# Model Training - Quick Reference

## Files Added

### Core Training Modules
1. **`ai_models/data_loader.py`** - Data loading and preparation
2. **`train_pipeline.py`** - Complete training pipeline script
3. **`routes/training_routes.py`** - Flask API endpoints for web training
4. **`templates/training_dashboard.html`** - Web UI for training

### Configuration & Scripts
5. **`training_config.json`** - Training hyperparameter configuration
6. **`train_quick_start.py`** - Setup verification and quick training

### Documentation
7. **`TRAINING_GUIDE.md`** - Comprehensive training guide

## Quick Start Commands

### 1. Verify Setup
```bash
python train_quick_start.py --check-only
```

### 2. Quick Test (5 epochs)
```bash
python train_quick_start.py --dataset /path/to/dataset --train --epochs 5
```

### 3. Full Training (Command Line)
```bash
python train_pipeline.py \
    --dataset /path/to/dataset \
    --model-type custom_cnn \
    --epochs 50 \
    --batch-size 32 \
    --learning-rate 0.001
```

### 4. Web Interface Training
```bash
python app.py
# Then visit: http://localhost:5000/training/dashboard
```

## Expected Directory Structure

```
your_dataset/
├── melanoma/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
└── benign/
    ├── image1.jpg
    ├── image2.jpg
    └── ...
```

## Key Features

✅ **Multiple Training Methods**
- Command-line interface
- Python script API
- Web dashboard with live monitoring

✅ **Smart Data Handling**
- Automatic train/validation/test split
- Data augmentation for training data
- Stratified splitting for balanced sets
- Class imbalance handling

✅ **Advanced Training**
- Early stopping to prevent overfitting
- Learning rate reduction on plateau
- Model checkpointing (saves best model)
- Configurable hyperparameters

✅ **Comprehensive Outputs**
- Trained model (.h5)
- Training history (.json)
- Performance plots (.png)
- TensorBoard logs

✅ **Monitoring & Debugging**
- Real-time training status via web UI
- Training logs in `logs/` directory
- Performance metrics per epoch
- Error tracking and reporting

## Training Outputs Location

```
model/
├── melanoma_model.h5           # Final trained model
├── checkpoints/
│   └── best_model_*.h5         # Best checkpoint
├── history/
│   └── history_*.json          # Training history
└── plots/
    └── history_*.png           # Training plots
```

## Model Performance Expectations

| Model Type | Dataset Size | Time | Accuracy |
|-----------|--------------|------|----------|
| Custom CNN | 100 images | ~5 min | 70-80% |
| Custom CNN | 500 images | ~15 min | 80-85% |
| Custom CNN | 1000+ images | ~30 min | 85-92% |
| EfficientNet | 100 images | ~3 min | 80-85% |
| EfficientNet | 500 images | ~8 min | 85-90% |

## Hyperparameter Guide

**For Small Datasets (< 500 images):**
```json
{
  "epochs": 100,
  "batch_size": 16,
  "learning_rate": 0.0005,
  "early_stopping_patience": 15
}
```

**For Large Datasets (> 1000 images):**
```json
{
  "epochs": 50,
  "batch_size": 32,
  "learning_rate": 0.001,
  "early_stopping_patience": 10
}
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Out of memory | Reduce batch_size to 16 or 8 |
| Slow training | Use EfficientNet model or reduce epochs |
| Low accuracy | Add more data or train longer |
| Overfitting | Use more data or enable early stopping |
| Training diverges | Reduce learning_rate to 0.0001 |

## Next Steps

1. ✅ Prepare dataset in required format
2. ✅ Run `train_quick_start.py --check-only` to verify setup
3. ✅ Start training with method of choice
4. ✅ Monitor training progress
5. ✅ Download trained model when complete
6. ✅ Deploy model to production

## Support Resources

- **Full Guide:** `TRAINING_GUIDE.md`
- **Training Logs:** `logs/training.log`
- **Configuration:** `training_config.json`
- **Error Messages:** Check terminal output or logs

---

**For detailed information, see [TRAINING_GUIDE.md](TRAINING_GUIDE.md)**
