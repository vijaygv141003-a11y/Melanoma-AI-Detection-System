import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import current_user
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Load environment variables
load_dotenv()
# Import extensions from database package initializer
from database.__init__ import db, migrate, login_manager

# ADVANCED AI FEATURES AND MODULES
# ============================================================================
# Core CNN and Transfer Learning
from ai_models.cnn_model import MelanomaDetectionModel
from ai_models.transfer_learning import TransferLearningModel
from ai_models.multiclass_model import MultiClassSkinCancerModel

# Data Processing and Analysis
from ai_models.data_loader import DataLoader
from ai_models.preprocessing import ImagePreprocessor
from ai_models.batch_analysis import BatchAnalysis

# Advanced Analysis and Explainability
from ai_models.dermoscopic_analyzer import DermoscopicAnalyzer
from ai_models.abcde_analyzer import ABCDEAnalyzer
from ai_models.explainability import GradCAMExplainer, IntegratedGradientsExplainer, FeatureImportanceAnalyzer, ExplainabilityReport

# Risk Stratification and Evaluation
from ai_models.risk_stratification import RiskStratification
from ai_models.evaluate_model import ModelEvaluator
from ai_models.confidence_metrics import ConfidenceMetrics, BayesianUncertainty, CalibrationMetrics

# Model Training
from ai_models.train_model import ModelTrainer

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    config_name = config_name.strip().lower() if config_name else 'development'
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Login manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Ensure instance and upload folders exist
    os.makedirs(app.instance_path, exist_ok=True)
    upload_folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'heatmaps'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'reports'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'reports', 'pdf_reports'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'reports', 'exported_csv'), exist_ok=True)
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.prediction_routes import prediction_bp
    from routes.admin_routes import admin_bp
    from routes.analytics_routes import analytics_bp
    from routes.api_routes import api_bp
    from routes.training_routes import training_bp
    from routes.advanced_testing_routes import advanced_bp
    from routes.practice_routes import practice_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(advanced_bp)
    app.register_blueprint(practice_bp)
    
    # Main route
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('prediction.dashboard'))
        return render_template('index.html')
    
    # Infographic route
    @app.route('/infographic')
    def infographic():
        """Display system architecture infographic"""
        return render_template('infographic.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Setup logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/melanoma_app.log',
                                          maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Melanoma AI Detection System startup')
    
    return app

# User loader for flask-login
@login_manager.user_loader
def load_user(user_id):
    from database.models import User
    return User.query.get(int(user_id))

# Create application instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)