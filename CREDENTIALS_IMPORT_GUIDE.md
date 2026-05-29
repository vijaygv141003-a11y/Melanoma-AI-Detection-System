# Credentials Import Guide

## Overview
The Melanoma AI Detection System now supports bulk user credential import from CSV or JSON files directly from the login page. This feature is useful for administrators who need to create multiple user accounts at once.

## Supported Formats

### CSV Format
CSV files should have the following headers (required fields marked with *):

- `username`* - Unique username for the user
- `password`* - User's password (will be hashed automatically)
- `email`* - User's email address
- `role` - User role (patient or doctor, defaults to patient)
- `first_name` - User's first name (defaults to username if not provided)
- `last_name` - User's last name
- `age` - User's age (defaults to 25 if not provided)
- `gender` - User's gender (Male, Female, or Other, defaults to Other)
- `phone` - User's phone number

### JSON Format
JSON files can contain either a single user object or an array of user objects. Each user object should have:

Required fields:
- `username` - Unique username for the user
- `password` - User's password (will be hashed automatically)
- `email` - User's email address

Optional fields:
- `role` - User role (patient or doctor, defaults to patient)
- `first_name` - User's first name
- `last_name` - User's last name
- `age` - User's age (number, defaults to 25)
- `gender` - User's gender (Male, Female, or Other)
- `phone` - User's phone number

## Sample Files

### Sample CSV (sample_credentials.csv)
```csv
username,password,email,role,first_name,last_name,age,gender,phone
john_doe,SecurePass123,john.doe@example.com,patient,John,Doe,35,Male,+1234567890
jane_smith,Password456,jane.smith@example.com,patient,Jane,Smith,28,Female,+0987654321
dr_wilson,MedPass789,dr.wilson@hospital.com,doctor,Robert,Wilson,45,Male,+5551234567
```

### Sample JSON (sample_credentials.json)
```json
[
  {
    "username": "john_doe",
    "password": "SecurePass123",
    "email": "john.doe@example.com",
    "role": "patient",
    "first_name": "John",
    "last_name": "Doe",
    "age": 35,
    "gender": "Male",
    "phone": "+1234567890"
  },
  {
    "username": "jane_smith",
    "password": "Password456",
    "email": "jane.smith@example.com",
    "role": "patient",
    "first_name": "Jane",
    "last_name": "Smith",
    "age": 28,
    "gender": "Female",
    "phone": "+0987654321"
  }
]
```

## How to Use

1. **Prepare your file**: Create a CSV or JSON file with user credentials following the format above
2. **Go to login page**: Navigate to the login page of the application
3. **Click import button**: Click the "Import Credentials (CSV/JSON)" button
4. **Select file**: Choose your prepared file from your computer
5. **Review results**: The system will show you how many users were imported successfully and any errors

## Validation and Error Handling

The import process includes the following validations:

- **Required fields**: username, password, and email are required
- **Unique constraints**: Username and email must be unique in the system
- **Role validation**: Role must be either 'patient' or 'doctor'
- **Age validation**: Age must be a valid number between 0-120
- **Gender validation**: Gender must be Male, Female, or Other
- **Email format**: Email must be in valid format
- **Password strength**: Password should meet minimum security requirements

## Error Messages

Common error messages you might encounter:

- "Missing required fields (username, password, email)" - Ensure all required fields are present
- "Username 'xxx' already exists" - Choose a different username
- "Email 'xxx' already exists" - Use a different email address
- "Invalid file format" - Ensure your file is CSV or JSON
- "CSV parsing error" - Check your CSV file format and encoding

## Security Considerations

- Passwords are automatically hashed using the system's security mechanisms
- The import feature can be used by anyone with access to the login page
- Consider implementing additional authentication for bulk imports in production
- Imported users will need to follow the same password strength requirements as manual registration

## Best Practices

1. **Test with small batches first**: Test your import file format with a few users before large batches
2. **Use strong passwords**: Ensure imported passwords meet security requirements
3. **Validate data beforehand**: Check your data for duplicates and format issues before importing
4. **Keep records**: Maintain records of imported users for audit purposes
5. **Notify users**: Send welcome emails to imported users informing them of their accounts

## Troubleshooting

**Import fails completely**:
- Check file format (CSV/JSON)
- Ensure file encoding is UTF-8
- Verify file is not corrupted

**Some users fail to import**:
- Check for duplicate usernames or emails
- Verify all required fields are present
- Ensure data types are correct (age as number, etc.)

**Users can't login after import**:
- Verify username and password are correct
- Check if accounts were created successfully
- Ensure users are using the correct login URL

## Support

For issues with credentials import, please contact your system administrator or check the application logs for detailed error messages.