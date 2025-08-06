# PEI
# LLM Security Middleware SDK

## Overview

This project delivers a modular and configurable SDK designed to monitor and filter interactions between users and Large Language Models (LLMs), ensuring security and integrity in critical applications. Developed in partnership with **AgentifAI**, the SDK acts as a middleware layer that detects sensitive topics, malicious inputs (like prompt injections) and inappropriate outputs.

It supports both Portuguese and English, offering contextual validation, toxicity analysis and customizable topic filtering.

## Objectives

- Ensure the secure use of LLMs in high-responsibility environments
- Detect prompt injection attacks and sensitive or malicious content
- Provide configurable filters for unwanted topics or unsafe behavior
- Support multilingual analysis (Portuguese and English)
- Enable modular integration across systems and industries

## Key Features

- Real-time analysis of both input prompts and model outputs
- Detection of:
  - Prompt injection attempts
  - Toxic language
  - Sensitive or off-topic content
  - Template exposure in outputs
- Customizable filtering rules per client
- Built-in translation for multilingual input handling
- Dockerized architecture with a Flask API and Node.js demo interface

## Technologies

- Python (Flask, Transformers, NLTK, FuzzyWuzzy, Torch, SentencePiece)
- Docker
- Node.js (for UI)
- AgentifAI technical mentoring
- HuggingFace NLP models

## Usage

The SDK exposes endpoints for validating LLM prompts and outputs. It can be used in any application where secure and context-aware interaction with LLMs is required, such as customer service bots, medical assistants, or educational platforms.

## Future Work

- Development of native multilingual models (eliminating the need for translation)
- Enhanced scalability (e.g., auto-scaling with multi-GPU inference)
- Continuous threat pattern updates to handle evolving prompt attack techniques
