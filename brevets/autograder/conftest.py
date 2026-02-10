"""
Test configuration and fixtures for the Brevets Calculator

This module provides pytest fixtures that are used across all test modules:
- `flask_app`: Creates and configures a Flask application instance
- `test_client`: Provides a test client for the Flask application
- `selenium_driver`: Provides a configured Selenium WebDriver instance
- `live_server`: Starts a live server for Selenium tests

These fixtures ensure consistent test setup and teardown across all test modules.
"""

import os
import sys

# Add parent directory to Python path so we can import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket
import threading
import time
from pathlib import Path
from typing import Generator
import tempfile

import pytest
from flask import Flask
from flask_session import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from flask_brevets import BrevetsCalculator


def find_available_port() -> int:
    """Find an available port between 5005 and 5009."""
    for port in range(5005, 5010):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(("0.0.0.0", port))
                return port
        except OSError:
            continue
    raise RuntimeError("No available ports found between 5005 and 5009 (inclusive)")


@pytest.fixture(scope="session")
def flask_app() -> BrevetsCalculator:
    """Create and configure a Flask application instance."""
    config_path = Path(__file__).parent.parent / "app.ini"
    app = BrevetsCalculator(config_path)
    app.app.config["TESTING"] = True
    app.app.config["DEBUG"] = False

    # Configure session storage using simple file-based storage
    session_dir = tempfile.mkdtemp()
    app.app.config["SESSION_TYPE"] = "filesystem"
    app.app.config["SESSION_FILE_DIR"] = session_dir
    app.app.config["SESSION_FILE_THRESHOLD"] = 500
    app.app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # 1 hour
    Session(app.app)

    return app


@pytest.fixture
def test_client(flask_app: BrevetsCalculator) -> Flask.test_client:
    """Create a test client for the Flask application."""
    return flask_app.app.test_client()


@pytest.fixture
def selenium_driver() -> Generator[webdriver.Chrome, None, None]:
    """Create and configure a Selenium WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def live_server(flask_app: BrevetsCalculator) -> Generator[int, None, None]:
    """Start a live server for Selenium tests."""
    port = find_available_port()

    # Start the server in a separate thread
    server_thread = threading.Thread(
        target=flask_app.app.run,
        kwargs={"port": port, "host": "0.0.0.0", "debug": False},
        daemon=True,
    )
    server_thread.start()

    # Wait for server to start
    time.sleep(1)

    yield port

    # The daemon thread will be automatically cleaned up
