export PYTHONPATH=$(pwd)
pytest tests/test_public_endpoint.py
pytest tests/test_secure_endpoints.py