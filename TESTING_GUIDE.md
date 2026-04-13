# Unit Tests - Auth Service

## Overview

Comprehensive unit tests for the **Auth Service** layer (`backend/services/auth_service.py`) covering:
- User login (password authentication)
- User registration (password)
- Password updates
- Profile management
- User account locking/unlocking

## Architecture

### Test Structure

```
tests/
├── conftest.py              # Pytest configuration & fixtures
├── test_auth_service.py     # Auth service unit tests ✓
├── test_cv_service.py       # CV service tests
├── test_matching_service.py # Matching service tests
├── test_repositories.py     # Repository tests
└── __init__.py
```

### Mocking Strategy

All tests use **mocked dependencies** - NO real database or external services:

1. **Repositories**: Mocked with `monkeypatch`
2. **Database**: Mocked `db.session` 
3. **Security**: Mocked hash/verify functions
4. **Models**: Mocked User, CandidateProfile, Company objects

## Test Coverage

### TestLoginWithPassword (6 tests)

| Test | Purpose | Status |
|------|---------|--------|
| `test_login_success` | Successful login with valid credentials | ✓ |
| `test_login_user_not_found` | Login fails when user doesn't exist | ✓ |
| `test_login_wrong_password` | Login fails with incorrect password | ✓ |
| `test_login_account_locked` | Login fails when account is locked | ✓ |
| `test_login_admin_user` | Login fails for admin users | ✓ |
| `test_login_email_normalization` | Email is normalized (lowercased/trimmed) | ✓ |

### TestRegisterWithPassword (8 tests)

| Test | Purpose | Status |
|------|---------|--------|
| `test_register_success_candidate` | Successful registration for candidate | ✓ |
| `test_register_success_recruiter` | Successful registration for recruiter | ✓ |
| `test_register_email_already_exists` | Registration fails if email exists | ✓ |
| `test_register_invalid_role` | Registration fails with invalid role | ✓ |
| `test_register_password_too_short` | Registration fails if password < 6 chars | ✓ |
| `test_register_missing_full_name` | Registration fails without full name | ✓ |
| `test_register_invalid_email` | Registration fails with invalid email | ✓ |
| `test_register_email_normalization` | Email is normalized during registration | ✓ |

### TestUpdatePassword (4 tests)

| Test | Purpose | Status |
|------|---------|--------|
| `test_update_password_success` | Successful password update | ✓ |
| `test_update_password_user_not_found` | Update fails when user not found | ✓ |
| `test_update_password_wrong_old_password` | Update fails with wrong old password | ✓ |
| `test_update_password_new_password_too_short` | Update fails if new password < 6 chars | ✓ |

### TestUpdateUserProfile (3 tests)

| Test | Purpose | Status |
|------|---------|--------|
| `test_update_profile_basic_info` | Update basic user info (name, phone) | ✓ |
| `test_update_profile_user_not_found` | Update fails when user not found | ✓ |
| `test_update_profile_candidate_details` | Update candidate profile details | ✓ |

### TestGetUserInfo (2 tests)

| Test | Purpose | Status |
|------|---------|--------|
| `test_get_user_info_success` | Successfully retrieve user information | ✓ |
| `test_get_user_info_not_found` | Get info fails when user not found | ✓ |

### TestLockAndUnlockUser (4 tests)

| Test | Purpose | Status |
|------|---------|--------|
| `test_lock_user_success` | Successfully lock user account | ✓ |
| `test_lock_user_not_found` | Lock fails when user not found | ✓ |
| `test_unlock_user_success` | Successfully unlock user account | ✓ |
| `test_unlock_user_not_found` | Unlock fails when user not found | ✓ |

**Total: 27 unit tests**

## Running Tests

### Run all auth service tests
```bash
pytest tests/test_auth_service.py -v
```

### Run specific test class
```bash
pytest tests/test_auth_service.py::TestLoginWithPassword -v
```

### Run specific test
```bash
pytest tests/test_auth_service.py::TestLoginWithPassword::test_login_success -v
```

### Run with coverage
```bash
pytest tests/test_auth_service.py --cov=backend.services.auth_service --cov-report=html
```

### Run only unit tests
```bash
pytest tests/test_auth_service.py -m unit -v
```

### Run all tests
```bash
pytest tests/ -v
```

## Test Pattern

Each test follows a consistent pattern:

### 1. Setup (Arrange)
```python
# Mock dependencies
monkeypatch.setattr(
    "backend.services.auth_service.get_user_by_email",
    lambda email: mock_user,
)

# Mock database
mock_db_session = Mock()
monkeypatch.setattr(
    "backend.services.auth_service.db.session",
    mock_db_session,
)
```

### 2. Execute (Act)
```python
result = login_with_password("user@example.com", "password123")
```

### 3. Verify (Assert)
```python
assert result.user_id == 1
assert result.email == "user@example.com"
mock_db_session.commit.assert_called_once()
```

