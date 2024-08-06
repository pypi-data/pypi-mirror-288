# FlexiAI

[![CI](https://github.com/SavinRazvan/flexiai/actions/workflows/workflow.yml/badge.svg)](https://github.com/SavinRazvan/flexiai/actions/workflows/workflow.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-000000.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/flexiai.svg?v=1.1)](https://badge.fury.io/py/flexiai)
[![Python Versions](https://img.shields.io/pypi/pyversions/flexiai.svg)](https://pypi.org/project/flexiai/)
[![Dependencies](https://img.shields.io/librariesio/github/SavinRazvan/flexiai)](https://libraries.io/github/SavinRazvan/flexiai)
[![Downloads](https://static.pepy.tech/badge/flexiai)](https://pepy.tech/project/flexiai)

FlexiAI is a dynamic and modular AI framework designed to leverage the power of Multi-Agent Systems and Retrieval Augmented Generation (RAG). This framework is ideal for developers seeking to integrate AI capabilities into their applications with ease and flexibility. With FlexiAI, you can harness the power of both OpenAI and Azure OpenAI services to create intelligent agents that can manage tasks, process data, and provide advanced AI-driven solutions.

## Introduction Video

Learn more about FlexiAI by watching the following introductory video:

[![Watch the video](https://img.youtube.com/vi/KveLqPBLhUE/0.jpg)](https://www.youtube.com/watch?v=uQLy4N-I_NQ)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Documentation](#documentation)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Flexible AI Management**: Central hub for managing AI operations including:
  - **Thread Management**: Handle and organize multiple threads of conversation.
  - **Message Management**: Manage messages within threads.
  - **Run Management**: Create and monitor runs for processing tasks.
  - **Session Management**: Maintain user sessions for continuity.
  - **Vector Store Management**: Manage vector stores for embedding and retrieval.
  - **Image Generation**: Create and manipulate images using AI models.
  - **Audio Management**: Advanced audio handling including:
    - Speech-to-Text
    - Text-to-Speech
    - Audio Transcription
    - Audio Translation
  - **Embedding Management**: Handle text embeddings for various NLP tasks.
  - **Multi-Agent System**: Manage multiple AI agents concurrently to handle various tasks efficiently.
- **Retrieval Augmented Generation (RAG)**: Enhance the AI's capabilities by integrating retrieval mechanisms to provide enriched and contextually relevant responses.
  - **Comprehensive Task Management**: Organize, execute, and manage a variety of tasks with the integrated `TaskManager`, enabling AI assistants to take actions and retrieve real-time data from your personal computer or cloud services.
- **Flexible Credential Management**: Seamlessly switch between OpenAI and Azure OpenAI credentials.
- **Extensible Architecture**: Easily extend and customize the framework with user-defined functions and tasks.
- **Robust Logging**: Comprehensive logging for effective debugging and monitoring.
- **Secure and Scalable**: Suitable for both small projects and large enterprise applications.
- **Actively Maintained**: Continuously improved and supported by the project's developer.
- **Parallel Execution**: Execute tasks and tool calls in parallel for improved performance.

## Installation

For setting up starter files and detailed installation instructions, please refer to the [Installation](docs/setup.md#table-of-contents).

## Documentation

The FlexiAI framework comes with comprehensive documentation to help you get started and make the most out of its capabilities:

- [Setup Guide](docs/setup.md)
- [Project Mapping](docs/project_mapping.md)
- [API Reference](docs/api_reference.md)
- [Usage Guide](docs/usage.md)
- [Contributing Guide](docs/contributing.md)

## Examples

- ### Basic Flask App

FlexiAI includes a basic Flask application to demonstrate how to integrate the framework with a web server. This app provides endpoints for managing threads, messages, and sessions.

- ### CLI Basic Chat

The framework also includes a basic CLI chat example, which shows how to create a simple command-line interface for interacting with AI assistants.

## Contributing

We welcome contributions from the community. If you want to contribute to FlexiAI, please read our [Contributing Guide](docs/contributing.md) to get started.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.

## Contact

For any inquiries or support, please contact Savin Ionut Razvan at [razvan.i.savin@gmail.com](mailto:razvan.i.savin@gmail.com).
