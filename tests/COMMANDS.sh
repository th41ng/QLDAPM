#!/bin/bash
# Quick pytest commands for QLDAPM tests

# ============================================================================
# RUN ALL TESTS
# ============================================================================
pytest tests/                                    # Run all tests
pytest tests/ -v                                 # Verbose output
pytest tests/ -v --tb=short                      # Short traceback
pytest tests/ -v --tb=long                       # Long traceback
pytest tests/ -x                                 # Stop on first failure
pytest tests/ --maxfail=3                        # Stop after 3 failures

# ============================================================================
# RUN SPECIFIC FILES
# ============================================================================
pytest tests/test_security.py                    # Run security tests only
pytest tests/test_otp_service.py                 # Run OTP tests only
pytest tests/test_repositories.py                # Run repository tests only
pytest tests/test_workflows.py                   # Run workflow tests only

# ============================================================================
# RUN SPECIFIC TEST CLASS
# ============================================================================
pytest tests/test_security.py::TestPasswordHashing
pytest tests/test_otp_service.py::TestOtpServiceSend
pytest tests/test_repositories.py::TestUserRepository
pytest tests/test_storage_service.py::TestResumeFileValidation

# ============================================================================
# RUN SPECIFIC TEST
# ============================================================================
pytest tests/test_security.py::TestPasswordHashing::test_verify_password_success
pytest tests/test_otp_service.py::TestOtpServiceSend::test_send_otp_register_success
pytest tests/test_repositories.py::TestUserRepository::test_get_user_by_id_success

# ============================================================================
# COVERAGE REPORTS
# ============================================================================
pytest tests/ --cov=backend                      # Coverage report (terminal)
pytest tests/ --cov=backend --cov-report=html    # HTML report (htmlcov/)
pytest tests/ --cov=backend --cov-report=xml     # XML report (coverage.xml)
open htmlcov/index.html                          # View HTML report (macOS)

# ============================================================================
# PARALLEL EXECUTION
# ============================================================================
pytest tests/ -n 4                               # Run with 4 workers
pytest tests/ -n auto                            # Auto-detect worker count

# ============================================================================
# FILTERING BY NAME
# ============================================================================
pytest tests/ -k "test_password"                 # Run tests matching name
pytest tests/ -k "test_password or test_otp"     # Multiple filters
pytest tests/ -k "not test_deprecated"           # Exclude tests

# ============================================================================
# OUTPUT FORMATS
# ============================================================================
pytest tests/ --co                               # Show test collection only
pytest tests/ -q                                 # Quiet (minimal output)
pytest tests/ --collect-only                     # List all tests
pytest tests/ -v --setup-show                    # Show fixtures used

# ============================================================================
# DEBUGGING
# ============================================================================
pytest tests/ -s                                 # Show print output
pytest tests/ -vv                                # Very verbose
pytest tests/ --pdb                              # Start debugger on failure
pytest tests/ --trace                            # Start debugger on each test
pytest tests/ --lf                               # Run last failed tests
pytest tests/ --ff                               # Run failed tests first

# ============================================================================
# COMMON WORKFLOWS
# ============================================================================

# Test development (run one test, verbose, show prints)
pytest tests/test_security.py::TestPasswordHashing::test_verify_password_success -vv -s

# Full test run with coverage
pytest tests/ --cov=backend --cov-report=html && open htmlcov/index.html

# Run tests before committing
pytest tests/ -q && git add . && git commit -m "Add tests"

# Find slow tests
pytest tests/ --durations=10                     # Show 10 slowest tests

# Generate JUnit report (for CI/CD)
pytest tests/ --junit-xml=report.xml

# ============================================================================
# SETUP & INSTALLATION
# ============================================================================

# Install pytest
pip install pytest

# Install pytest plugins
pip install pytest-cov              # Coverage
pip install pytest-xdist            # Parallel
pip install pytest-timeout          # Timeout support
pip install pytest-html             # HTML reports

# Full install
pip install pytest pytest-cov pytest-xdist pytest-timeout pytest-html

# ============================================================================
# EXAMPLE WORKFLOWS
# ============================================================================

# Development: Test while coding
pytest tests/test_security.py -v -s --tb=short

# Before push: Full coverage check
pytest tests/ --cov=backend --cov-report=term-missing

# CI/CD Pipeline: Generate reports
pytest tests/ --cov=backend --cov-report=xml --cov-report=html --junit-xml=report.xml

# Debugging failing test
pytest tests/test_otp_service.py::TestOtpServiceSend::test_send_otp_register_success -vvs --tb=long

# Run specific feature tests in isolation
pytest tests/test_workflows.py::TestJobApplicationWorkflow -v
pytest tests/test_repositories.py::TestApplicationRepository -v

# ============================================================================
# CONFIGURATION
# ============================================================================

# pytest.ini already configured, key settings:
# - testpaths = tests/
# - python_files = test_*.py
# - python_classes = Test*
# - python_functions = test_*
# - addopts = -v (can add more here)

# Example pytest.ini content (already applied in conftest.py):
# [pytest]
# testpaths = tests
# python_files = test_*.py
# addopts = --tb=short -v
# markers =
#     slow: marks tests as slow
#     integration: marks tests as integration tests
