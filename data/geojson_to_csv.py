#!/usr/bin/env python3

import json
import csv

# Load your GeoJSON
with open('borough-boundaries3.geojson', 'r') as f:
    geojson = json.load(f)

# Define the output CSV file
with open('boroughs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        'boroname',
        'borocode',
        'pop2020',
        'median_income',
        'land_area_km2',
        'borough_president',
        'coordinates'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for feature in geojson.get('features', []):
        props = feature.get('properties', {})
        geometry = feature.get('geometry', {})

        # Skip features without proper geometry
        if not geometry or 'coordinates' not in geometry:
            continue

        # Make sure it's a Polygon or MultiPolygon
        geom_type = geometry.get('type')
        coords = geometry.get('coordinates')

        if geom_type not in ['Polygon', 'MultiPolygon']:
            continue

        # Stringify the coordinates safely
        try:
            coords_str = json.dumps(coords)
        except Exception as e:
            print(f"Skipping feature due to invalid coordinates: {e}")
            continue

        # Write the row to CSV
        writer.writerow({
            'boroname': props.get('boroname', ''),
            'borocode': props.get('borocode', ''),
            'pop2020': props.get('pop2020', ''),
            'median_income': props.get('median_income', ''),
            'land_area_km2': props.get('land_area_km2', ''),
            'borough_president': props.get('borough_president', ''),
            'coordinates': coords_str
        })
#!/usr/bin/env python3

import json
import csv

with open('borough-boundaries3.geojson') as f:
    geojson = json.load(f)

with open('boroughs.csv', 'w', newline='') as csvfile:
    fieldnames = ['boroname', 'borocode', 'pop2020', 'median_income', 'land_area_km2', 'borough_president', 'coordinates']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for feature in geojson['features']:
        props = feature['properties']
        coords = json.dumps(feature['geometry']['coordinates'])  # convert to string
        writer.writerow({
            'boroname': props['boroname'],
            'borocode': props['borocode'],
            'pop2020': props['pop2020'],
            'median_income': props.get('median_income'),
            'land_area_km2': props.get('land_area_km2'),
            'borough_president': props.get('borough_president'),
            'coordinates': coords
        })
