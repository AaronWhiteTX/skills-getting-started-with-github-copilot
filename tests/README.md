# Tests for Mergington High School Activities API

This directory contains comprehensive tests for the FastAPI application.

## Test Structure

- `conftest.py` - Test configuration and fixtures
- `test_app.py` - Main application tests

## Test Categories

### 1. Main Endpoints (`TestMainEndpoints`)
- Root endpoint redirection
- Activities listing functionality

### 2. Signup Endpoint (`TestSignupEndpoint`)
- Successful signup scenarios
- Error handling (non-existent activities, duplicate signups)
- Validation of existing participants

### 3. Unregister Endpoint (`TestUnregisterEndpoint`)
- Successful unregistration
- Error handling (non-existent activities, not registered participants)
- Complete signup/unregister workflow

### 4. Data Integrity (`TestDataIntegrity`)
- Data structure validation
- Email format validation
- Multiple activity signup scenarios

## Running Tests

### Option 1: Using pytest directly
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

### Option 2: Using the test runner script
```bash
./run_tests.sh
```

## Test Coverage

The tests achieve **100% code coverage** of the main application code (`src/app.py`).

## Test Dependencies

- `pytest` - Testing framework
- `httpx` - HTTP client for testing FastAPI
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting

All dependencies are listed in `requirements.txt`.

## Fixtures

- `client` - FastAPI test client
- `reset_activities` - Resets activity data after each test
- `sample_activity_name` / `sample_email` - Test data fixtures