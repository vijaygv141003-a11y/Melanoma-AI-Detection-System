# Model Configuration & Debugging Guide

## Issue: Model Always Predicts "Benign"

If your melanoma detection model is predicting "benign" for all test cases, this guide will help you fix it.

### Root Causes

1. **Class Order Mismatch** (Most Common)
   - Your trained model might have classes in order: `['melanoma', 'benign']` (index 0 = melanoma, index 1 = benign)
   - But the code expects: `['benign', 'melanoma']` (index 0 = benign, index 1 = melanoma)
   - This causes all melanoma predictions to be labeled as benign and vice versa

2. **Placeholder Model**
   - The real trained model wasn't found, so a random untrained placeholder was created
   - This model makes random predictions that happen to favor benign

3. **Preprocessing Mismatch**
   - Images aren't being preprocessed the same way they were during model training

### How to Fix

#### Option 1: Reverse Class Order (Quick Fix)

If your model predicts melanoma as index 0 and benign as index 1:

**Method A: Edit model_config.py**
```python
# File: model_config.py

# Change this line:
REVERSE_CLASS_ORDER = False

# To:
REVERSE_CLASS_ORDER = True
```

**Method B: Set Environment Variable**
```bash
# Before running the app, set:
set REVERSE_CLASS_ORDER=true

# Then run:
python app.py
```

#### Option 2: Custom Class Order

Edit `model_config.py`:
```python
# Set custom class order
ModelConfig.CLASS_ORDER = ['melanoma', 'benign']  # Adjust as needed
```

#### Option 3: Check Model Predictions Directly

Run the test script to see what your model actually outputs:

```bash
# First, set up the environment
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Then run the test
python test_model_simple.py
```

Expected output should show predictions for both melanoma and benign classes, not always the same class.

### Verify the Fix

1. Upload a test image known to be melanoma
2. Check the prediction result
3. It should show "melanoma" with appropriate confidence
4. Repeat with benign images

### Model Architecture Details

- **Type**: EfficientNetB0 Transfer Learning
- **Input Shape**: (224, 224, 3) - RGB images
- **Output Classes**: 2 - Benign and Melanoma
- **Expected Accuracy**: ~94%+ (from model_metrics.json)

### Configuration File Locations

- **Model Config**: `model_config.py` - Controls class order and thresholds
- **Model File**: `model/melanoma_model.h5` - The trained model weights
- **Model Metadata**: `model/model_metrics.json` - Training metrics and performance data
- **Class Labels**: `model/labels.txt` - List of class names

### Advanced: Test Model Directly in Python

```python
import tensorflow as tf
import numpy as np

# Load model
model = tf.keras.models.load_model('model/melanoma_model.h5')

# Create random test input
test_input = np.random.rand(1, 224, 224, 3).astype(np.float32)

# Make prediction
predictions = model.predict(test_input, verbose=0)
print(f"Benign probability (index 0): {predictions[0][0]:.4f}")
print(f"Melanoma probability (index 1): {predictions[0][1]:.4f}")

# Get predicted class
predicted_class_idx = np.argmax(predictions[0])
print(f"Predicted class: {predicted_class_idx}")
```

### Need More Help?

If the model is still not working:
1. Verify `model/melanoma_model.h5` file exists and is not corrupted
2. Check `logs/melanoma_app.log` for error messages
3. Ensure TensorFlow/Keras versions match training environment
4. Retrain the model with your own labeled melanoma/benign images

### Related Files

- `routes/prediction_routes.py` - Main prediction logic
- `model_config.py` - Configuration for class order
- `ai_models/train_model.py` - Model training/loading code
- `ai_models/preprocessing.py` - Image preprocessing pipeline
