#!/usr/bin/env python3
"""
GitHub Stars CLI - Find most starred GitHub projects in a specific date range

Usage:
  github_stars.py [--from DATE] [--to DATE] [--count COUNT]

Options:
  --from DATE    Start date in YYYY-MM-DD format [default: 30 days ago]
  --to DATE      End date in YYYY-MM-DD format [default: today]
  --count COUNT  Number of repositories to display [default: 10]
  -h, --help     Show this help message and exit
"""

import requests
import argparse
from datetime import datetime, timedelta
import sys
import os
import json
from typing import Dict, List, Any


class GitHubAPI:
    """Client for interacting with the GitHub Search API"""
    
    BASE_URL = "https://api.github.com/search/repositories"
    
    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        # Add GitHub token if available in environment
        if "GITHUB_TOKEN" in os.environ:
            self.headers["Authorization"] = f"token {os.environ['GITHUB_TOKEN']}"
    
    def search_repositories(self, from_date: str, to_date: str, count: int, language: str = None) -> List[Dict[str, Any]]:
        """
        Search for repositories created between from_date and to_date, sorted by stars
        
        Args:
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format
            count: Number of repositories to return
            language: Optional language to filter repositories
            
        Returns:
            List of repository data
        """
        query = f"created:{from_date}..{to_date}"
        if language:
            query += f" language:{language}"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": count
        }
        
        try:
            response = requests.get(
                self.BASE_URL,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json()["items"]
        except requests.RequestException as e:
            print(f"Error: Failed to fetch data from GitHub API: {e}", file=sys.stderr)
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            sys.exit(1)


def format_repository(repo: Dict[str, Any], index: int) -> str:
    """Format repository data for display"""
    return (
        f"{index+1}. {repo['full_name']} - ⭐ {repo['stargazers_count']}\n"
        f"   Description: {repo['description'] or 'No description'}\n"
        f"   URL: {repo['html_url']}\n"
        f"   Language: {repo['language'] or 'Not specified'}\n"
    )


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Find the most starred GitHub projects in a date range"
    )
    
    # Calculate default dates
    today = datetime.now().strftime("%Y-%m-%d")
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    parser.add_argument(
        "--from", 
        dest="from_date",
        default=thirty_days_ago,
        help=f"Start date in YYYY-MM-DD format (default: {thirty_days_ago})"
    )
    parser.add_argument(
        "--to", 
        dest="to_date",
        default=today,
        help=f"End date in YYYY-MM-DD format (default: {today})"
    )
    parser.add_argument(
        "--count", 
        type=int,
        default=10,
        help="Number of repositories to display (default: 10)"
    )
    parser.add_argument(
        "--language",
        type=str,
        help="Filter repositories by programming language (e.g., Python, JavaScript)"
    )
    parser.add_argument(
        "--export",
        type=str,
        help="Export results to a JSON file (provide filename)"
    )
    
    return parser.parse_args()


def validate_date(date_str: str) -> bool:
    """Validate that a string is in YYYY-MM-DD format"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def main():
    """Main function"""
    args = parse_arguments()
    
    # Validate dates
    if not validate_date(args.from_date):
        print(f"Error: Invalid from date '{args.from_date}'. Please use YYYY-MM-DD format.", file=sys.stderr)
        sys.exit(1)
    
    if not validate_date(args.to_date):
        print(f"Error: Invalid to date '{args.to_date}'. Please use YYYY-MM-DD format.", file=sys.stderr)
        sys.exit(1)
    
    # Validate count
    if args.count <= 0:
        print("Error: Count must be greater than 0", file=sys.stderr)
        sys.exit(1)
    
    print(f"Searching for the top {args.count} GitHub repositories by stars", file=sys.stderr)
    print(f"Date range: {args.from_date} to {args.to_date}", file=sys.stderr)
    if args.language:
        print(f"Language: {args.language}", file=sys.stderr)
    print("", file=sys.stderr)
    
    # Fetch repositories
    github_api = GitHubAPI()
    repositories = github_api.search_repositories(
        args.from_date,
        args.to_date,
        args.count,
        args.language
    )
    
    # Display results
    if not repositories:
        print("No repositories found in the specified date range.")
        return
    
    print(f"Found {len(repositories)} repositories:\n")
    for i, repo in enumerate(repositories):
        print(format_repository(repo, i))
    
    # Export results if requested
    if args.export:
        export_path = args.export
        if not export_path.endswith('.json'):
            export_path += '.json'
        
        # Prepare data for export (simplify it to avoid circular references)
        export_data = []
        for repo in repositories:
            export_data.append({
                'name': repo['full_name'],
                'description': repo['description'],
                'url': repo['html_url'],
                'stars': repo['stargazers_count'],
                'language': repo['language'],
                'created_at': repo['created_at'],
                'updated_at': repo['updated_at'],
                'forks': repo['forks_count']
            })
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults exported to {export_path}")


if __name__ == "__main__":
    main()
