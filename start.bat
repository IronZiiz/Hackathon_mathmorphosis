@echo off
pip install uv

uv sync

uv run streamlit run app.py