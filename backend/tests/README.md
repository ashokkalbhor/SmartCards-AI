# SmartCards AI Backend Test Suite

This directory contains comprehensive tests for the SmartCards AI backend, achieving 90%+ test coverage.

## 📁 Test Structure

```
tests/
├── __init__.py
├── conftest.py                 # Pytest configuration and fixtures
├── api/                        # API endpoint tests
│   ├── test_auth.py           # Authentication tests
│   ├── test_card_master_data.py # Card data API tests
│   ├── test_edit_suggestions.py # Edit suggestions tests
│   └── test_admin.py          # Admin functionality tests
├── core/                       # Core functionality tests
│   └── test_card_templates.py # Card templates tests
├── models/                     # Model tests
│   └── test_card_master_data.py # Card data model tests
└── schemas/                    # Schema validation tests
```

## 🧪 Test Categories

### 1. Authentication Tests (`test_auth.py`)
- ✅ User registration
- ✅ User login/logout
- ✅ Token validation
- ✅ Password verification
- ✅ User role management

### 2. Card Master Data Tests (`test_card_master_data.py`)
- ✅ Card CRUD operations
- ✅ Spending categories management
- ✅ Merchant rewards management
- ✅ Card comparison functionality
- ✅ Data filtering and search

### 3. Edit Suggestions Tests (`test_edit_suggestions.py`)
- ✅ Submit edit suggestions
- ✅ Review suggestions (approve/reject)
- ✅ Cap editing functionality
- ✅ Reward rate editing
- ✅ Duplicate suggestion prevention

### 4. Admin Functionality Tests (`test_admin.py`)
- ✅ Admin dashboard statistics
- ✅ User management
- ✅ Moderator request handling
- ✅ Suggestion review workflow
- ✅ Access control validation

### 5. Core Functionality Tests (`test_card_templates.py`)
- ✅ Default spending categories
- ✅ Default merchant rewards
- ✅ Tier-based reward rates
- ✅ Popularity-based merchant ordering
- ✅ Template generation

### 6. Model Tests (`test_card_master_data.py`)
- ✅ Card model properties
- ✅ Spending category model
- ✅ Merchant reward model
- ✅ Display formatting
- ✅ Data validation

## 🚀 Running Tests

### Quick Start
```bash
cd backend
python run_tests.py
```

### Manual Test Execution
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests with coverage
pytest --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=90 -v

# Run specific test categories
pytest tests/api/test_auth.py -v
pytest tests/api/test_card_master_data.py -v
pytest tests/core/test_card_templates.py -v

# Run tests with specific markers
pytest -m "unit" -v
pytest -m "integration" -v
pytest -m "not slow" -v
```

## 📊 Coverage Reports

After running tests, coverage reports are generated in multiple formats:

- **Terminal**: Shows missing lines in terminal output
- **HTML**: Detailed report in `htmlcov/index.html`
- **XML**: Coverage data in `coverage.xml` for CI/CD

## 🎯 Test Coverage Goals

- **Overall Coverage**: ≥90%
- **API Endpoints**: 100% coverage
- **Core Functions**: 100% coverage
- **Models**: 100% coverage
- **Error Handling**: 100% coverage

## 🔧 Test Configuration

### Fixtures (`conftest.py`)
- Database setup/teardown
- Test user creation (user, admin, moderator)
- Test card data creation
- Authentication headers
- In-memory SQLite database

### Test Database
- Uses SQLite in-memory database
- Automatic cleanup between tests
- Isolated test environment

## 📝 Test Best Practices

1. **Descriptive Test Names**: Clear, descriptive test function names
2. **Arrange-Act-Assert**: Consistent test structure
3. **Isolation**: Each test is independent
4. **Fixtures**: Reusable test data and setup
5. **Coverage**: Aim for 90%+ coverage
6. **Error Cases**: Test both success and failure scenarios

## 🐛 Debugging Tests

```bash
# Run with verbose output
pytest -v -s

# Run single test
pytest tests/api/test_auth.py::TestAuth::test_register_success -v

# Run with debugger
pytest --pdb

# Show coverage for specific file
pytest --cov=app.core.card_templates --cov-report=term-missing
```

## 📈 Continuous Integration

The test suite is designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run Tests
  run: |
    cd backend
    pip install -r requirements-test.txt
    pytest --cov=app --cov-report=xml --cov-fail-under=90
```

## 🎉 Success Criteria

Tests pass when:
- ✅ All test cases pass
- ✅ Coverage ≥90%
- ✅ No critical errors
- ✅ All API endpoints tested
- ✅ All models validated
- ✅ Error handling verified 