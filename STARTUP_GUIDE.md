# Project Startup Guide

## Quick Start Instructions

Since the shell environment is currently unavailable, please follow these manual steps to run the project:

### Option 1: Using Command Prompt

1. **Open Command Prompt** (cmd)
2. **Navigate to project directory**:
   ```cmd
   cd C:\Melanoma AI Detection System
   ```

3. **Activate virtual environment**:
   ```cmd
   .venv\Scripts\activate
   ```

4. **Install dependencies** (if not already installed):
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```cmd
   python app.py
   ```

6. **Access the application**:
   Open your browser and navigate to: `http://localhost:5000`

### Option 2: Using PowerShell

1. **Open PowerShell**
2. **Navigate to project directory**:
   ```powershell
   cd 'C:\Melanoma AI Detection System'
   ```

3. **Activate virtual environment**:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. **Install dependencies** (if needed):
   ```powershell
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```powershell
   python app.py
   ```

6. **Access the application**:
   Open your browser and navigate to: `http://localhost:5000`

### Option 3: Using the Batch Script

1. **Double-click** the `run_app.bat` file in the project directory
2. The application will start automatically
3. Access it at: `http://localhost:5000`

## What's New in This Version

### Recent Updates:
1. **Fixed Binary Classification Error**: Corrected class order reversal issue in `model_config.py`
2. **Enhanced Dashboard Statistics**: Added practice summary, confidence analysis, and activity tracking
3. **Credentials Import Feature**: Added bulk user import from CSV/JSON on login page

### New Features:
- **Practice Summary**: Comprehensive statistics on patient dashboards
- **Average Confidence Display**: Shows confidence percentages for predictions
- **Benign/Melanoma Breakdown**: Detailed statistics with percentages
- **Activity Tracking**: Recent predictions monitoring (7-day window)
- **Confidence Analysis**: High/medium/low confidence prediction breakdown
- **Bulk User Import**: Import user credentials from CSV or JSON files

## Default Login Credentials

If you need to create initial users, you can:

1. **Register manually** through the registration page
2. **Import credentials** using the new import feature on the login page
3. **Use sample files** provided:
   - `sample_credentials.csv`
   - `sample_credentials.json`

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, you can change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to available port
```

### Database Issues
If you encounter database errors, delete the database file and let it recreate:
```cmd
del instance\melanoma_detection.db
```

### Missing Dependencies
If you get import errors, reinstall dependencies:
```cmd
pip install -r requirements.txt
```

### TensorFlow Issues
If TensorFlow fails to load, ensure you have the correct Python version (3.11 or 3.12 recommended for TensorFlow 2.12).

## Development vs Production

### Development Mode (Default)
- Debug mode enabled
- Auto-reload on code changes
- Detailed error messages

### Production Mode
Set environment variable:
```cmd
set FLASK_ENV=production
python app.py
```

## Accessing Different Dashboards

Once running:
- **Patient Dashboard**: `http://localhost:5000/prediction/dashboard`
- **Doctor Dashboard**: `http://localhost:5000/prediction/doctor/dashboard`
- **Admin Dashboard**: `http://localhost:5000/admin/dashboard`
- **Login Page**: `http://localhost:5000/auth/login`

## Testing the New Features

### Test Credentials Import:
1. Go to login page
2. Click "Import Credentials (CSV/JSON)"
3. Use `sample_credentials.csv` or `sample_credentials.json`
4. Verify users are created successfully

### Test Enhanced Statistics:
1. Login as a patient or doctor
2. View the dashboard
3. Check the new practice summary section
4. Verify confidence percentages and breakdowns

### Test Fixed Predictions:
1. Upload a skin lesion image
2. Verify prediction results make clinical sense
3. Check that benign/melanoma classification is correct

## Support

For issues or questions:
- Check the logs in `logs/` directory
- Review error messages in the console
- Consult the documentation files in the project root