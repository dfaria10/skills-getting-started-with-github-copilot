# FastAPI Backend Tests

Comprehensive test suite for the Mergington High School Activities API.

## Overview

- **31 tests** organized by endpoint
- **97% code coverage** of `src/app.py`
- **Test isolation** with fixture-based state management
- **Full error path coverage** including validation and edge cases

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run with verbose output
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/test_signup.py -v
```

### Run with coverage report
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Generate HTML coverage report
```bash
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html to view results
```

## Test Organization

### `test_activities.py` (8 tests)
Tests for `GET /activities` endpoint
- Structure validation (required fields, data types)
- Participant counts and capacity limits
- Activity metadata (schedule, description)
- Empty participant lists handling

### `test_signup.py` (11 tests)
Tests for `POST /activities/{activity_name}/signup` endpoint
- Successful signup with participant tracking
- Duplicate student prevention (400 error)
- Activity validation (404 error)
- Multiple students in same activity
- Same student in multiple activities
- Parameter validation (missing/empty email)
- Response message format

### `test_unregister.py` (12 tests)
Tests for `DELETE /activities/{activity_name}/unregister` endpoint
- Successful unregistration with participant removal
- Participant count decrement
- Not registered error (400)
- Activity not found error (404)
- Isolation across multiple activities
- Double unregister prevention
- Parameter validation
- Unregistering all participants

## Fixture Reference

### `client`
FastAPI TestClient for making API requests
```python
def test_example(client):
    response = client.get("/activities")
```

### `clean_activities`
Isolated activity state reset per test (test isolation)
```python
def test_example(client, clean_activities):
    # Activities are reset to initial state
    # Changes don't affect other tests
```

### `activities_with_empty_classes`
Activities with some empty participant lists
```python
def test_example(client, activities_with_empty_classes):
    # Art Studio and Basketball Team have no participants
```

### `full_activity`
Activity at max capacity for edge case testing
```python
def test_example(client, full_activity):
    # Tennis Club is filled with 8 students (at max)
```

## Code Coverage

| File       | Coverage | Details |
|-----------|----------|---------|
| src/app.py | 97%      | All endpoints and error paths covered; line 83 (root redirect) not triggered in tests |

## Adding New Tests

1. Create a new test file: `tests/test_<feature>.py`
2. Import fixtures from conftest:
   ```python
   from tests.conftest import client, clean_activities
   ```
3. Use class-based organization for clarity:
   ```python
   class TestNewFeature:
       def test_case_one(self, client, clean_activities):
           response = client.get("/endpoint")
           assert response.status_code == 200
   ```
4. Run tests: `pytest tests/test_<feature>.py -v`

## Fixture Patterns

### Isolated State (Unit-like)
```python
def test_isolated(client, clean_activities):
    # Each test gets fresh activities
    # No cross-test pollution
```

### Shared State (Integration)
```python
def test_integration(client, activities_with_empty_classes):
    # State is preset for scenario testing
    # Still reset after test completes
```

### Custom State
```python
def test_custom(client, clean_activities):
    # Modify as needed for test
    clean_activities["Chess Club"]["participants"] = ["custom@email.com"]
```

## Known Limitations

1. **In-memory database**: Activities dict is reset per test. Real database tests would need additional setup.
2. **Email validation**: Current API doesn't validate email format or empty strings (enhancement opportunity).
3. **Capacity enforcement**: Current API doesn't prevent signup when activity is full (future improvement).
4. **Static files**: Frontend tests (HTML/CSS/JS) not included; focus is backend API.

## Continuous Improvement

Suggested enhancements:
- Add email format validation to `src/app.py`
- Add capacity limit enforcement
- Add participant name/details (currently just email)
- Refactor to use real database (SQLAlchemy, etc.) — tests will validate contracts
- Add async endpoint support
