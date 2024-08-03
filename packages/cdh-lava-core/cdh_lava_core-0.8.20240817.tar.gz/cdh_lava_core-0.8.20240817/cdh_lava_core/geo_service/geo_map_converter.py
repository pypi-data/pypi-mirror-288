import geopandas as gpd
import os
import sys
import json
import pandas as pd
from shapely.affinity import translate, scale
from shapely.ops import unary_union
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import matplotlib.pyplot as plt
import topojson as tp
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

# List of states to keep (continental US, Alaska, Hawaii, and Washington DC)
desired_states = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
    'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
    'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 
    'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 
    'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 
    'Washington', 'West Virginia', 'Wisconsin', 'Wyoming', 'District of Columbia'
]

# Mapping of states to census regions (for possible future use)
state_to_region = {
    'Northeast': ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Rhode Island', 'Vermont', 'New Jersey', 'New York', 'Pennsylvania'],
    'Midwest': ['Illinois', 'Indiana', 'Michigan', 'Ohio', 'Wisconsin', 'Iowa', 'Kansas', 'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'South Dakota'],
    'South': ['Delaware', 'Florida', 'Georgia', 'Maryland', 'North Carolina', 'South Carolina', 'Virginia', 'District of Columbia', 'West Virginia', 'Alabama', 'Kentucky', 'Mississippi', 'Tennessee', 'Arkansas', 'Louisiana', 'Oklahoma', 'Texas'],
    'West': ['Arizona', 'Colorado', 'Idaho', 'Montana', 'Nevada', 'New Mexico', 'Utah', 'Wyoming', 'Alaska', 'California', 'Hawaii', 'Oregon', 'Washington']
}

# Mapping of states to census divisions (for possible future use)
state_to_division = {
    'New England': ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Rhode Island', 'Vermont'],
    'Middle Atlantic': ['New Jersey', 'New York', 'Pennsylvania'],
    'East North Central': ['Illinois', 'Indiana', 'Michigan', 'Ohio', 'Wisconsin'],
    'West North Central': ['Iowa', 'Kansas', 'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'South Dakota'],
    'South Atlantic': ['Delaware', 'Florida', 'Georgia', 'Maryland', 'North Carolina', 'South Carolina', 'Virginia', 'District of Columbia', 'West Virginia'],
    'East South Central': ['Alabama', 'Kentucky', 'Mississippi', 'Tennessee'],
    'West South Central': ['Arkansas', 'Louisiana', 'Oklahoma', 'Texas'],
    'Mountain': ['Arizona', 'Colorado', 'Idaho', 'Montana', 'Nevada', 'New Mexico', 'Utah', 'Wyoming'],
    'Pacific': ['Alaska', 'California', 'Hawaii', 'Oregon', 'Washington']
}

class GeoMapConverter:
    @staticmethod
    def load_shapefile(shapefile_path, data_product_id, environment):
        """Load the shapefile into a GeoDataFrame."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("load_shapefile"):
            try:
                geo_data_frame = gpd.read_file(shapefile_path)
                logger.info(f"Shapefile {shapefile_path} loaded successfully.")
                logger.info(f"Columns in the shapefile: {str(geo_data_frame.columns)}")
                return geo_data_frame
            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def filter_states(gdf):
        """Filter the GeoDataFrame to include only the desired states."""
        return gdf[gdf['NAME'].isin(desired_states)]

    @classmethod
    def move_alaska_hawaii(cls, gdf, data_product_id, environment):
        """Move Alaska and Hawaii for better visualization based on their shape names."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("move_alaska_hawaii"):
            try:
                # Reproject to a common projection for transformation
                gdf = gdf.to_crs("ESRI:102003")

                # Identify Alaska and Hawaii by name
                gdf_alaska = gdf[gdf['NAME'] == 'Alaska']
                gdf_hawaii = gdf[gdf['NAME'] == 'Hawaii']

                if not gdf_alaska.empty:     
                    gdf_alaska = cls.translate_geometries(gdf_alaska, 1300000, -4900000, 0.5, 32)
                    logger.info("Alaska repositioned.")
                if not gdf_hawaii.empty:
                    gdf_hawaii = cls.translate_geometries(gdf_hawaii, 5400000, -1500000, 1, 24)
                    logger.info("Hawaii repositioned.")

                # Remove original Alaska and Hawaii from the main GeoDataFrame
                gdf = gdf[~gdf['NAME'].isin(['Alaska', 'Hawaii'])]

                # Add moved Alaska and Hawaii back to the GeoDataFrame
                gdf = pd.concat([gdf, gdf_alaska, gdf_hawaii])

                return gdf

            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def translate_geometries(df, x, y, scale_factor, rotate_angle):
        df.loc[:, "geometry"] = df.geometry.translate(yoff=y, xoff=x)
        center = df.dissolve().centroid.iloc[0]
        df.loc[:, "geometry"] = df.geometry.scale(xfact=scale_factor, yfact=scale_factor, origin=center)
        df.loc[:, "geometry"] = df.geometry.rotate(rotate_angle, origin=center)
        return df

    @classmethod
    def merge_by_division(cls, gdf, data_product_id, environment):
        """Merge states into census divisions."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("merge_by_division"):
            try:
                divisions = []
                for division, states in state_to_division.items():
                    division_gdf = gdf[gdf['NAME'].isin(states)]
                    if not division_gdf.empty:
                        merged_division = division_gdf.dissolve()
                        merged_division['NAME'] = division
                        divisions.append(merged_division)
                
                if not divisions:
                    raise ValueError("No divisions were found when merging by division.")
                    
                merged_gdf = pd.concat(divisions, ignore_index=True)
                logger.info("States merged into divisions successfully.")
                return merged_gdf
            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def merge_by_region(cls, gdf, data_product_id, environment):
        """Merge states into census regions."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("merge_by_region"):
            try:
                regions = []
                for region, states in state_to_region.items():
                    region_gdf = gdf[gdf['NAME'].isin(states)]
                    if not region_gdf.empty:
                        merged_region = region_gdf.dissolve()
                        merged_region['NAME'] = region
                        regions.append(merged_region)
                
                if not regions:
                    raise ValueError("No regions were found when merging by region.")
                    
                merged_gdf = pd.concat(regions, ignore_index=True)
                logger.info("States merged into regions successfully.")
                return merged_gdf
            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
        
    @classmethod
    def plot_map(cls, gdf, output_path, data_product_id, environment, move_ak_hi=False, merge_regions=False, merge_divisions=False):
        """Plot the map including Alaska and Hawaii with options to move them and merge regions or divisions."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("plot_map"):
            try:
                # Filter the GeoDataFrame to include only desired states
                gdf = cls.filter_states(gdf)

                if move_ak_hi:
                    gdf = cls.move_alaska_hawaii(gdf, data_product_id, environment)
                    
                if merge_regions:
                    gdf = cls.merge_by_region(gdf, data_product_id, environment)
                
                if merge_divisions:
                    gdf = cls.merge_by_division(gdf, data_product_id, environment)

                # Reproject to WGS 84
                gdf = gdf.to_crs("EPSG:4326")
                logger.info("Data reprojected to EPSG:4326")

                # Create figure and axes for with Matplotlib for main map
                fig, ax = plt.subplots(1, figsize=(18, 14))
                # Remove the axis box from the main map
                ax.axis('off')
                
                # Create map of all divisions
                gdf.plot(color='lightblue', linewidth=0.8, ax=ax, edgecolor='0.8')

                # Save the figure
                fig.savefig(output_path, dpi=400, bbox_inches="tight")
                logger.info(f"Map saved to {output_path}")

            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def convert_to_topojson(cls, geo_data_frame, output_path, data_product_id, environment, move_ak_hi=False, merge_regions=False, merge_divisions=False):
        """Convert the shapefile to a TopoJSON file."""
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("convert_to_topojson"):
            try:
                
                if geo_data_frame is not None:
                    # Filter the GeoDataFrame to include only desired states
                    geo_data_frame = cls.filter_states(geo_data_frame)

                    if move_ak_hi:
                        geo_data_frame = cls.move_alaska_hawaii(geo_data_frame, data_product_id, environment)
                        
                    if merge_regions:
                        geo_data_frame = cls.merge_by_region(geo_data_frame, data_product_id, environment)
                    
                    if merge_divisions:
                        geo_data_frame = cls.merge_by_division(geo_data_frame, data_product_id, environment)

                    # Reproject to WGS 84
                    geo_data_frame = geo_data_frame.to_crs("EPSG:4326")
                    logger.info("Data reprojected to EPSG:4326")
                        
                    # Log the columns to identify the correct name column
                    logger.info(f"Columns in the shapefile: {str(geo_data_frame.columns)}")

                    # Try common alternatives if 'NAME' is not present
                    name_column = 'NAME'
                    if name_column not in geo_data_frame.columns:
                        possible_columns = ['name', 'Name', 'NAMELSAD', 'GEOID', 'LSAD', 'STUSPS']
                        for possible_col in possible_columns:
                            if possible_col in geo_data_frame.columns:
                                name_column = possible_col
                                break
                        else:
                            raise ValueError("The shapefile does not contain a 'NAME' or similar column for Power BI compatibility.")

                    # Convert GeoDataFrame to GeoJSON
                    geojson_data = json.loads(geo_data_frame.to_json())

                    # Convert GeoJSON to TopoJSON
                    topojson_data = tp.Topology(geojson_data).to_dict()

                    # Save the TopoJSON to a file
                    with open(output_path, 'w') as f:
                        json.dump(topojson_data, f, indent=2)

                    logger.info(f"TopoJSON file has been saved to {output_path}")
                else:
                    raise ValueError("Failed to load the shapefile. Conversion to TopoJSON aborted.")
            except Exception as ex:
                error_msg = f"Error: {ex}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

# Example usage
if __name__ == "__main__":
    shapefile_path = 'path_to_your_shapefile.shp'
    output_map_path = 'output_map.png'
    output_topojson_path = 'output_map.topojson'
    data_product_id = 'your_data_product_id'
    environment = 'your_environment'

    # Load and process shapefile
    gdf = GeoMapConverter.load_shapefile(shapefile_path, data_product_id, environment)
    
    # Plot map with moving Alaska and Hawaii
    GeoMapConverter.plot_map(gdf, output_map_path.replace(".png", "_moved.png"), data_product_id, environment, move_ak_hi=True, merge_regions=True)

    # Convert to TopoJSON
    GeoMapConverter.convert_to_topojson(gdf, output_topojson_path, data_product_id, environment, move_ak_hi=True, merge_regions=True)
