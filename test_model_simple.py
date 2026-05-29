import os
import sys
os.chdir('c:/Melanoma AI Detection System')
sys.path.insert(0, 'c:/Melanoma AI Detection System')

print("\n" + "="*60)
print("MODEL PREDICTION TEST")
print("="*60)

try:
    import tensorflow as tf
    from tensorflow import keras
    import numpy as np
    
    print("\n1. Loading model...")
    model = keras.models.load_model('model/melanoma_model.h5')
    print("✓ Model loaded")
    print(f"  Output shape: {model.output_shape}")
    
    print("\n2. Testing with random input...")
    test_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
    predictions = model.predict(test_input, verbose=0)
    
    pred_benign = float(predictions[0][0])
    pred_melanoma = float(predictions[0][1])
    pred_class = int(np.argmax(predictions[0]))
    
    print(f"  Benign probability:   {pred_benign:.6f}")
    print(f"  Melanoma probability: {pred_melanoma:.6f}")
    print(f"  Predicted class: {['benign', 'melanoma'][pred_class]} (index {pred_class})")
    
    # Test multiple times
    print("\n3. Testing 10 random inputs...")
    melanoma_count = 0
    benign_count = 0
    
    for i in range(10):
        test = np.random.rand(1, 224, 224, 3).astype(np.float32)
        pred = model.predict(test, verbose=0)
        cls = int(np.argmax(pred[0]))
        if cls == 0:
            benign_count += 1
        else:
            melanoma_count += 1
    
    print(f"  Benign predictions:   {benign_count}/10")
    print(f"  Melanoma predictions: {melanoma_count}/10")
    
    if benign_count == 10:
        print("\n❌ PROBLEM FOUND: Model predicts BENIGN for everything!")
        print("   This suggests the class order might be reversed.")
        print("   Try swapping classes to ['melanoma', 'benign'] in the code.")
    elif melanoma_count == 0:
        print("\n⚠️  WARNING: No melanoma predictions from random inputs")
    else:
        print("\n✓ Model appears to work correctly")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
