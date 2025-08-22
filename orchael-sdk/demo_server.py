#!/usr/bin/env python3
"""
Demo script for the Orchael SDK FastAPI server
"""

import time
import requests
import subprocess
import sys
from pathlib import Path


def start_server(config_file: str = "example_config.yaml") -> subprocess.Popen[bytes]:
    """Start the server in a subprocess"""
    print(f"Starting server with config: {config_file}")

    # Check if config file exists
    if not Path(config_file).exists():
        print(f"Error: Config file {config_file} not found")
        print("Please create a config.yaml file or use the example_config.yaml")
        sys.exit(1)

    # Start server
    process = subprocess.Popen(
        [sys.executable, "-m", "orchael_sdk.server"],
        env={"ORCHAEL_CONFIG_FILE": config_file},
    )

    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)

    return process


def test_server(base_url: str = "http://localhost:8000") -> bool:
    """Test the server endpoints"""
    print(f"\nTesting server at {base_url}")

    try:
        # Test health endpoint
        print("\n1. Testing /health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print(f"✅ Health check passed: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False

        # Test chat endpoint
        print("\n2. Testing /chat endpoint...")
        chat_data = {"input": "Hello, Orchael SDK!", "history": []}
        response = requests.post(f"{base_url}/chat", json=chat_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat processing successful:")
            print(f"   Input: {result['input']}")
            print(f"   Output: {result['output']}")
        else:
            print(f"❌ Chat processing failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False

        # Test chat history endpoint
        print("\n3. Testing /chat/history endpoint...")
        response = requests.get(f"{base_url}/chat/history")
        if response.status_code == 200:
            history = response.json()
            print(f"✅ Chat history retrieved: {len(history['history'])} entries")
            for i, entry in enumerate(history["history"]):
                print(f"   {i+1}. Input: {entry['input']}")
                print(f"      Output: {entry['output']}")
        else:
            print(f"❌ Chat history failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False

        print("\n🎉 All tests passed! Server is working correctly.")
        return True

    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to server at {base_url}")
        print("Make sure the server is running and accessible")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False


def main() -> None:
    """Main demo function"""
    print("🚀 Orchael SDK FastAPI Server Demo")
    print("=" * 50)

    # Start server
    server_process = start_server()

    try:
        # Test server
        success = test_server()

        if success:
            print("\n📖 Server is running successfully!")
            print("You can now:")
            print("  - View API docs at: http://localhost:8000/docs")
            print("  - Test with curl:")
            print("    curl http://localhost:8000/health")
            print("    curl -X POST http://localhost:8000/chat \\")
            print("      -H 'Content-Type: application/json' \\")
            print('      -d \'{"input": "Hello!", "history": []}\'')
            print("\nPress Ctrl+C to stop the server")

            # Keep server running
            try:
                server_process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping server...")

    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    finally:
        # Clean up
        if server_process.poll() is None:
            print("🛑 Terminating server process...")
            server_process.terminate()
            server_process.wait()
        print("✅ Demo completed")


if __name__ == "__main__":
    main()
