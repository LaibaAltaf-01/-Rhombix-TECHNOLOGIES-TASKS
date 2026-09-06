"""
Geolocation Tracker
--------------------
Fetches the user's (or any given) geolocation using their IP address
and displays it on an interactive map (HTML file opened in the browser).

Dependencies:
    pip install requests folium

Usage:
    python geolocation_tracker.py
    python geolocation_tracker.py 8.8.8.8      (look up a specific IP)
"""

import sys
import json
import webbrowser
import os

import requests

try:
    import folium
except ImportError:
    folium = None


def get_geolocation(ip_address: str = "") -> dict:
    """
    Fetch geolocation data for the given IP address.
    If ip_address is empty, the caller's own public IP is used.

    Uses the free ip-api.com JSON endpoint (no API key required).
    """
    url = f"http://ip-api.com/json/{ip_address}"
    params = {
        "fields": "status,message,country,regionName,city,zip,"
                  "lat,lon,timezone,isp,org,query"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Network error while contacting geolocation API: {exc}")

    data = response.json()

    if data.get("status") != "success":
        raise RuntimeError(f"Geolocation lookup failed: {data.get('message', 'unknown error')}")

    return data


def print_summary(data: dict) -> None:
    print("\n--- Geolocation Result ---")
    print(f"IP Address : {data.get('query')}")
    print(f"City       : {data.get('city')}")
    print(f"Region     : {data.get('regionName')}")
    print(f"Country    : {data.get('country')}")
    print(f"Zip Code   : {data.get('zip')}")
    print(f"Latitude   : {data.get('lat')}")
    print(f"Longitude  : {data.get('lon')}")
    print(f"Timezone   : {data.get('timezone')}")
    print(f"ISP        : {data.get('isp')}")
    print(f"Org        : {data.get('org')}")
    print("---------------------------\n")


def build_map(data: dict, output_file: str = "geolocation_map.html") -> str:
    """
    Build an interactive Leaflet map (via folium) centered on the location
    and save it as an HTML file. Returns the path to the saved file.
    """
    if folium is None:
        raise RuntimeError(
            "The 'folium' package is required to build the map. "
            "Install it with: pip install folium"
        )

    lat, lon = data.get("lat"), data.get("lon")
    if lat is None or lon is None:
        raise RuntimeError("Latitude/longitude not available for this IP.")

    location_label = f"{data.get('city', '')}, {data.get('regionName', '')}, {data.get('country', '')}"

    fmap = folium.Map(location=[lat, lon], zoom_start=11, tiles="OpenStreetMap")

    popup_html = (
        f"<b>IP:</b> {data.get('query')}<br>"
        f"<b>Location:</b> {location_label}<br>"
        f"<b>ISP:</b> {data.get('isp')}<br>"
        f"<b>Timezone:</b> {data.get('timezone')}"
    )

    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip="Click for details",
        icon=folium.Icon(color="red", icon="map-marker", prefix="fa"),
    ).add_to(fmap)

    folium.Circle(
        location=[lat, lon],
        radius=2000,
        color="crimson",
        fill=True,
        fill_opacity=0.15,
    ).add_to(fmap)

    fmap.save(output_file)
    return os.path.abspath(output_file)


def save_json(data: dict, output_file: str = "geolocation_data.json") -> str:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return os.path.abspath(output_file)


def main():
    ip_arg = sys.argv[1] if len(sys.argv) > 1 else ""

    print("Fetching geolocation data..." if not ip_arg else f"Fetching geolocation for {ip_arg}...")

    try:
        data = get_geolocation(ip_arg)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print_summary(data)

    json_path = save_json(data)
    print(f"Raw data saved to: {json_path}")

    try:
        map_path = build_map(data)
        print(f"Map saved to: {map_path}")

        # Try to open it automatically in the default browser
        try:
            webbrowser.open(f"file://{map_path}")
        except Exception:
            pass
    except RuntimeError as e:
        print(f"Warning: {e}")


if __name__ == "__main__":
    main()
