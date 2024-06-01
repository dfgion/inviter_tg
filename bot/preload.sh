#!/bin/bash

alembic revision --autogenerate -m "Database creation" &&
alembic upgrade head &&
echo "migrations have been applied"
python insert.py &&
echo "Basic data inserted"
python main.py