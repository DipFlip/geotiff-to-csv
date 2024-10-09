import rasterio
import csv
import numpy as np
from pyproj import Transformer

def geotiff_to_csv(input_geotiff, output_csv):
    # Open the GeoTIFF file
    with rasterio.open(input_geotiff) as src:
        # Read the data
        data = src.read(1)  # Assuming single band raster
        
        # Get the geotransform information
        transform = src.transform
        
        # Get the CRS
        crs = src.crs
        
        # Create a transformer to convert to lat/lon
        transformer = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
        
        # Get rows and columns
        rows, cols = data.shape
        
        # Open the CSV file for writing
        with open(output_csv, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # Write header
            csvwriter.writerow(['Latitude', 'Longitude', 'Height_m'])
            
            # Iterate through each pixel
            for row in range(rows):
                for col in range(cols):
                    # Get x, y coordinates
                    x, y = transform * (col, row)
                    
                    # Convert to lat, lon
                    lon, lat = transformer.transform(x, y)
                    
                    # Get height value and convert from feet to meters
                    height = data[row, col]
                    
                    # Write to CSV
                    csvwriter.writerow([lat, lon, height])

    print(f"Conversion complete. Output saved to {output_csv}")

# Usage
input_geotiff = 'sample.tif'
output_csv = 'sample.csv'
geotiff_to_csv(input_geotiff, output_csv)