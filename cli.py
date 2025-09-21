#!/usr/bin/env python3
"""CLI tool for testing the FastAPI Caching Service"""

import argparse
import json
import sys
import httpx
from typing import Optional, TextIO
from pathlib import Path

class CacheCLI:
    """Command-line interface for the caching service"""
    
    def __init__(self, host: str = "http://localhost:8000"):
        self.host = host.rstrip('/')
        self.base_url = f"{self.host}/payload"
    
    def create_payload(self, list_1: list, list_2: list) -> dict:
        """Create a new payload"""
        payload_data = {
            "list_1": list_1,
            "list_2": list_2
        }
        
        try:
            with httpx.Client() as client:
                response = client.post(self.base_url, json=payload_data)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            print(f"Error creating payload: {e}", file=sys.stderr)
            sys.exit(1)
    
    def get_payload(self, payload_id: str) -> dict:
        """Retrieve a payload by ID"""
        try:
            with httpx.Client() as client:
                response = client.get(f"{self.base_url}/{payload_id}")
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            print(f"Error retrieving payload: {e}", file=sys.stderr)
            sys.exit(1)
    
    def process_input_file(self, input_file: TextIO) -> dict:
        """Process input from file or stdin"""
        try:
            content = input_file.read().strip()
            if not content:
                print("Error: Empty input", file=sys.stderr)
                sys.exit(1)
            
            data = json.loads(content)
            
            if not isinstance(data, dict):
                print("Error: Input must be a JSON object", file=sys.stderr)
                sys.exit(1)
            
            if "list_1" not in data or "list_2" not in data:
                print("Error: Input must contain 'list_1' and 'list_2' fields", file=sys.stderr)
                sys.exit(1)
            
            if not isinstance(data["list_1"], list) or not isinstance(data["list_2"], list):
                print("Error: 'list_1' and 'list_2' must be arrays", file=sys.stderr)
                sys.exit(1)
            
            if len(data["list_1"]) != len(data["list_2"]):
                print("Error: 'list_1' and 'list_2' must have the same length", file=sys.stderr)
                sys.exit(1)
            
            return data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}", file=sys.stderr)
            sys.exit(1)
    
    def write_output(self, data: dict, output_file: TextIO):
        """Write output to file or stdout"""
        json.dump(data, output_file, indent=2)
        output_file.write('\n')
    
    def run(self, args):
        """Main CLI execution"""
        # Determine input source
        if hasattr(args, 'json') and args.json:
            # Handle JSON input directly
            input_data = args.json
        elif args.input == '-':
            input_data = self.process_input_file(sys.stdin)
        else:
            with open(args.input, 'r') as f:
                input_data = self.process_input_file(f)
        
        # Determine output destination
        if args.output == '-':
            output_file = sys.stdout
        else:
            output_file = open(args.output, 'w')
        
        try:
            # Process repeat iterations
            for i in range(args.repeat):
                if args.repeat > 1:
                    print(f"--- Iteration {i + 1}/{args.repeat} ---", file=sys.stderr)
                
                # Create payload
                result = self.create_payload(input_data["list_1"], input_data["list_2"])
                payload_id = result["id"]
                
                # Retrieve payload
                payload_output = self.get_payload(payload_id)
                
                # Write output
                self.write_output(payload_output, output_file)
                
                if args.repeat > 1 and i < args.repeat - 1:
                    output_file.write('\n')
        
        finally:
            if args.output != '-':
                output_file.close()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="CLI tool for testing the FastAPI Caching Service",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test with JSON input
  cache-cli --json '{"list_1": ["hello", "world"], "list_2": ["foo", "bar"]}'
  
  # Test with input file
  cache-cli --input test_data.json --output results.json
  
  # Test with repeat iterations
  cache-cli --json '{"list_1": ["test"], "list_2": ["data"]}' --repeat 5
  
  # Test with stdin/stdout
  echo '{"list_1": ["a"], "list_2": ["b"]}' | cache-cli --input - --output -
        """
    )
    
    parser.add_argument(
        '--host',
        default='http://localhost:8000',
        help='Server URL (default: http://localhost:8000)'
    )
    
    parser.add_argument(
        '-r', '--repeat',
        type=int,
        default=1,
        help='Number of iterations (default: 1)'
    )
    
    parser.add_argument(
        '-i', '--input',
        default='-',
        help='Input file path ("-" for stdin, default: stdin)'
    )
    
    parser.add_argument(
        '-j', '--json',
        help='Input argument in JSON format (properly escaped)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='-',
        help='Output file path ("-" for stdout, default: stdout)'
    )
    
    args = parser.parse_args()
    
    # Handle JSON input
    if args.json:
        try:
            input_data = json.loads(args.json)
            if not isinstance(input_data, dict):
                print("Error: JSON input must be an object", file=sys.stderr)
                sys.exit(1)
            if "list_1" not in input_data or "list_2" not in input_data:
                print("Error: JSON input must contain 'list_1' and 'list_2' fields", file=sys.stderr)
                sys.exit(1)
            if not isinstance(input_data["list_1"], list) or not isinstance(input_data["list_2"], list):
                print("Error: 'list_1' and 'list_2' must be arrays", file=sys.stderr)
                sys.exit(1)
            if len(input_data["list_1"]) != len(input_data["list_2"]):
                print("Error: 'list_1' and 'list_2' must have the same length", file=sys.stderr)
                sys.exit(1)
            
            # Store the parsed JSON data directly
            args.json = input_data
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Validate arguments
    if args.repeat < 1:
        print("Error: Repeat count must be at least 1", file=sys.stderr)
        sys.exit(1)
    
    # Run CLI
    cli = CacheCLI(args.host)
    cli.run(args)

if __name__ == "__main__":
    main()