## Naming Conventions

### Test Functions
```
test_<function_name>_<expected_behavior>

Examples:
- test_login_success
- test_login_wrong_password
- test_register_email_already_exists
```

### Test Classes
```
Test<FunctionName>

Examples:
- TestLoginWithPassword
- TestRegisterWithPassword
- TestUpdatePassword
```

## Key Testing Principles

### 1. **No Real Database**
- All database operations are mocked
- No test data persisted
- Tests run in seconds

### 2. **No External Services**
- Email sending is mocked
- File storage is mocked
- Password hashing is mocked

### 3. **Isolated Tests**
- Each test is independent
- Can run in any order
- No shared state

### 4. **Clear Failure Messages**
- Assertions match business logic errors
- Status codes are verified
- Error messages are checked

### 5. **Focused on Business Logic**
- Test service layer only
- Mock repository & external dependencies
- Verify business rules, not implementation details

## Mocking Patterns

### Mock Repository Functions
```python
monkeypatch.setattr(
    "backend.services.auth_service.get_user_by_email",
    lambda email: mock_user,
)
```

### Mock Security Functions
```python
monkeypatch.setattr(
    "backend.services.auth_service.verify_password",
    lambda hash, pwd: True,
)
```

### Mock Database Session
```python
mock_db_session = Mock()
monkeypatch.setattr(
    "backend.services.auth_service.db.session",
    mock_db_session,
)
```

### Mock Model Creation
```python
with patch("backend.services.auth_service.User") as mock_user_class:
    mock_user_class.return_value = mock_user_instance
    # Test code here
```

## Error Cases Tested

✓ User not found (404)
✓ Account locked/inactive (403)
✓ Wrong password (401)
✓ Admin user (403)
✓ Email already exists (409)
✓ Invalid role (400)
✓ Short password (400)
✓ Missing full name (400)
✓ Invalid email (400)

## Future Test Improvements

### OTP Service Tests
- `test_send_otp_request` - Send OTP for login/register
- `test_verify_otp_request` - Verify OTP code
- `test_otp_expiration` - Test OTP timeout
- `test_otp_max_attempts` - Test failed attempts limit

### Resume Service Tests
- `test_upload_resume` - Upload and validate resume
- `test_validate_file_type` - Check file type restrictions
- `test_validate_file_size` - Check file size limits

### Matching Service Tests
- `test_calculate_match_score` - Calculate job-candidate match
- `test_get_recommendations` - Get recommended jobs

### Statistics Service Tests
- `test_get_user_statistics` - User stat aggregation
- `test_get_company_statistics` - Company stat aggregation

### Storage Service Tests
- `test_upload_file` - Upload file to storage
- `test_delete_file` - Delete file from storage
- `test_validate_file` - File validation

## Configuration

### pytest.ini
```ini
[pytest]
testpaths = tests/unit
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    unit: Unit test (fast, mocked, no DB)
    integration: Integration test (requires services)

timeout = 5
```

### conftest.py
Provides:
- `app` - Flask app instance
- `app_context` - App context fixture
- `client` - Test client
- `mock_db` - Mock database
- `mock_user` - Mock user fixture
- `mock_recruiter` - Mock recruiter fixture
- `mock_admin` - Mock admin fixture
- `mock_candidate_profile` - Mock candidate profile
- `mock_company` - Mock company

## Troubleshooting

### Import Errors
```
ModuleNotFoundError: No module named 'backend'
```
**Solution**: Ensure `pytest.ini` has correct `testpaths` and run from project root:
```bash
cd /d d:\QLDAPM\QLDAPM
pytest tests/test_auth_service.py -v
```

### Monkeypatch Not Working
```
AttributeError: module has no attribute 'function'
```
**Solution**: Use correct import path with module prefix:
```python
monkeypatch.setattr(
    "backend.services.auth_service.get_user_by_email",  # Correct
    lambda email: mock_user,
)
```

### Mock Not Being Called
```
AssertionError: assert_called_once() not called
```
**Solution**: Verify the mock is patched at the right location - where it's imported, not where it's defined.

## Dependencies

Tests use:
- `pytest==7.4.3` - Test framework
- `pytest-mock==3.12.0` - Mock utilities
- `pytest-cov==4.1.0` - Coverage reporting
- `unittest.mock` - Mock objects
- `monkeypatch` - Dynamic patching

## Next Steps

1. ✅ Create Auth Service (`backend/services/auth_service.py`)
2. ✅ Write Auth Service Tests (`tests/test_auth_service.py`)
3. 📝 Continue with other services:
   - OTP Service
   - Resume Service
   - Matching Service
   - Email Service
   - Storage Service
   - Statistics Service

---

**Last Updated**: April 13, 2026
**Auth Service Version**: 1.0
**Test Coverage**: 27 tests (Auth only)
