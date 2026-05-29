# Model Configuration
# This file allows you to fix prediction class order issues

import json
import os
import logging

logger = logging.getLogger(__name__)

class ModelConfig:
    """Model configuration management"""
    
    # Class order configuration
    # Change this if your model predicts classes in reverse order
    CLASS_ORDER = ['benign', 'melanoma']  # Index 0 = benign, Index 1 = melanoma
    
    # Alternative class order if model was trained differently
    # ALTERNATE_CLASS_ORDER = ['melanoma', 'benign']
    
    # If set to True, the CLASS_ORDER will be reversed for all predictions
    REVERSE_CLASS_ORDER = False
    
    # Confidence threshold for melanoma prediction
    MELANOMA_CONFIDENCE_THRESHOLD = 0.5
    
    @staticmethod
    def get_class_names():
        """Get the current class name order"""
        class_order = ModelConfig.CLASS_ORDER
        if ModelConfig.REVERSE_CLASS_ORDER:
            class_order = list(reversed(class_order))
            logger.info(f"Class order reversed: {class_order}")
        return class_order
    
    @staticmethod
    def reverse_predictions():
        """Toggle class order reversal"""
        ModelConfig.REVERSE_CLASS_ORDER = not ModelConfig.REVERSE_CLASS_ORDER
        logger.info(f"Class order reversal toggled to: {ModelConfig.REVERSE_CLASS_ORDER}")
        return ModelConfig.REVERSE_CLASS_ORDER
    
    @staticmethod
    def set_class_order(order):
        """Set custom class order"""
        if len(order) != 2:
            raise ValueError("Class order must have exactly 2 classes")
        ModelConfig.CLASS_ORDER = order
        logger.info(f"Class order set to: {order}")

# Load from environment variable if available
if 'MODEL_CLASS_ORDER' in os.environ:
    try:
        order = os.environ.get('MODEL_CLASS_ORDER', '').split(',')
        if len(order) == 2:
            ModelConfig.CLASS_ORDER = [c.strip() for c in order]
            logger.info(f"Class order loaded from environment: {ModelConfig.CLASS_ORDER}")
    except Exception as e:
        logger.warning(f"Failed to load class order from environment: {e}")

if os.environ.get('REVERSE_CLASS_ORDER', '').lower() == 'true':
    ModelConfig.REVERSE_CLASS_ORDER = True
    logger.info("Class order reversal enabled via environment variable")
