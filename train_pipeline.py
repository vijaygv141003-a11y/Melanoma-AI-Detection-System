"""
Complete training pipeline for melanoma detection model
Handles model training, validation, and evaluation
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

from ai_models.cnn_model import MelanomaDetectionModel
from ai_models.train_model import ModelTrainer
from ai_models.data_loader import DataLoader

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TrainingPipeline:
    """Complete training pipeline for melanoma detection"""
    
    def __init__(self, config: Dict = None):
        """
        Initialize training pipeline
        
        Args:
            config: Training configuration dictionary
        """
        # Merge provided config with defaults
        default_config = self._default_config()
        if config:
            default_config.update(config)
        self.config = default_config
        
        self.model = None
        self.trainer = None
        self.data_loader = None
        self.history = None
        self.metrics = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create necessary directories
        self._create_directories()
    
    @staticmethod
    def _default_config() -> Dict:
        """Get default training configuration"""
        return {
            'model_type': 'custom_cnn',
            'input_shape': (224, 224, 3),
            'num_classes': 2,
            'epochs': 50,
            'batch_size': 32,
            'learning_rate': 0.001,
            'validation_split': 0.2,
            'test_split': 0.1,
            'optimizer': 'adam',
            'loss_function': 'categorical_crossentropy',
            'metrics': ['accuracy', 'AUC'],
            'early_stopping_patience': 10,
            'reduce_lr_patience': 5,
            'reduce_lr_factor': 0.5,
            'model_name': 'melanoma_model'
        }
    
    def _create_directories(self):
        """Create necessary directories for training"""
        os.makedirs('logs', exist_ok=True)
        os.makedirs('model', exist_ok=True)
        os.makedirs('model/checkpoints', exist_ok=True)
        os.makedirs('model/history', exist_ok=True)
        os.makedirs('model/plots', exist_ok=True)
    
    def load_dataset(self, dataset_path: str) -> Dict:
        """
        Load dataset from directory
        
        Args:
            dataset_path: Path to dataset directory
        
        Returns:
            Dictionary with dataset information
        """
        logger.info(f"Loading dataset from: {dataset_path}")
        
        self.data_loader = DataLoader(
            target_size=self.config['input_shape'][:2],
            batch_size=self.config['batch_size']
        )
        
        dataset_info = self.data_loader.load_from_directory(
            dataset_path,
            validation_split=self.config['validation_split'],
            test_split=self.config['test_split']
        )
        
        logger.info(f"Dataset loaded successfully")
        logger.info(f"  Train: {dataset_info['train_count']}")
        logger.info(f"  Val: {dataset_info['val_count']}")
        logger.info(f"  Test: {dataset_info['test_count']}")
        logger.info(f"  Classes: {dataset_info['class_names']}")
        
        return dataset_info
    
    def build_model(self, model_type: str = None) -> keras.Model:
        """
        Build the model
        
        Args:
            model_type: Type of model to build (custom_cnn, efficientnet, etc.)
        
        Returns:
            Compiled Keras model
        """
        model_type = model_type or self.config['model_type']
        input_shape = self.config['input_shape']
        num_classes = self.config['num_classes']
        
        logger.info(f"Building {model_type} model...")
        
        if model_type == 'custom_cnn':
            self.model = MelanomaDetectionModel.build_custom_cnn(
                input_shape=input_shape,
                num_classes=num_classes
            )
        elif model_type == 'efficientnet':
            self.model = MelanomaDetectionModel.build_efficientnet_model(
                input_shape=input_shape,
                num_classes=num_classes,
                pretrained=True
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Compile model
        optimizer = self._get_optimizer()
        self.model.compile(
            optimizer=optimizer,
            loss=self.config['loss_function'],
            metrics=self.config['metrics']
        )
        
        logger.info(f"Model compiled successfully")
        logger.info(f"Model summary:")
        self.model.summary(print_fn=logger.info)
        
        return self.model
    
    def _get_optimizer(self):
        """Get optimizer based on configuration"""
        optimizer_name = self.config['optimizer'].lower()
        learning_rate = self.config['learning_rate']
        
        if optimizer_name == 'adam':
            return keras.optimizers.Adam(learning_rate=learning_rate)
        elif optimizer_name == 'sgd':
            return keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.9)
        elif optimizer_name == 'rmsprop':
            return keras.optimizers.RMSprop(learning_rate=learning_rate)
        else:
            logger.warning(f"Unknown optimizer {optimizer_name}, using Adam")
            return keras.optimizers.Adam(learning_rate=learning_rate)
    
    def train(self, train_ds, val_ds, test_ds=None) -> Dict:
        """
        Train the model
        
        Args:
            train_ds: Training dataset
            val_ds: Validation dataset
            test_ds: Test dataset (optional)
        
        Returns:
            Training history and metrics
        """
        logger.info("Starting model training...")
        
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
        
        callbacks = self._get_callbacks()
        
        try:
            self.history = self.model.fit(
                train_ds,
                validation_data=val_ds,
                epochs=self.config['epochs'],
                callbacks=callbacks,
                verbose=1
            )
            
            logger.info("Training completed successfully")
            
            # Evaluate on test set if provided
            if test_ds is not None:
                logger.info("Evaluating on test set...")
                test_results = self.model.evaluate(test_ds, verbose=0)
                test_loss, *test_metrics = test_results
                
                self.metrics['test_loss'] = float(test_loss)
                for i, metric_name in enumerate(self.config['metrics']):
                    self.metrics[f'test_{metric_name}'] = float(test_metrics[i])
                
                logger.info(f"Test Loss: {test_loss:.4f}")
                for metric_name in self.config['metrics']:
                    if f'test_{metric_name}' in self.metrics:
                        logger.info(f"Test {metric_name}: {self.metrics[f'test_{metric_name}']:.4f}")
            
            return {
                'history': self.history.history,
                'metrics': self.metrics
            }
        
        except Exception as e:
            logger.error(f"Error during training: {str(e)}")
            raise
    
    def _get_callbacks(self) -> list:
        """Get training callbacks"""
        callbacks = []
        
        # Model checkpoint
        checkpoint_path = f"model/checkpoints/best_model_{self.timestamp}.h5"
        callbacks.append(keras.callbacks.ModelCheckpoint(
            checkpoint_path,
            monitor='val_loss',
            save_best_only=True,
            verbose=1
        ))
        
        # Early stopping
        callbacks.append(keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=self.config['early_stopping_patience'],
            restore_best_weights=True,
            verbose=1
        ))
        
        # Reduce learning rate on plateau
        callbacks.append(keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=self.config['reduce_lr_factor'],
            patience=self.config['reduce_lr_patience'],
            min_lr=1e-7,
            verbose=1
        ))
        
        # Tensorboard logging
        log_dir = f"logs/tensorboard_{self.timestamp}"
        callbacks.append(keras.callbacks.TensorBoard(
            log_dir=log_dir,
            histogram_freq=1
        ))
        
        return callbacks
    
    def save_model(self, save_path: str = None) -> str:
        """
        Save trained model
        
        Args:
            save_path: Path to save model (default: model/melanoma_model.h5)
        
        Returns:
            Path where model was saved
        """
        if self.model is None:
            raise ValueError("No model to save. Train model first.")
        
        save_path = save_path or f"model/{self.config['model_name']}.h5"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        logger.info(f"Saving model to: {save_path}")
        self.model.save(save_path)
        logger.info(f"Model saved successfully")
        
        return save_path
    
    def save_history(self, save_path: str = None) -> str:
        """
        Save training history to JSON
        
        Args:
            save_path: Path to save history
        
        Returns:
            Path where history was saved
        """
        if self.history is None:
            logger.warning("No training history to save")
            return None
        
        save_path = save_path or f"model/history/history_{self.timestamp}.json"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Convert numpy types to Python types for JSON serialization
        history_dict = {}
        for key, values in self.history.history.items():
            history_dict[key] = [float(v) for v in values]
        
        # Add metrics
        history_dict['metrics'] = self.metrics
        
        with open(save_path, 'w') as f:
            json.dump(history_dict, f, indent=2)
        
        logger.info(f"Training history saved to: {save_path}")
        return save_path
    
    def plot_history(self, save_path: str = None) -> str:
        """
        Plot training history
        
        Args:
            save_path: Path to save plot
        
        Returns:
            Path where plot was saved
        """
        if self.history is None:
            logger.warning("No training history to plot")
            return None
        
        save_path = save_path or f"model/plots/history_{self.timestamp}.png"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot accuracy
        axes[0, 0].plot(self.history.history['accuracy'])
        axes[0, 0].plot(self.history.history['val_accuracy'])
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend(['Train', 'Val'])
        axes[0, 0].grid(True)
        
        # Plot loss
        axes[0, 1].plot(self.history.history['loss'])
        axes[0, 1].plot(self.history.history['val_loss'])
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend(['Train', 'Val'])
        axes[0, 1].grid(True)
        
        # Plot precision if available
        if 'precision' in self.history.history:
            axes[1, 0].plot(self.history.history['precision'])
            axes[1, 0].plot(self.history.history['val_precision'])
            axes[1, 0].set_title('Model Precision')
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('Precision')
            axes[1, 0].legend(['Train', 'Val'])
            axes[1, 0].grid(True)
        
        # Plot AUC if available
        if 'auc' in self.history.history:
            axes[1, 1].plot(self.history.history['auc'])
            axes[1, 1].plot(self.history.history['val_auc'])
            axes[1, 1].set_title('Model AUC')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('AUC')
            axes[1, 1].legend(['Train', 'Val'])
            axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        logger.info(f"Training plot saved to: {save_path}")
        plt.close()
        
        return save_path
    
    def print_summary(self):
        """Print training summary"""
        logger.info("\n" + "="*60)
        logger.info("TRAINING SUMMARY")
        logger.info("="*60)
        logger.info(f"Model type: {self.config['model_type']}")
        logger.info(f"Epochs: {self.config['epochs']}")
        logger.info(f"Batch size: {self.config['batch_size']}")
        logger.info(f"Learning rate: {self.config['learning_rate']}")
        
        if self.history:
            logger.info(f"\nFinal training accuracy: {self.history.history['accuracy'][-1]:.4f}")
            logger.info(f"Final validation accuracy: {self.history.history['val_accuracy'][-1]:.4f}")
            logger.info(f"Final training loss: {self.history.history['loss'][-1]:.4f}")
            logger.info(f"Final validation loss: {self.history.history['val_loss'][-1]:.4f}")
        
        if self.metrics:
            logger.info("\nTest Metrics:")
            for metric_name, value in self.metrics.items():
                logger.info(f"  {metric_name}: {value:.4f}")
        
        logger.info("="*60 + "\n")


def main():
    """Main training entry point"""
    parser = argparse.ArgumentParser(description='Train melanoma detection model')
    parser.add_argument('--dataset', type=str, required=True,
                       help='Path to dataset directory')
    parser.add_argument('--model-type', type=str, default='custom_cnn',
                       choices=['custom_cnn', 'efficientnet'],
                       help='Type of model to train')
    parser.add_argument('--epochs', type=int, default=50,
                       help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=32,
                       help='Batch size for training')
    parser.add_argument('--learning-rate', type=float, default=0.001,
                       help='Learning rate for optimizer')
    parser.add_argument('--output-model', type=str, default='model/melanoma_model.h5',
                       help='Path to save trained model')
    parser.add_argument('--config', type=str, default=None,
                       help='Path to config JSON file')
    
    args = parser.parse_args()
    
    # Load config
    config = None
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        config = TrainingPipeline._default_config()
        config['model_type'] = args.model_type
        config['epochs'] = args.epochs
        config['batch_size'] = args.batch_size
        config['learning_rate'] = args.learning_rate
    
    # Create pipeline
    pipeline = TrainingPipeline(config)
    
    # Load dataset
    dataset_info = pipeline.load_dataset(args.dataset)
    
    # Build model
    pipeline.build_model(args.model_type)
    
    # Train model
    results = pipeline.train(
        dataset_info['train_ds'],
        dataset_info['val_ds'],
        dataset_info['test_ds']
    )
    
    # Save outputs
    pipeline.save_model(args.output_model)
    pipeline.save_history()
    pipeline.plot_history()
    
    # Print summary
    pipeline.print_summary()


if __name__ == '__main__':
    main()
