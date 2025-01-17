if [ ! "$1" ]; then
  echo "Migration Name not provided."
  exit 1
fi
alembic revision --autogenerate -m "$1"
