# Playwright Pytest Framework

This sample framework is designed to facilitate automated testing of web applications using Playwright in combination with pytest. It provides a robust structure for writing and executing tests efficiently.

## Features

- **Cross-browser Testing**: Run tests on multiple browsers including Chromium, Firefox, and WebKit.
- **Headless Mode**: Easily run tests in headless mode for CI/CD integration.
- **Event Listeners**: Attach various event listeners to capture and log console messages, requests, responses, and clicks during tests.
- **Dynamic Configuration**: Use command-line options to customize test execution without modifying the code.
- **Screenshot Capture**: Automatically capture screenshots on test failures and embed them in the HTML report.
- **Logging**: Integrated logging for better tracking of test execution.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Command Line Options](#command-line-options)

## Requirements

- Python 3.12 or higher
- Playwright
- Pytest

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dmberezovskyii/playwrite-pytest-framework.git
   cd playwrite-pytest-framework
    poetry shell
   poetry install
   ```

## Command Line Options
The framework supports several command-line options to customize the test execution:

    --env: Specify the environment (default: dev)
    --browser-type: Choose the browser type (chromium, firefox, webkit, default: chromium)
    --headless: Run tests in headless mode (default: False)
    --devtools: Open the browser with devtools (default: False)
    --proxy: Set a proxy server address (e.g., http://proxy-server:port)
    --listeners: Comma-separated list of event listeners to attach (options: console, request, response, click)
    --slow-mo: Slow down operations by the specified milliseconds (default: 0)