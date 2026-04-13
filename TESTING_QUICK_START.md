# Testing Quick Start

## How to Run Tests

### Prerequisites
```bash
# Install dependencies (already done)
pip install -r requirements.txt
```

### Run Auth Service Tests
```bash
# From project root: d:\QLDAPM\QLDAPM
cd d:\QLDAPM\QLDAPM

# Run all auth tests
pytest tests/test_auth_service.py -v

# Run specific test class
pytest tests/test_auth_service.py::TestLoginWithPassword -v

# Run specific test
pytest tests/test_auth_service.py::TestLoginWithPassword::test_login_success -v

# Run with coverage report
pytest tests/test_auth_service.py --cov=backend.services.auth_service --cov-report=html

# Run only unit tests
pytest tests/test_auth_service.py -m unit -v
```

## Test File Structure

### Service Layer (`backend/services/auth_service.py`)
✅ **Created** - Contains core authentication business logic:
- `login_with_password(email, password)` - Login with password
- `register_with_password(...)` - Register new user
- `update_password(user_id, old_pwd, new_pwd)` - Change password
- `update_user_profile(user_id, profile_data)` - Update profile
- `get_user_info(user_id)` - Retrieve user info
- `lock_user(user_id)` - Lock account
- `unlock_user(user_id)` - Unlock account

### Test File (`tests/test_auth_service.py`)
✅ **Created** - 27 comprehensive unit tests:
- **TestLoginWithPassword**: 6 tests
- **TestRegisterWithPassword**: 8 tests
- **TestUpdatePassword**: 4 tests
- **TestUpdateUserProfile**: 3 tests
- **TestGetUserInfo**: 2 tests
- **TestLockAndUnlockUser**: 4 tests

### Test Configuration (`tests/conftest.py`)
✅ **Created** - Fixtures and app context for testing

## Test Highlights

### ✅ All Tests Are Mocked
- No real database access
- No API calls
- No file I/O
- **Fast execution** (< 1 second)

### ✅ Easy to Understand
```python
def test_login_success(self, monkeypatch):
    """Test successful login with correct email and password."""
    # Setup: Mock user and database
    mock_user = Mock()
    monkeypatch.setattr(
        "backend.services.auth_service.get_user_by_email",
        lambda email: mock_user,
    )
    
    # Execute: Call function
    result = login_with_password("user@example.com", "password123")
    
    # Assert: Verify result
    assert result.user_id == 1
```

### ✅ Comprehensive Coverage
- ✓ Success cases (happy path)
- ✓ Failure cases (errors)
- ✓ Edge cases (email normalization, validation)
- ✓ Security concerns (admin users, locked accounts)

## Example: Run Tests

```bash
# Windows PowerShell
$env:PYTHONPATH = "d:\QLDAPM\QLDAPM"
cd d:\QLDAPM\QLDAPM
pytest tests/test_auth_service.py -v

# Or using Python
python -m pytest tests/test_auth_service.py -v
```

## Expected Output

```
tests/test_auth_service.py::TestLoginWithPassword::test_login_success PASSED
tests/test_auth_service.py::TestLoginWithPassword::test_login_user_not_found PASSED
tests/test_auth_service.py::TestLoginWithPassword::test_login_wrong_password PASSED
tests/test_auth_service.py::TestLoginWithPassword::test_login_account_locked PASSED
tests/test_auth_service.py::TestLoginWithPassword::test_login_admin_user PASSED
tests/test_auth_service.py::TestLoginWithPassword::test_login_email_normalization PASSED
tests/test_auth_service.py::TestRegisterWithPassword::test_register_success_candidate PASSED
tests/test_auth_service.py::TestRegisterWithPassword::test_register_success_recruiter PASSED
...
======================== 27 passed in 0.45s ========================
```

## File Locations

| File | Location | Purpose |
|------|----------|---------|
| **auth_service.py** | `backend/services/auth_service.py` | Core auth business logic |
| **test_auth_service.py** | `tests/test_auth_service.py` | Auth service unit tests |
| **conftest.py** | `tests/conftest.py` | Test fixtures & configuration |
| **TESTING_GUIDE.md** | `TESTING_GUIDE.md` | Comprehensive testing documentation |
| **pytest.ini** | `pytest.ini` | Pytest configuration |

## Next Steps - Other Services to Test

### 1. OTP Service (`backend/services/otp_service.py`)
```
Tests needed:
- send_otp_request() - Send OTP
- verify_otp_request() - Verify OTP code
- resend_otp_request() - Resend OTP
```

### 2. Resume/CV Service (`backend/services/cv_service.py`)
```
Tests needed:
- upload_resume() - Upload and validate
- extract_text_from_pdf() - Extract content
- extract_text_from_docx() - Extract content
- validate_file_type() - Check MIME type
- validate_file_size() - Check size
```

### 3. Matching Service (`backend/services/matching_service.py`)
```
Tests needed:
- calculate_match_score() - Score calculation
- get_recommendations() - Recommend jobs
- filter_by_salary() - Salary filtering
- filter_by_location() - Location filtering
```

### 4. Email Service (`backend/services/mail_service.py`)
```
Tests needed:
- send_otp_email() - OTP email
- send_application_email() - Application email
- send_job_alert() - Job alert email
```

### 5. Storage Service (`backend/services/storage_service.py`)
```
Tests needed:
- upload_file() - Upload to storage
- delete_file() - Delete file
- display_url() - Generate display URL
- validate_file() - Validate file
```

### 6. Statistics Service (`backend/services/statistics_service.py`)
```
Tests needed:
- get_job_statistics() - Job stats
- get_user_statistics() - User stats
- get_company_statistics() - Company stats
```

## Key Mocking Patterns Used

### Pattern 1: Mock Repository Functions
```python
monkeypatch.setattr(
    "backend.services.auth_service.get_user_by_email",
    lambda email: mock_user,
)
```

### Pattern 2: Mock Security Functions
```python
monkeypatch.setattr(
    "backend.services.auth_service.verify_password",
    lambda hash, pwd: True,
)
```

### Pattern 3: Mock Database
```python
mock_db_session = Mock()
monkeypatch.setattr(
    "backend.services.auth_service.db.session",
    mock_db_session,
)
```

### Pattern 4: Patch Model Creation
```python
with patch("backend.services.auth_service.User") as mock_user_class:
    mock_user_class.return_value = mock_user_instance
```

## Troubleshooting

### Issue: ImportError for backend module
**Solution**: Ensure tests run from project root:
```bash
cd d:\QLDAPM\QLDAPM
pytest tests/test_auth_service.py -v
```

### Issue: pytest not found
**Solution**: Install from requirements.txt:
```bash
pip install pytest==7.4.3 pytest-mock==3.12.0
```

### Issue: Fixtures not working
**Solution**: Ensure `conftest.py` is in `tests/` directory

---

**Ready to run tests!** ✅
