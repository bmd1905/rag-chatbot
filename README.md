# RAG Chatbot

[![build status](https://github.com/bmd1905/rag-chatbot/actions/workflows/test.yml/badge.svg)](https://github.com/bmd1905/rag-chatbot/actions/workflows/test.yml) [![codecov](https://codecov.io/github/bmd1905/rag-chatbot/graph/badge.svg?token=5MTJSYWD05)](https://codecov.io/github/bmd1905/rag-chatbot) [![Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fbmd1905%2Frag-chatbot%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)](https://github.com/bmd1905/rag-chatbot/blob/main/pyproject.toml)
[![GitHub License](https://img.shields.io/github/license/bmd1905/rag-chatbot)](https://github.com/bmd1905/rag-chatbot/blob/main/LICENSE)

## Overview

This project is a chatbot that uses a RAG (Retrieval-Augmented Generation) model to answer questions about a given context.


## Installation

Make sure have uv installed. If not, you can find it [here](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv sync
```

Install the pre-commit hooks.

```bash
uv run pre-commit install
```

Run the tests.

```bash
uv run pytest
```

Run the tests and generate a coverage report.

```bash
uv run pytest --cov=backend --cov-report=xml
```

## Usage

Checkout the Makefile for more information.
