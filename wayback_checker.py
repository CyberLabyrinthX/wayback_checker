import requests
import argparse
import os

def get_archived_urls(base_url):
    wayback_url = f"http://archive.org/wayback/available?url={base_url}"
    response = requests.get(wayback_url)

    if response.status_code == 200:
        data = response.json()
        if 'archived_snapshots' in data and data['archived_snapshots']:
            return data['archived_snapshots']
        else:
            return None
    elif response.status_code == 404:
        print("Error: The requested URL does not exist.")
    elif response.status_code == 403:
        print("Error: Access to the Wayback Machine is forbidden.")
    else:
        print(f"Error fetching data: {response.status_code}")
    return None

def save_to_file(base_url, archived_info, output_file):
    with open(output_file, 'w') as f:
        f.write(f"Archived URLs for {base_url}:\n")
        for snapshot in archived_info.values():
            f.write(f"URL: {snapshot['url']}\n")
            f.write(f"Timestamp: {snapshot['timestamp']}\n\n")
    print(f"Results saved to {output_file}")

def print_archived_info(base_url, output_file):
    archived_info = get_archived_urls(base_url)

    if archived_info:
        print(f"Archived URLs for {base_url}:")
        for snapshot in archived_info.values():
            print(f"URL: {snapshot['url']}")
            print(f"Timestamp: {snapshot['timestamp']}\n")
        save_to_file(base_url, archived_info, output_file)
    else:
        print(f"No archived versions found for {base_url}.")

def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL format. Please include 'http://' or 'https://'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check archived URLs in the Wayback Machine.')
    parser.add_argument('url', type=str, help='The URL to check for archives.')
    parser.add_argument('-o', '--output', type=str, default='output.txt', help='Output file to save results.')

    args = parser.parse_args()
    
    try:
        validate_url(args.url)
        print_archived_info(args.url, args.output)
    except ValueError as e:
        print(e)

