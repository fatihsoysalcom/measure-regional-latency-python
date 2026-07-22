import requests
import time
import sys

# Define a list of "regions" with corresponding URLs to test latency.
# These URLs are chosen to represent different geographical locations,
# though actual server locations might vary based on CDN or routing.
# The goal is to illustrate that network distance impacts response time.
REGIONAL_ENDPOINTS = {
    "Turkey (Google TR)": "https://www.google.com.tr",
    "Germany (Google DE)": "https://www.google.de",
    "United Kingdom (Google UK)": "https://www.google.co.uk",
    "United States (Google US)": "https://www.google.com",
    "Japan (Google JP)": "https://www.google.co.jp",
}

def measure_latency(url):
    """Measures the time taken to perform an HTTP GET request to a URL."""
    try:
        start_time = time.perf_counter()
        response = requests.get(url, timeout=5) # Set a timeout to prevent hanging
        end_time = time.perf_counter()
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        return (end_time - start_time) * 1000 # Return latency in milliseconds
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def main():
    print("--- Measuring Regional Latency ---")
    print("This script simulates fetching data from servers in different geographical regions.")
    print("The time taken (latency) will vary based on your current location and network path.")
    print("-" * 35)

    results = []
    for region, url in REGIONAL_ENDPOINTS.items():
        print(f"Testing {region} ({url})... ", end="")
        sys.stdout.flush() # Ensure print output is shown immediately
        latency = measure_latency(url)
        if isinstance(latency, float):
            print(f"Latency: {latency:.2f} ms")
            results.append((region, latency))
        else:
            print(latency) # Print error message
            results.append((region, float('inf'))) # Use infinity for sorting errors

    print("\n--- Latency Results (Lower is Better) ---")
    # Sort results by latency for easier comparison
    sorted_results = sorted([r for r in results if isinstance(r[1], float) and r[1] != float('inf')], key=lambda x: x[1])

    if not sorted_results:
        print("No successful latency measurements to display.")
        return

    for region, latency in sorted_results:
        # This is where the core concept of regional proximity is demonstrated.
        # Users geographically closer to a server typically experience lower latency.
        print(f"- {region}: {latency:.2f} ms")

    print("\n--- Conclusion ---")
    print("As observed, latency differs significantly across regions.")
    print("Hosting your application's backend or content delivery network (CDN) nodes")
    print("closer to your target users minimizes this latency, leading to a faster")
    print("and more responsive user experience, which is crucial for regional accessibility.")

if __name__ == "__main__":
    # Ensure 'requests' library is available.
    # If not, the user will need to install it: pip install requests
    try:
        import requests
    except ImportError:
        print("The 'requests' library is not installed.")
        print("Please install it using: pip install requests")
        sys.exit(1)
    main()