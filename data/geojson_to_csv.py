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
