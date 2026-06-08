#!/usr/bin/env python3
"""
Calculator API Test Script
Makes multiple calls to the Calculator API endpoints based on OpenAPI spec
"""

import os
import requests
import json
from typing import Dict, Any

# Configuration
HOSTNAME = os.getenv("HOST_NAME")
PORT = 3000
BASE_URL = f"http://{HOSTNAME}:{PORT}/v1"

# Test cases
test_cases = [
    {
        "name": "Calculate: 10 + 5",
        "method": "POST",
        "endpoint": "/calculate",
        "data": {
            "operand1": 10,
            "operator": "add",
            "operand2": 5
        }
    },
    {
        "name": "Calculate: 20 - 8",
        "method": "POST",
        "endpoint": "/calculate",
        "data": {
            "operand1": 20,
            "operator": "subtract",
            "operand2": 8
        }
    },
    {
        "name": "Calculate: 6 * 7",
        "method": "POST",
        "endpoint": "/calculate",
        "data": {
            "operand1": 6,
            "operator": "multiply",
            "operand2": 7
        }
    },
    {
        "name": "Calculate: 100 / 4",
        "method": "POST",
        "endpoint": "/calculate",
        "data": {
            "operand1": 100,
            "operator": "divide",
            "operand2": 4
        }
    },
    {
        "name": "Calculate: 17 % 5",
        "method": "POST",
        "endpoint": "/calculate",
        "data": {
            "operand1": 17,
            "operator": "modulo",
            "operand2": 5
        }
    },
    {
        "name": "Calculate: 2 ^ 8",
        "method": "POST",
        "endpoint": "/calculate",
        "data": {
            "operand1": 2,
            "operator": "power",
            "operand2": 8
        }
    },
    {
        "name": "Get calculation history",
        "method": "GET",
        "endpoint": "/history",
        "data": None
    },
    {
        "name": "Get history entry #1",
        "method": "GET",
        "endpoint": "/history/1",
        "data": None
    },
    {
        "name": "Update history entry #1 note",
        "method": "PUT",
        "endpoint": "/history/1",
        "data": {
            "note": "Test calculation"
        }
    },
    {
        "name": "Clear all history",
        "method": "DELETE",
        "endpoint": "/history",
        "data": None
    }
]


def make_request(method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Make an HTTP request to the API
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path
        data: Request body data (for POST/PUT)
    
    Returns:
        Response data or error information
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=5)
        else:
            return {"error": f"Unknown method: {method}"}
        
        return {
            "status_code": response.status_code,
            "response": response.json() if response.text else None,
            "success": 200 <= response.status_code < 300
        }
    except requests.exceptions.ConnectionError as e:
        return {"error": f"Connection error: {e}", "success": False}
    except requests.exceptions.Timeout:
        return {"error": "Request timeout", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}


def run_tests():
    """Run all test cases"""
    print("=" * 70)
    print(f"Calculator API Test Suite")
    print(f"Target: {BASE_URL}")
    print("=" * 70)
    print()
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"[{i}] {test['name']}")
        print(f"    Method: {test['method']} {test['endpoint']}")
        
        if test['data']:
            print(f"    Data: {json.dumps(test['data'], indent=2)}")
        
        result = make_request(test['method'], test['endpoint'], test['data'])
        results.append({
            "test_name": test['name'],
            "result": result
        })
        
        if result.get("success"):
            print(f"    ✓ Status: {result.get('status_code')}")
            if result.get("response"):
                print(f"    Response: {json.dumps(result['response'], indent=2)}")
        else:
            print(f"    ✗ Error: {result.get('error', 'Unknown error')}")
            if result.get("status_code"):
                print(f"    Status: {result.get('status_code')}")
        
        print()
    
    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    successful = sum(1 for r in results if r['result'].get('success'))
    failed = len(results) - successful
    print(f"Total tests: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()


if __name__ == "__main__":
    run_tests()
