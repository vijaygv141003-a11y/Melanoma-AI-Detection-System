#!/usr/bin/env python
"""
Debug script to test model predictions and identify class order issues
"""
import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_model_predictions():
    """Test the model with dummy inputs"""
    model_path = 'model/melanoma_model.h5'
    
    print("=" * 80)
    print("MELANOMA AI DETECTION - MODEL DEBUG SCRIPT")
    print("=" * 80)
    
    # Check if model file exists
    if not os.path.exists(model_path):
        print(f"\n❌ ERROR: Model file not found at {model_path}")
        return False
    
    print(f"\n✓ Model file found: {model_path}")
    print(f"  File size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
    
    try:
        # Load model
        print("\n[1] Loading model...")
        model = keras.models.load_model(model_path)
        print("✓ Model loaded successfully")
        
        # Print model summary
        print("\n[2] Model Architecture:")
        print(f"  Input shape: {model.input_shape}")
        print(f"  Output shape: {model.output_shape}")
        print(f"  Total parameters: {model.count_params():,}")
        
        # Print last layer info
        print("\n[3] Output Layer Details:")
        last_layer = model.layers[-1]
        print(f"  Layer name: {last_layer.name}")
        print(f"  Layer type: {type(last_layer).__name__}")
        print(f"  Units: {last_layer.units if hasattr(last_layer, 'units') else 'N/A'}")
        print(f"  Activation: {last_layer.activation.__name__ if hasattr(last_layer, 'activation') else 'N/A'}")
        
        # Test with random inputs
        print("\n[4] Testing with random inputs...")
        test_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
        predictions = model.predict(test_input, verbose=0)
        
        print(f"  Input shape: {test_input.shape}")
        print(f"  Raw predictions: {predictions}")
        print(f"  Prediction shape: {predictions.shape}")
        
        # Interpret predictions
        class_names = ['benign', 'melanoma']
        predicted_idx = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))
        
        print(f"\n[5] Prediction Interpretation:")
        print(f"  Class probabilities: benign={predictions[0][0]:.4f}, melanoma={predictions[0][1]:.4f}")
        print(f"  Predicted class: {class_names[predicted_idx]} (index {predicted_idx})")
        print(f"  Confidence: {confidence:.4f}")
        
        # Test with all-zero input
        print("\n[6] Testing with all-zero input (edge case)...")
        zero_input = np.zeros((1, 224, 224, 3), dtype=np.float32)
        zero_predictions = model.predict(zero_input, verbose=0)
        
        zero_idx = int(np.argmax(zero_predictions[0]))
        zero_conf = float(np.max(zero_predictions[0]))
        
        print(f"  Class probabilities: benign={zero_predictions[0][0]:.4f}, melanoma={zero_predictions[0][1]:.4f}")
        print(f"  Predicted class: {class_names[zero_idx]} (index {zero_idx})")
        print(f"  Confidence: {zero_conf:.4f}")
        
        # Test with all-ones input
        print("\n[7] Testing with all-ones input (edge case)...")
        ones_input = np.ones((1, 224, 224, 3), dtype=np.float32)
        ones_predictions = model.predict(ones_input, verbose=0)
        
        ones_idx = int(np.argmax(ones_predictions[0]))
        ones_conf = float(np.max(ones_predictions[0]))
        
        print(f"  Class probabilities: benign={ones_predictions[0][0]:.4f}, melanoma={ones_predictions[0][1]:.4f}")
        print(f"  Predicted class: {class_names[ones_idx]} (index {ones_idx})")
        print(f"  Confidence: {ones_conf:.4f}")
        
        # Summary
        print("\n" + "=" * 80)
        print("DIAGNOSIS:")
        print("=" * 80)
        
        if predicted_idx == 0 and zero_idx == 0 and ones_idx == 0:
            print("⚠️  WARNING: Model always predicts BENIGN (index 0)")
            print("\nPossible causes:")
            print("1. Model class order might be REVERSED in the saved weights")
            print("   (i.e., trained with melanoma=0, benign=1, but code assumes benign=0)")
            print("2. Model might be biased/undertrained for melanoma detection")
            print("3. Model input preprocessing mismatch")
            print("\nRECOMMENDED FIX:")
            print("Try swapping the class names to ['melanoma', 'benign'] in prediction_routes.py")
        else:
            print("✓ Model appears to be working correctly")
            print("  (Making predictions for both classes)")
        
        print("\n" + "=" * 80)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR loading/testing model: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_model_predictions()
    sys.exit(0 if success else 1)
