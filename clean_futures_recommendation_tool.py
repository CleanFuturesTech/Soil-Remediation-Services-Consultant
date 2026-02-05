"""
Clean Futures Solution Recommendation Tool
Permian Basin Soil Remediation Decision Support System

Compares three remediation approaches:
1. Dig & Haul to Landfill
2. Clean Futures Onsite Remediation
3. Clean Futures Surface Facility Treatment
"""

# ============================================================================
# VERSION
# ============================================================================
APP_VERSION = "1.4.3"

import streamlit as st
import pandas as pd
import json
import math
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Clean Futures Solution Recommendation",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - DISTINCTIVE DESIGN
# ============================================================================

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=Work+Sans:wght@300;400;500;600&display=swap');
    
    /* Main styling */
    .main {
        background: linear-gradient(135deg, #f8faf9 0%, #e8f4f0 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Crimson Pro', serif;
        color: #1a4d2e;
    }
    
    h1 {
        font-size: 3.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Body text */
    p, li, label, .stMarkdown {
        font-family: 'Work Sans', sans-serif;
        color: #2d5f3f;
    }
    
    /* Welcome section */
    .welcome-box {
        background: linear-gradient(135deg, #1a4d2e 0%, #2d7a4f 100%);
        color: white;
        padding: 3rem;
        border-radius: 16px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(26, 77, 46, 0.3);
    }
    
    .welcome-title {
        font-family: 'Crimson Pro', serif;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: white;
    }
    
    .welcome-subtitle {
        font-family: 'Work Sans', sans-serif;
        font-size: 1.3rem;
        font-weight: 300;
        color: #d4f1e3;
        margin-bottom: 1.5rem;
    }
    
    .mission-statement {
        font-family: 'Work Sans', sans-serif;
        font-size: 1.1rem;
        line-height: 1.8;
        color: white;
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #81c995;
    }
    
    /* Mode selector cards */
    .mode-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .mode-card:hover {
        border-color: #2d7a4f;
        box-shadow: 0 8px 24px rgba(45, 122, 79, 0.15);
        transform: translateY(-4px);
    }
    
    .mode-card-title {
        font-family: 'Crimson Pro', serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #1a4d2e;
        margin-bottom: 1rem;
    }
    
    /* Results cards */
    .solution-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 6px solid #2d7a4f;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }
    
    .recommended-badge {
        display: inline-block;
        background: linear-gradient(135deg, #81c995 0%, #2d7a4f 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 24px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    /* Metrics */
    .metric-box {
        background: linear-gradient(135deg, #f0f7f4 0%, #e1f0e8 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #c8e6d4;
    }
    
    .metric-value {
        font-family: 'Crimson Pro', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a4d2e;
        margin: 0;
    }
    
    .metric-label {
        font-family: 'Work Sans', sans-serif;
        font-size: 0.95rem;
        color: #5a8a6f;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2d7a4f 0%, #1a4d2e 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 8px !important;
        font-family: 'Work Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(45, 122, 79, 0.3) !important;
    }
    
    /* Ensure button text stays white - target all inner elements */
    .stButton > button span,
    .stButton > button p,
    .stButton > button div,
    .stButton button span,
    .stButton button p,
    .stButton button div,
    .stButton > button * {
        color: white !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(45, 122, 79, 0.4) !important;
    }
    
    .stButton > button:hover span,
    .stButton > button:hover p,
    .stButton > button:hover * {
        color: white !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8faf9;
    }
    
    /* Tables */
    .dataframe {
        font-family: 'Work Sans', sans-serif;
    }
    
    /* Pro/Con lists */
    .pros-list {
        background: #e8f5e9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
    }
    
    .cons-list {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-family: 'Work Sans', sans-serif;
        font-weight: 600;
        color: #1a4d2e;
    }
    
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS - DISTANCE AND GEOSPATIAL
# ============================================================================

# ============================================================================
# HELPER FUNCTIONS - DISTANCE AND GEOSPATIAL
# ============================================================================

def determine_state_county(lat, lon, db):
    """Determine state and county from GPS coordinates"""
    # Texas/New Mexico boundary is roughly at -103° longitude
    state = "Texas" if lon > -103.0 else "New Mexico"
    
    # Find nearest county from the landfill database
    county_distances = {}
    
    for lf in db['landfills']:
        county = lf['county']
        # Calculate distance to this landfill (use as proxy for county)
        distance = haversine_distance(lat, lon, lf['latitude'], lf['longitude'])
        
        # Keep the closest distance for each county
        if county not in county_distances or distance < county_distances[county]:
            county_distances[county] = distance
    
    if county_distances:
        # Return the county with the closest landfill
        nearest_county = min(county_distances, key=county_distances.get)
        return state, nearest_county
    
    # Fallback: try to estimate based on coordinates
    if state == "Texas":
        # Rough Texas Permian Basin county estimates
        if lon > -101.5:
            return state, "HOWARD"
        elif lon > -102.5:
            return state, "MIDLAND"
        else:
            return state, "REEVES"
    else:
        # New Mexico side
        return state, "LEA"

def get_soil_type(lat, lon, state):
    """Estimate soil type based on location in Permian Basin"""
    # Simplified soil classification for Permian Basin
    # In production, this would query USDA Web Soil Survey or similar database
    
    # Eastern Permian (more clay-rich)
    if lon > -102.0:
        return "Clay Loam / Silty Clay"
    # Central Permian (mixed)
    elif lon > -103.5:
        return "Sandy Clay Loam / Caliche"
    # Western Permian (more sandy)
    else:
        return "Sandy Loam / Desert Soils"

def get_regulatory_thresholds(state, groundwater_depth_category=None):
    """
    Get soil regulatory thresholds for TPH and Chlorides.
    
    Args:
        state: "Texas" or "New Mexico"
        groundwater_depth_category: For New Mexico only - one of:
            - "50_or_less" (groundwater at 50 feet or less)
            - "51_to_100" (groundwater at 51-100 feet)  
            - "over_100" (groundwater at >100 feet)
    
    Returns:
        Dictionary with threshold values and regulatory information
    """
    # Texas TCEQ Protective Concentration Levels (PCLs)
    # New Mexico NMED Soil Screening Levels (SSLs)
    
    if state == "Texas":
        return {
            'tph_threshold_mgkg': 10000,
            'tph_residential_mgkg': 10000,
            'tph_industrial_mgkg': 10000,
            'chloride_threshold_mgkg': 3000,
            'chloride_soil_mgkg': '3,000 mg/kg (guidance)',
            'benzene_threshold_mgkg': 0.026,
            'regulatory_agency': 'TCEQ (Texas Commission on Environmental Quality)',
            'regulation_type': 'Guidance',
            'groundwater_depth_display': 'N/A (Texas)',
            'notes': 'Texas uses risk-based guidance levels; site-specific cleanup levels may vary'
        }
    else:  # New Mexico - thresholds depend on groundwater depth
        if groundwater_depth_category == "50_or_less":
            return {
                'tph_threshold_mgkg': 100,
                'tph_residential_mgkg': 100,
                'tph_industrial_mgkg': 100,
                'chloride_threshold_mgkg': 600,
                'chloride_soil_mgkg': '600 mg/kg',
                'benzene_threshold_mgkg': 10,
                'btex_threshold_mgkg': 50,
                'regulatory_agency': 'NMED (New Mexico Environment Department)',
                'regulation_type': 'Regulation',
                'groundwater_depth_display': '≤50 feet',
                'notes': 'Strictest thresholds apply when groundwater is shallow (≤50 ft)'
            }
        elif groundwater_depth_category == "51_to_100":
            return {
                'tph_threshold_mgkg': 2500,
                'tph_residential_mgkg': 2500,
                'tph_industrial_mgkg': 2500,
                'chloride_threshold_mgkg': 10000,
                'chloride_soil_mgkg': '10,000 mg/kg',
                'benzene_threshold_mgkg': 10,
                'btex_threshold_mgkg': 50,
                'gro_dro_threshold_mgkg': 1000,
                'regulatory_agency': 'NMED (New Mexico Environment Department)',
                'regulation_type': 'Regulation',
                'groundwater_depth_display': '51-100 feet',
                'notes': 'Moderate thresholds apply for mid-depth groundwater (51-100 ft)'
            }
        else:  # over_100 or default
            return {
                'tph_threshold_mgkg': 2500,
                'tph_residential_mgkg': 2500,
                'tph_industrial_mgkg': 2500,
                'chloride_threshold_mgkg': 20000,
                'chloride_soil_mgkg': '20,000 mg/kg',
                'benzene_threshold_mgkg': 10,
                'btex_threshold_mgkg': 50,
                'gro_dro_threshold_mgkg': 1000,
                'regulatory_agency': 'NMED (New Mexico Environment Department)',
                'regulation_type': 'Regulation',
                'groundwater_depth_display': '>100 feet',
                'notes': 'Less restrictive thresholds apply when groundwater is deep (>100 ft)'
            }

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two GPS coordinates in miles"""
    R = 3959  # Earth's radius in miles
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def load_facilities_database():
    """Return the facilities database (embedded in code for reliable deployment)"""
    return {
        "landfills": [
            {
                "id": "LF001",
                "company": "MILESTONE",
                "site_name": "UPTON",
                "county": "GLASSCOCK",
                "latitude": 31.499316,
                "longitude": -101.931524,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": True,
                "backfill_cost_cy": 10
            },
            {
                "id": "LF002",
                "company": "MILESTONE",
                "site_name": "STANTON LANDFILL",
                "county": "HOWARD",
                "latitude": 31.981708,
                "longitude": -101.771822,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": False,
                "backfill_cost_cy": 0
            },
            {
                "id": "LF003",
                "company": "R360",
                "site_name": "WISHBONE",
                "county": "HOWARD",
                "latitude": 32.201328,
                "longitude": -101.737306,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": True,
                "backfill_cost_cy": 10
            },
            {
                "id": "LF004",
                "company": "REPUBLIC",
                "site_name": "SOUTH ODESSA",
                "county": "MIDLAND",
                "latitude": 31.77227,
                "longitude": -102.542218,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": False,
                "backfill_cost_cy": 0
            },
            {
                "id": "LF005",
                "company": "US ECOLOGY",
                "site_name": "REAGAN",
                "county": "GLASSCOCK",
                "latitude": 31.418575,
                "longitude": -101.691314,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": True,
                "backfill_cost_cy": 10
            },
            {
                "id": "LF006",
                "company": "WM",
                "site_name": "BIG LAKE",
                "county": "GLASSCOCK",
                "latitude": 31.344978,
                "longitude": -101.502558,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": False,
                "backfill_cost_cy": 0
            },
            {
                "id": "LF007",
                "company": "WM",
                "site_name": "HOWARD",
                "county": "HOWARD",
                "latitude": 32.175082,
                "longitude": -101.665695,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": False,
                "backfill_cost_cy": 0
            },
            {
                "id": "LF008",
                "company": "MILESTONE",
                "site_name": "ORLA EWF",
                "county": "LOVING",
                "latitude": 31.865379,
                "longitude": -103.847547,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": True,
                "backfill_cost_cy": 10
            },
            {
                "id": "LF009",
                "company": "R360",
                "site_name": "RED BLUFF",
                "county": "CULBERSON",
                "latitude": 31.9861,
                "longitude": -104.021569,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": False,
                "backfill_cost_cy": 0
            },
            {
                "id": "LF010",
                "company": "WM",
                "site_name": "ORLA LANDFILL",
                "county": "LOVING",
                "latitude": 31.824627,
                "longitude": -103.910185,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": False,
                "backfill_cost_cy": 0
            },
            {
                "id": "LF011",
                "company": "WM",
                "site_name": "DEEP SIX",
                "county": "REEVES",
                "latitude": 31.286899,
                "longitude": -103.392814,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": False,
                "backfill_cost_cy": 0
            },
            {
                "id": "LF012",
                "company": "REPUBLIC",
                "site_name": "REEVES",
                "county": "REEVES",
                "latitude": 31.654254,
                "longitude": -103.637612,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": True,
                "backfill_cost_cy": 10
            },
            {
                "id": "LF013",
                "company": "DESERT ENVIRONMENTAL",
                "site_name": "DRF MENTONE",
                "county": "LOVING",
                "latitude": 31.960808,
                "longitude": -103.75866,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": True,
                "backfill_cost_cy": 10
            },
            {
                "id": "LF014",
                "company": "US ECOLOGY",
                "site_name": "PECOS",
                "county": "REEVES",
                "latitude": 31.320076,
                "longitude": -103.621133,
                "accepts_tph": True,
                "tph_max_mgkg": 5000,
                "accepts_chloride": True,
                "chloride_max_mgkg": 10000,
                "disposal_cost_cy": 25,
                "backfill_available": False,
                "backfill_cost_cy": 0
            }
        ],
        "clean_futures_facilities": [
            {
                "id": "CF001",
                "facility_name": "Clean Futures Facility 1",
                "region": "Delaware Basin",
                "latitude": 31.9195,
                "longitude": -103.6285,
                "processing_cost_cy": 25,
                "includes_backfill": True,
                "backfill_cost_cy": 0,
                "typical_turnaround_days": 30,
                "notes": "Treated soil returned to site"
            },
            {
                "id": "CF002",
                "facility_name": "Clean Futures Facility 2",
                "region": "Midland Basin",
                "latitude": 32.1022,
                "longitude": -102.4654,
                "processing_cost_cy": 25,
                "includes_backfill": True,
                "backfill_cost_cy": 0,
                "typical_turnaround_days": 30,
                "notes": "Treated soil returned to site"
            },
            {
                "id": "CF003",
                "facility_name": "Clean Futures Facility 3",
                "region": "Central Basin",
                "latitude": 31.3458,
                "longitude": -101.7301,
                "processing_cost_cy": 25,
                "includes_backfill": True,
                "backfill_cost_cy": 0,
                "typical_turnaround_days": 30,
                "notes": "Treated soil returned to site"
            },
            {
                "id": "CF004",
                "facility_name": "Clean Futures Facility 4",
                "region": "Eastern Basin",
                "latitude": 32.3109,
                "longitude": -101.8421,
                "processing_cost_cy": 25,
                "includes_backfill": True,
                "backfill_cost_cy": 0,
                "typical_turnaround_days": 30,
                "notes": "Treated soil returned to site"
            }
        ]
    }

def find_nearest_qualified_landfill(lat, lon, tph_level, chloride_level, needs_backfill, db):
    """Find the nearest landfill that accepts the contamination levels"""
    qualified = []
    
    for lf in db['landfills']:
        # Check if landfill accepts the contamination levels
        accepts_tph = tph_level <= lf['tph_max_mgkg'] if tph_level > 0 else True
        accepts_chloride = chloride_level <= lf['chloride_max_mgkg'] if chloride_level > 0 else True
        
        if accepts_tph and accepts_chloride:
            # Include all qualified landfills - we'll note backfill availability separately
            distance = haversine_distance(lat, lon, lf['latitude'], lf['longitude'])
            qualified.append({
                'landfill': lf,
                'distance_miles': distance
            })
    
    # Sort by distance
    qualified.sort(key=lambda x: x['distance_miles'])
    
    return qualified[0] if qualified else None

def find_nearest_cf_facility(lat, lon, db):
    """Find the nearest Clean Futures facility"""
    facilities = []
    
    for cf in db['clean_futures_facilities']:
        distance = haversine_distance(lat, lon, cf['latitude'], cf['longitude'])
        facilities.append({
            'facility': cf,
            'distance_miles': distance
        })
    
    facilities.sort(key=lambda x: x['distance_miles'])
    
    return facilities[0] if facilities else None

# ============================================================================
# CALCULATION FUNCTIONS
# ============================================================================

def calculate_volume_cy(surface_area_sqft, depth_ft):
    """Calculate volume in cubic yards from surface area and depth"""
    cubic_feet = surface_area_sqft * depth_ft
    cubic_yards = cubic_feet / 27
    return cubic_yards

def calculate_co2_emissions(fuel_gallons):
    """Calculate CO2 emissions from fuel consumption"""
    # Diesel produces approximately 22.38 lbs CO2 per gallon
    co2_lbs = fuel_gallons * 22.38
    co2_tons = co2_lbs / 2000
    return co2_lbs, co2_tons

def calculate_dig_and_haul(volume_cy, site_lat, site_lon, needs_backfill, 
                          tph_level, chloride_level, db, 
                          num_trucks=3, equipment_capacity_per_day=300,
                          landfill_has_backfill=False, extra_backfill_minutes=0,
                          advanced_params=None):
    """
    Calculate costs and metrics for Dig & Haul option.
    
    Implements bottleneck analysis:
    - Truck capacity/day = (trips per truck per day) × num_trucks × truck_capacity_cy
    - Equipment capacity/day = from input (simple) or calculated (advanced)
    - Actual daily capacity = MIN(truck capacity, equipment capacity)
    
    Backfill logic:
    - If landfill has backfill: no extra time needed
    - If landfill does NOT have backfill: add extra_backfill_minutes to each trip
    - Extra travel time affects: trip duration, project timeline, trucking cost, CO2
    
    This math aligns with Advanced Mode where users can specify detailed equipment.
    """
    
    # Find nearest qualified landfill
    nearest_lf = find_nearest_qualified_landfill(site_lat, site_lon, tph_level, 
                                                  chloride_level, needs_backfill, db)
    
    if not nearest_lf:
        return None
    
    landfill = nearest_lf['landfill']
    distance_miles = nearest_lf['distance_miles']
    
    # Use advanced parameters or defaults
    if advanced_params:
        truck_capacity_cy = advanced_params.get('truck_capacity_cy', 18)
        num_trucks = advanced_params.get('num_trucks', num_trucks)
        truck_hourly_rate = advanced_params.get('truck_hourly_rate', 85)
        excavator_rate = advanced_params.get('excavator_rate', 150)
        loader_rate = advanced_params.get('loader_rate', 125)
        work_hours_per_day = advanced_params.get('work_hours_per_day', 10)
        disposal_cost = advanced_params.get('disposal_cost_cy', landfill['disposal_cost_cy'])
        backfill_cost = advanced_params.get('backfill_cost_cy', 10)
        # Advanced mode: calculate equipment capacity from detailed specs
        excavator_capacity_cy_hr = advanced_params.get('excavator_capacity_cy_hr', 40)
        loader_capacity_cy_hr = advanced_params.get('loader_capacity_cy_hr', 35)
        num_excavators = advanced_params.get('num_excavators', 1)
        num_loaders = advanced_params.get('num_loaders', 1)
        equipment_capacity_per_day = min(
            excavator_capacity_cy_hr * num_excavators,
            loader_capacity_cy_hr * num_loaders
        ) * work_hours_per_day
    else:
        # Simple mode defaults
        truck_capacity_cy = 18
        truck_hourly_rate = 85
        excavator_rate = 150
        loader_rate = 125
        work_hours_per_day = 10
        disposal_cost = landfill['disposal_cost_cy']
        backfill_cost = 10 if needs_backfill else 0  # Always $10/CY in simple mode
        # equipment_capacity_per_day comes from function parameter (user selection)
    
    # Trip time calculation
    avg_speed_mph = 45
    travel_time_hours = distance_miles / avg_speed_mph
    loading_time = 0.25  # 15 min to load truck at site
    unloading_time = 0.5  # 30 min at landfill (drop off + pick up backfill if available)
    
    # Base trip time (assuming backfill at landfill)
    base_trip_time = loading_time + travel_time_hours + unloading_time + travel_time_hours + loading_time
    
    # Extra time if backfill NOT at landfill
    if needs_backfill and not landfill_has_backfill:
        extra_backfill_hours = extra_backfill_minutes / 60.0
    else:
        extra_backfill_hours = 0
    
    # Total trip time includes extra backfill sourcing time
    trip_time = base_trip_time + extra_backfill_hours
    
    # BOTTLENECK ANALYSIS
    # Calculate truck capacity per day
    trips_per_truck_per_day = work_hours_per_day / trip_time
    truck_capacity_per_day = trips_per_truck_per_day * num_trucks * truck_capacity_cy
    
    # Determine bottleneck
    if truck_capacity_per_day <= equipment_capacity_per_day:
        bottleneck = "Trucking"
        actual_daily_capacity = truck_capacity_per_day
    else:
        bottleneck = "Loading Equipment"
        actual_daily_capacity = equipment_capacity_per_day
    
    # Calculate duration based on bottleneck
    project_days = math.ceil(volume_cy / actual_daily_capacity)
    project_hours = project_days * work_hours_per_day
    
    # Number of trips (for cost calculation)
    num_trips = math.ceil(volume_cy / truck_capacity_cy)
    
    # COSTS
    # Equipment runs for project duration
    equipment_cost = (excavator_rate + loader_rate) * project_hours
    
    # Trucking cost based on actual trips needed (includes extra backfill time)
    total_truck_hours = num_trips * trip_time
    trucking_cost = total_truck_hours * truck_hourly_rate
    
    # Disposal and backfill
    disposal_total = volume_cy * disposal_cost
    backfill_total = volume_cy * backfill_cost if needs_backfill else 0
    
    total_cost = equipment_cost + trucking_cost + disposal_total + backfill_total
    cost_per_cy = total_cost / volume_cy
    
    # CO2 calculations
    excavator_fuel_gph = 6
    loader_fuel_gph = 5
    truck_fuel_gph = 4
    
    # Base fuel consumption
    base_truck_hours = num_trips * base_trip_time
    base_truck_fuel = truck_fuel_gph * base_truck_hours
    
    # Extra fuel from backfill sourcing trips
    extra_backfill_truck_hours = num_trips * extra_backfill_hours
    extra_backfill_fuel = truck_fuel_gph * extra_backfill_truck_hours
    
    total_fuel = (excavator_fuel_gph * project_hours + 
                  loader_fuel_gph * project_hours +
                  base_truck_fuel +
                  extra_backfill_fuel)
    
    co2_lbs, co2_tons = calculate_co2_emissions(total_fuel)
    
    # Also calculate CO2 breakdown for display
    _, extra_backfill_co2_tons = calculate_co2_emissions(extra_backfill_fuel)
    
    return {
        'option_name': 'Dig & Haul to Landfill',
        'total_cost': total_cost,
        'cost_per_cy': cost_per_cy,
        'project_days': project_days,
        'landfill_name': f"{landfill['company']} - {landfill['site_name']}",
        'distance_miles': distance_miles,
        'co2_tons': co2_tons,
        'equipment_cost': equipment_cost,
        'trucking_cost': trucking_cost,
        'disposal_cost': disposal_total,
        'backfill_cost': backfill_total,
        'includes_backfill': needs_backfill,
        'backfill_available_at_landfill': landfill_has_backfill,
        # Bottleneck info
        'bottleneck': bottleneck,
        'truck_capacity_per_day': truck_capacity_per_day,
        'equipment_capacity_per_day': equipment_capacity_per_day,
        'actual_daily_capacity': actual_daily_capacity,
        'num_trucks': num_trucks,
        'num_trips': num_trips,
        'trip_time_hours': trip_time,
        'base_trip_time_hours': base_trip_time,
        # Extra backfill info
        'extra_backfill_minutes': extra_backfill_minutes if needs_backfill and not landfill_has_backfill else 0,
        'extra_backfill_co2_tons': extra_backfill_co2_tons
    }

def calculate_onsite_remediation(volume_cy, site_lat, site_lon, soil_permeability='medium',
                                tph_level=0, chloride_level=0, advanced_params=None):
    """Calculate costs and metrics for Onsite Remediation option"""
    
    # Simple mode: flat $30/CY rate
    # Advanced mode: will use detailed calculation with mobilization, amendments, etc.
    if advanced_params:
        processing_cost_cy = advanced_params.get('onsite_processing_cost_cy', 30)
        # Advanced mode could add mobilization, amendments, etc. here
        total_processing_cost = volume_cy * processing_cost_cy
        mobilization_cost = advanced_params.get('mobilization_cost', 0)
        amendment_cost = advanced_params.get('amendment_cost', 0)
        total_cost = total_processing_cost + mobilization_cost + amendment_cost
    else:
        # Simple mode: flat $30/CY all-in rate
        processing_cost_cy = 30
        total_processing_cost = volume_cy * processing_cost_cy
        mobilization_cost = 0  # Included in flat rate
        amendment_cost = 0  # Included in flat rate
        total_cost = total_processing_cost
    
    # Treatment duration estimation based on soil permeability
    base_treatment_days = 45
    if soil_permeability == 'high':
        treatment_days = base_treatment_days * 0.7  # Faster treatment
    elif soil_permeability == 'low':
        treatment_days = base_treatment_days * 1.5  # Slower treatment
    else:
        treatment_days = base_treatment_days
    
    # Adjust for contamination levels
    if tph_level > 3000:
        treatment_days *= 1.2
    if chloride_level > 7000:
        treatment_days *= 1.2
    
    treatment_days = int(treatment_days)
    
    cost_per_cy = total_cost / volume_cy
    
    # CO2 estimation (much lower than dig & haul)
    # Onsite equipment and limited trucking
    estimated_fuel_gallons = volume_cy * 0.1  # Much less fuel than hauling
    co2_lbs, co2_tons = calculate_co2_emissions(estimated_fuel_gallons)
    
    return {
        'option_name': 'Clean Futures Onsite Remediation',
        'total_cost': total_cost,
        'cost_per_cy': cost_per_cy,
        'project_days': treatment_days,
        'processing_cost': total_processing_cost,
        'mobilization_cost': mobilization_cost,
        'amendment_cost': amendment_cost,
        'co2_tons': co2_tons,
        'includes_backfill': True,
        'soil_returned_clean': True,
        'permeability_factor': soil_permeability,
        'rate_per_cy': processing_cost_cy
    }

def calculate_surface_facility(volume_cy, site_lat, site_lon, needs_backfill,
                               tph_level, chloride_level, db, 
                               num_trucks=3, equipment_capacity_per_day=300,
                               advanced_params=None):
    """
    Calculate costs and metrics for Surface Facility option.
    
    KEY CONCEPT: Operators drop off contaminated soil and pick up clean backfill
    (from previously treated stockpile) on the SAME TRIP. Treatment happens after
    the operator leaves and doesn't affect their timeline.
    
    This makes Surface Facility timeline = just the hauling days (same as Dig & Haul).
    
    Competitive advantages over landfill:
    - No disposal liability (soil is treated, not buried)
    - Backfill included (pick up clean soil same trip)
    - Faster/more convenient than sourcing separate backfill
    - Environmentally friendly alternative
    """
    
    # Find nearest CF facility
    nearest_cf = find_nearest_cf_facility(site_lat, site_lon, db)
    
    if not nearest_cf:
        return None
    
    facility = nearest_cf['facility']
    distance_miles = nearest_cf['distance_miles']
    
    # Transportation parameters
    if advanced_params:
        truck_capacity_cy = advanced_params.get('truck_capacity_cy', 18)
        num_trucks = advanced_params.get('num_trucks', num_trucks)
        truck_hourly_rate = advanced_params.get('truck_hourly_rate', 85)
        processing_cost_cy = advanced_params.get('surface_processing_cost_cy', 25)
        work_hours_per_day = advanced_params.get('work_hours_per_day', 10)
        # Advanced mode equipment calculation
        excavator_capacity_cy_hr = advanced_params.get('excavator_capacity_cy_hr', 40)
        loader_capacity_cy_hr = advanced_params.get('loader_capacity_cy_hr', 35)
        num_excavators = advanced_params.get('num_excavators', 1)
        num_loaders = advanced_params.get('num_loaders', 1)
        equipment_capacity_per_day = min(
            excavator_capacity_cy_hr * num_excavators,
            loader_capacity_cy_hr * num_loaders
        ) * work_hours_per_day
    else:
        truck_capacity_cy = 18
        truck_hourly_rate = 85
        processing_cost_cy = facility['processing_cost_cy']
        work_hours_per_day = 10
        # equipment_capacity_per_day comes from function parameter
    
    # Trip calculations
    avg_speed_mph = 45
    travel_time_hours = distance_miles / avg_speed_mph
    loading_time = 0.25  # Load contaminated soil at site
    unloading_time = 0.5  # Drop off contaminated, pick up clean backfill at facility
    
    # Round trip time (drop off dirty, pick up clean - all in one trip)
    trip_time = loading_time + travel_time_hours + unloading_time + travel_time_hours + loading_time
    
    # BOTTLENECK ANALYSIS
    # Calculate truck capacity per day
    trips_per_truck_per_day = work_hours_per_day / trip_time
    truck_capacity_per_day = trips_per_truck_per_day * num_trucks * truck_capacity_cy
    
    # Determine bottleneck
    if truck_capacity_per_day <= equipment_capacity_per_day:
        bottleneck = "Trucking"
        actual_daily_capacity = truck_capacity_per_day
    else:
        bottleneck = "Loading Equipment"
        actual_daily_capacity = equipment_capacity_per_day
    
    # Calculate hauling duration - THIS IS THE TOTAL PROJECT TIME
    # (No waiting for treatment - operator picks up clean backfill same trip)
    project_days = math.ceil(volume_cy / actual_daily_capacity)
    
    # Number of trips
    num_trips = math.ceil(volume_cy / truck_capacity_cy)
    total_truck_hours = num_trips * trip_time
    
    # COSTS
    trucking_cost = total_truck_hours * truck_hourly_rate
    processing_cost = volume_cy * processing_cost_cy
    
    # Equipment cost for loading (excavator + loader during project)
    excavator_rate = 150
    loader_rate = 125
    equipment_hours = project_days * work_hours_per_day
    equipment_cost = (excavator_rate + loader_rate) * equipment_hours
    
    total_cost = trucking_cost + processing_cost + equipment_cost
    cost_per_cy = total_cost / volume_cy
    
    # CO2 (trucking + loading equipment)
    truck_fuel_gph = 4
    excavator_fuel_gph = 6
    loader_fuel_gph = 5
    total_fuel = (truck_fuel_gph * total_truck_hours + 
                  excavator_fuel_gph * equipment_hours +
                  loader_fuel_gph * equipment_hours)
    co2_lbs, co2_tons = calculate_co2_emissions(total_fuel)
    
    return {
        'option_name': 'Clean Futures Surface Facility',
        'total_cost': total_cost,
        'cost_per_cy': cost_per_cy,
        'project_days': project_days,  # Just haul days - no treatment wait!
        'facility_name': facility['facility_name'],
        'distance_miles': distance_miles,
        'trucking_cost': trucking_cost,
        'processing_cost': processing_cost,
        'equipment_cost': equipment_cost,
        'co2_tons': co2_tons,
        'includes_backfill': True,
        'soil_returned_clean': True,
        # Bottleneck info
        'bottleneck': bottleneck,
        'truck_capacity_per_day': truck_capacity_per_day,
        'equipment_capacity_per_day': equipment_capacity_per_day,
        'actual_daily_capacity': actual_daily_capacity,
        'num_trucks': num_trucks,
        'num_trips': num_trips,
        'trip_time_hours': trip_time
    }

def generate_recommendation(dig_haul, onsite, surface_facility, user_priorities):
    """Generate recommendation based on calculations and user priorities"""
    
    options = []
    if dig_haul:
        options.append(('dig_haul', dig_haul))
    if onsite:
        options.append(('onsite', onsite))
    if surface_facility:
        options.append(('surface', surface_facility))
    
    if not options:
        return None
    
    # Score each option based on priorities
    scores = {}
    for opt_type, opt in options:
        score = 0
        
        # Cost priority
        if user_priorities.get('cost', 'medium') == 'high':
            # Lower cost = higher score
            min_cost = min([o[1]['cost_per_cy'] for o in options])
            score += 40 * (1 - (opt['cost_per_cy'] - min_cost) / min_cost) if min_cost > 0 else 20
        elif user_priorities.get('cost', 'medium') == 'medium':
            min_cost = min([o[1]['cost_per_cy'] for o in options])
            score += 20 * (1 - (opt['cost_per_cy'] - min_cost) / min_cost) if min_cost > 0 else 10
        
        # Timeline priority
        if user_priorities.get('speed', 'medium') == 'high':
            min_days = min([o[1]['project_days'] for o in options])
            score += 30 * (1 - (opt['project_days'] - min_days) / min_days) if min_days > 0 else 15
        elif user_priorities.get('speed', 'medium') == 'medium':
            min_days = min([o[1]['project_days'] for o in options])
            score += 15 * (1 - (opt['project_days'] - min_days) / min_days) if min_days > 0 else 7
        
        # ESG priority
        if user_priorities.get('esg', 'medium') == 'high':
            min_co2 = min([o[1]['co2_tons'] for o in options])
            score += 30 * (1 - (opt['co2_tons'] - min_co2) / min_co2) if min_co2 > 0 else 15
            # Bonus for treatment vs disposal
            if opt_type in ['onsite', 'surface']:
                score += 10
        elif user_priorities.get('esg', 'medium') == 'medium':
            min_co2 = min([o[1]['co2_tons'] for o in options])
            score += 15 * (1 - (opt['co2_tons'] - min_co2) / min_co2) if min_co2 > 0 else 7
        
        scores[opt_type] = score
    
    # Find recommendation
    recommended = max(scores, key=scores.get)
    
    return recommended, scores

# ============================================================================
# WELCOME PAGE
# ============================================================================

def show_welcome_page():
    """Display the welcome page"""
    
    st.markdown(f"""
        <div class="welcome-box">
            <div class="welcome-title">Clean Futures Solution Recommendation Tool</div>
            <div style="color: #81c995; font-size: 0.9rem; margin-bottom: 0.5rem;">Version {APP_VERSION}</div>
            <div class="welcome-subtitle">Intelligent Decision Support for Soil Remediation in the Permian Basin</div>
            <div class="mission-statement">
                At Clean Futures, we're committed to providing innovative solutions that make our world 
                better and cleaner. Our approach combines cutting-edge remediation technology with 
                environmental stewardship, helping you make informed decisions that balance cost, 
                timeline, and sustainability. Whether you need rapid dig-and-haul services, onsite 
                treatment, or surface facility processing, we're here to guide you to the best solution 
                for your unique situation.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 🎯 How Can We Help You Today?")
    st.write("Choose your path to get started:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="mode-card">
                <div class="mode-card-title">⚡ Simple Mode</div>
                <p><strong>Quick estimates with minimal input</strong></p>
                <ul>
                    <li>Basic site information</li>
                    <li>Standard assumptions</li>
                    <li>Fast preliminary recommendations</li>
                    <li>Perfect for initial planning</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Simple Mode", key="simple", use_container_width=True):
            st.session_state.mode = 'simple'
            st.rerun()
    
    with col2:
        st.markdown("""
            <div class="mode-card">
                <div class="mode-card-title">🎛️ Advanced Mode</div>
                <p><strong>Detailed analysis with custom parameters</strong></p>
                <ul>
                    <li>Comprehensive site data</li>
                    <li>Custom equipment & costs</li>
                    <li>Precise recommendations</li>
                    <li>Ideal for final decision-making</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Advanced Mode", key="advanced", use_container_width=True):
            st.session_state.mode = 'advanced'
            st.rerun()
    
    st.markdown("---")
    
    # Additional info
    with st.expander("📚 About This Tool"):
        st.markdown("""
            ### What This Tool Does
            
            This recommendation engine analyzes your contaminated soil situation and compares three 
            remediation approaches:
            
            1. **Dig & Haul to Landfill** - Excavate, transport to qualified landfill, replace with clean fill
            2. **Clean Futures Onsite Remediation** - Treat soil in place using our proven methods
            3. **Clean Futures Surface Facility** - Transport to our facility for treatment, return clean soil
            
            ### What You'll Get
            
            - **Cost Analysis** - Detailed breakdown of all costs for each option
            - **Timeline Estimates** - Project duration from start to completion
            - **Environmental Impact** - CO2 emissions and sustainability metrics
            - **Pros & Cons** - Clear comparison of advantages and limitations
            - **Smart Recommendation** - AI-powered suggestion based on your priorities
            
            ### Coverage Area
            
            Currently optimized for the **Permian Basin** region (West Texas & SE New Mexico), with:
            - 14 qualified landfills in the database
            - 4 Clean Futures surface facilities
            - Regional cost and regulatory data
        """)

# ============================================================================
# QUESTIONNAIRE - SIMPLE MODE
# ============================================================================

def show_simple_questionnaire():
    """Display simple mode questionnaire"""
    
    st.title("📝 Simple Mode Questionnaire")
    st.markdown("### Tell us about your contaminated soil site")
    st.write("Provide basic details and we'll recommend the best remediation solution.")
    
    # Back button
    if st.button("← Back to Welcome", key="back_simple"):
        st.session_state.mode = None
        st.rerun()
    
    # =========================================================================
    # SITE DIMENSIONS - Outside form for dynamic volume calculation
    # =========================================================================
    st.markdown("### 📏 Site Dimensions")
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        surface_area = st.number_input("Surface Area (square feet)", value=5000, min_value=100, key="surface_area")
    with col2:
        depth = st.number_input("Depth of Contamination (feet)", value=5.0, min_value=0.5, max_value=30.0, step=0.5, key="depth")
    with col3:
        # Dynamic volume calculation
        volume_cy = calculate_volume_cy(surface_area, depth)
        st.markdown("**Estimated Volume**")
        st.markdown(f"### 📦 {volume_cy:,.0f} CY")
    
    st.markdown("---")
    
    # =========================================================================
    # BACKFILL OPTIONS - Outside form for dynamic toggle behavior
    # =========================================================================
    st.markdown("### 🔄 Backfill Options")
    needs_backfill = st.checkbox("Clean backfill required", value=True, key="needs_backfill")
    
    if needs_backfill:
        st.markdown("**For Dig & Haul option:**")
        col1, col2 = st.columns(2)
        with col1:
            landfill_has_backfill = st.toggle(
                "Landfill has backfill available?",
                value=False,
                help="Most landfills do NOT have backfill on-site. If unchecked, you'll need to pick up backfill elsewhere.",
                key="landfill_has_backfill"
            )
        with col2:
            if landfill_has_backfill:
                # When landfill has backfill, show disabled slider at 0
                st.slider(
                    "Extra time for backfill pickup (minutes)",
                    min_value=0,
                    max_value=120,
                    value=0,
                    step=5,
                    disabled=True,
                    key="backfill_slider_disabled"
                )
                extra_backfill_minutes = 0
                st.caption("✅ Backfill at landfill - no extra trip needed")
            else:
                # When landfill doesn't have backfill, show active slider
                extra_backfill_minutes = st.slider(
                    "Extra time for backfill pickup (minutes)",
                    min_value=0,
                    max_value=120,
                    value=30,
                    step=5,
                    help="Additional round-trip time to pick up backfill from another source (e.g., quarry, supplier)",
                    key="backfill_slider_active"
                )
    else:
        landfill_has_backfill = False
        extra_backfill_minutes = 0
    
    st.markdown("---")
    
    # =========================================================================
    # SITE LOCATION - Outside form for dynamic state detection
    # =========================================================================
    st.markdown("### 📍 Site Location")
    col1, col2 = st.columns(2)
    with col1:
        site_lat = st.number_input("Latitude", value=32.2366, min_value=30.0, max_value=35.0, format="%.4f", key="site_lat_simple")
    with col2:
        site_lon = st.number_input("Longitude", value=-103.9563, min_value=-105.0, max_value=-100.0, format="%.4f", key="site_lon_simple")
    
    # Determine state from longitude and show appropriate info
    is_new_mexico = site_lon < -103.0
    state_display = "New Mexico" if is_new_mexico else "Texas"
    
    # Show state indicator and groundwater depth dropdown for New Mexico
    if is_new_mexico:
        st.info(f"📍 **Site Location:** {state_display} - Groundwater depth affects regulatory thresholds")
        
        groundwater_depth = st.selectbox(
            "Groundwater Depth at Site",
            options=["50_or_less", "51_to_100", "over_100"],
            format_func=lambda x: {
                "50_or_less": "≤50 feet (strictest thresholds)",
                "51_to_100": "51-100 feet (moderate thresholds)",
                "over_100": ">100 feet (least restrictive thresholds)"
            }[x],
            help="New Mexico regulations vary based on groundwater depth. Shallower groundwater = stricter limits.",
            key="groundwater_depth_simple"
        )
        
        # Show the applicable thresholds based on selection
        nm_thresholds = get_regulatory_thresholds("New Mexico", groundwater_depth)
        st.caption(f"📋 Applicable thresholds: TPH ≤{nm_thresholds['tph_threshold_mgkg']:,} mg/kg, Chloride ≤{nm_thresholds['chloride_threshold_mgkg']:,} mg/kg")
    else:
        st.success(f"📍 **Site Location:** {state_display}")
        groundwater_depth = None  # Not applicable for Texas
    
    st.markdown("---")
    
    # =========================================================================
    # REST OF FORM
    # =========================================================================
    with st.form("simple_form"):
        st.markdown("### 🧪 Contamination Details")
        contam_type = st.selectbox("Contamination Type", 
                                   ["TPH Only", "Chloride Only", "Both TPH and Chloride"])
        
        # Always show both input fields
        col1, col2 = st.columns(2)
        with col1:
            tph_level = st.number_input(
                "TPH Level (mg/kg)", 
                value=1000, 
                min_value=0, 
                max_value=10000,
                help="Enter 0 if not applicable"
            )
        
        with col2:
            chloride_level = st.number_input(
                "Chloride Level (mg/kg)", 
                value=5000, 
                min_value=0, 
                max_value=20000,
                help="Enter 0 if not applicable"
            )
        
        st.markdown("### 🚛 Trucking & Equipment")
        col1, col2 = st.columns(2)
        with col1:
            num_trucks = st.slider(
                "Number of Trucks Available", 
                min_value=1, 
                max_value=10, 
                value=3,
                help="How many trucks can haul soil per day?"
            )
        with col2:
            # Standard equipment assumption with simple toggle
            equipment_size = st.selectbox(
                "Loading Equipment",
                ["Standard (1 excavator + 1 loader)", "Heavy (2 excavators + 2 loaders)"],
                help="Standard equipment can load ~300 CY/day; Heavy can load ~500 CY/day"
            )
        
        # Calculate equipment capacity based on selection
        if equipment_size == "Standard (1 excavator + 1 loader)":
            equipment_capacity_per_day = 300  # CY/day
        else:
            equipment_capacity_per_day = 500  # CY/day
        
        st.markdown("### 🎯 Project Priorities")
        col1, col2, col3 = st.columns(3)
        with col1:
            cost_priority = st.select_slider("Cost Importance", 
                                            options=['low', 'medium', 'high'],
                                            value='medium')
        with col2:
            speed_priority = st.select_slider("Speed Importance",
                                             options=['low', 'medium', 'high'],
                                             value='medium')
        with col3:
            esg_priority = st.select_slider("ESG/Sustainability",
                                           options=['low', 'medium', 'high'],
                                           value='medium')
        
        submitted = st.form_submit_button("🔍 Analyze Solutions", type="primary", use_container_width=True)
        
        if submitted:
            # Adjust contamination levels based on type selection
            final_tph = tph_level if contam_type in ["TPH Only", "Both TPH and Chloride"] else 0
            final_chloride = chloride_level if contam_type in ["Chloride Only", "Both TPH and Chloride"] else 0
            
            # Store in session state
            st.session_state.analysis = {
                'site_lat': site_lat,
                'site_lon': site_lon,
                'groundwater_depth': groundwater_depth,  # None for Texas, category for NM
                'tph_level': final_tph,
                'chloride_level': final_chloride,
                'volume_cy': volume_cy,
                'needs_backfill': needs_backfill,
                'landfill_has_backfill': landfill_has_backfill,
                'extra_backfill_minutes': extra_backfill_minutes,
                'num_trucks': num_trucks,
                'equipment_capacity_per_day': equipment_capacity_per_day,
                'priorities': {
                    'cost': cost_priority,
                    'speed': speed_priority,
                    'esg': esg_priority
                },
                'advanced_params': None,
                'soil_permeability': 'medium'
            }
            st.session_state.show_results = True
            st.rerun()

# ============================================================================
# QUESTIONNAIRE - ADVANCED MODE
# ============================================================================

def show_advanced_questionnaire():
    """Display advanced mode questionnaire"""
    
    st.title("🎛️ Advanced Mode Questionnaire")
    st.markdown("### Detailed Project Specifications")
    st.write("Provide comprehensive information for precise analysis and recommendations.")
    
    # Back button
    if st.button("← Back to Welcome", key="back_advanced"):
        st.session_state.mode = None
        st.rerun()
    
    # =========================================================================
    # SITE LOCATION - Outside form for dynamic state detection
    # =========================================================================
    st.markdown("### 📍 Site Location")
    col1, col2 = st.columns(2)
    with col1:
        site_lat = st.number_input("Latitude", value=31.9, min_value=30.0, max_value=35.0, format="%.4f", key="site_lat_advanced")
    with col2:
        site_lon = st.number_input("Longitude", value=-102.0, min_value=-105.0, max_value=-100.0, format="%.4f", key="site_lon_advanced")
    
    # Determine state from longitude and show appropriate info
    is_new_mexico = site_lon < -103.0
    state_display = "New Mexico" if is_new_mexico else "Texas"
    
    # Show state indicator and groundwater depth dropdown for New Mexico
    if is_new_mexico:
        st.info(f"📍 **Site Location:** {state_display} - Groundwater depth affects regulatory thresholds")
        
        groundwater_depth = st.selectbox(
            "Groundwater Depth at Site",
            options=["50_or_less", "51_to_100", "over_100"],
            format_func=lambda x: {
                "50_or_less": "≤50 feet (strictest thresholds)",
                "51_to_100": "51-100 feet (moderate thresholds)",
                "over_100": ">100 feet (least restrictive thresholds)"
            }[x],
            help="New Mexico regulations vary based on groundwater depth. Shallower groundwater = stricter limits.",
            key="groundwater_depth_advanced"
        )
        
        # Show the applicable thresholds based on selection
        nm_thresholds = get_regulatory_thresholds("New Mexico", groundwater_depth)
        st.caption(f"📋 Applicable thresholds: TPH ≤{nm_thresholds['tph_threshold_mgkg']:,} mg/kg, Chloride ≤{nm_thresholds['chloride_threshold_mgkg']:,} mg/kg")
    else:
        st.success(f"📍 **Site Location:** {state_display}")
        groundwater_depth = None  # Not applicable for Texas
    
    st.markdown("---")
    
    with st.form("advanced_form"):
        st.markdown("### 🧪 Contamination Details")
        contam_type = st.selectbox("Contamination Type", 
                                   ["TPH Only", "Chloride Only", "Both TPH and Chloride"])
        
        col1, col2 = st.columns(2)
        with col1:
            if contam_type in ["TPH Only", "Both TPH and Chloride"]:
                tph_level = st.number_input("TPH Level (mg/kg)", value=1000, min_value=0, max_value=10000)
            else:
                tph_level = 0
        with col2:
            if contam_type in ["Chloride Only", "Both TPH and Chloride"]:
                chloride_level = st.number_input("Chloride Level (mg/kg)", value=5000, min_value=0, max_value=20000)
            else:
                chloride_level = 0
        
        st.markdown("### 📏 Site Dimensions")
        col1, col2 = st.columns(2)
        with col1:
            surface_area = st.number_input("Surface Area (square feet)", value=5000, min_value=100)
        with col2:
            depth = st.number_input("Depth of Contamination (feet)", value=5.0, min_value=0.5, max_value=30.0, step=0.5)
        
        volume_cy = calculate_volume_cy(surface_area, depth)
        st.info(f"📦 **Estimated Volume:** {volume_cy:,.0f} cubic yards")
        
        st.markdown("### 🌍 Soil Characteristics")
        soil_permeability = st.selectbox("Soil Permeability", 
                                        ["high", "medium", "low"],
                                        help="Affects onsite treatment duration")
        
        st.markdown("### 🚜 Equipment & Operations")
        col1, col2, col3 = st.columns(3)
        with col1:
            num_trucks = st.number_input("Number of Trucks", value=3, min_value=1, max_value=10)
            truck_capacity = st.number_input("Truck Capacity (CY)", value=18, min_value=10, max_value=30)
        with col2:
            truck_hourly_rate = st.number_input("Truck Hourly Rate ($)", value=85, min_value=50, max_value=200)
            excavator_rate = st.number_input("Excavator Rate ($/hr)", value=150, min_value=75, max_value=300)
        with col3:
            loader_rate = st.number_input("Loader Rate ($/hr)", value=125, min_value=75, max_value=250)
            work_hours_per_day = st.number_input("Work Hours/Day", value=10, min_value=6, max_value=16)
        
        st.markdown("### 💰 Custom Pricing (Optional)")
        use_custom_pricing = st.checkbox("Override default pricing")
        
        if use_custom_pricing:
            col1, col2, col3 = st.columns(3)
            with col1:
                disposal_cost = st.number_input("Landfill Disposal ($/CY)", value=25, min_value=10, max_value=100)
                backfill_cost = st.number_input("Backfill Cost ($/CY)", value=10, min_value=5, max_value=50)
            with col2:
                onsite_cost = st.number_input("Onsite Processing ($/CY)", value=25, min_value=15, max_value=75)
            with col3:
                surface_cost = st.number_input("Surface Facility ($/CY)", value=25, min_value=15, max_value=75)
        else:
            disposal_cost = 25
            backfill_cost = 10
            onsite_cost = 25
            surface_cost = 25
        
        st.markdown("### 🎯 Project Priorities")
        col1, col2, col3 = st.columns(3)
        with col1:
            cost_priority = st.select_slider("Cost Importance", 
                                            options=['low', 'medium', 'high'],
                                            value='medium')
        with col2:
            speed_priority = st.select_slider("Speed Importance",
                                             options=['low', 'medium', 'high'],
                                             value='medium')
        with col3:
            esg_priority = st.select_slider("ESG/Sustainability",
                                           options=['low', 'medium', 'high'],
                                           value='medium')
        
        needs_backfill = st.checkbox("Clean backfill required", value=True)
        
        submitted = st.form_submit_button("🔍 Analyze Solutions", type="primary", use_container_width=True)
        
        if submitted:
            advanced_params = {
                'truck_capacity_cy': truck_capacity,
                'num_trucks': num_trucks,
                'truck_hourly_rate': truck_hourly_rate,
                'excavator_rate': excavator_rate,
                'loader_rate': loader_rate,
                'work_hours_per_day': work_hours_per_day,
                'disposal_cost_cy': disposal_cost,
                'backfill_cost_cy': backfill_cost,
                'onsite_processing_cost_cy': onsite_cost,
                'surface_processing_cost_cy': surface_cost
            }
            
            st.session_state.analysis = {
                'site_lat': site_lat,
                'site_lon': site_lon,
                'groundwater_depth': groundwater_depth,  # None for Texas, category for NM
                'tph_level': tph_level,
                'chloride_level': chloride_level,
                'volume_cy': volume_cy,
                'needs_backfill': needs_backfill,
                'priorities': {
                    'cost': cost_priority,
                    'speed': speed_priority,
                    'esg': esg_priority
                },
                'advanced_params': advanced_params if use_custom_pricing or True else None,
                'soil_permeability': soil_permeability
            }
            st.session_state.show_results = True
            st.rerun()

# ============================================================================
# RESULTS DISPLAY
# ============================================================================

def show_results():
    """Display analysis results and recommendations"""
    
    analysis = st.session_state.analysis
    db = load_facilities_database()
    
    # Header with Start Over button
    col_title, col_button = st.columns([4, 1])
    with col_title:
        st.markdown("## 🎯 Solution Analysis & Recommendations")
    with col_button:
        if st.button("🔄 Start Over", type="secondary", use_container_width=True):
            # Clear session state and restart
            st.session_state.mode = None
            st.session_state.show_results = False
            st.session_state.analysis = None
            st.rerun()
    
    # ========================================================================
    # LOCATION SUMMARY
    # ========================================================================
    
    st.markdown("### 📍 Location Summary")
    
    # Get location details
    state, county = determine_state_county(analysis['site_lat'], analysis['site_lon'], db)
    soil_type = get_soil_type(analysis['site_lat'], analysis['site_lon'], state)
    groundwater_depth = analysis.get('groundwater_depth', None)  # Get from analysis
    reg_thresholds = get_regulatory_thresholds(state, groundwater_depth)
    
    # Find nearest qualified landfill for distance
    nearest_lf = find_nearest_qualified_landfill(
        analysis['site_lat'], 
        analysis['site_lon'],
        analysis['tph_level'],
        analysis['chloride_level'],
        analysis['needs_backfill'],
        db
    )
    
    if nearest_lf:
        distance_to_landfill = nearest_lf['distance_miles']
        nearest_landfill_name = f"{nearest_lf['landfill']['company']} - {nearest_lf['landfill']['site_name']}"
        distance_display = f"{distance_to_landfill:.1f} mi"
    else:
        distance_to_landfill = None
        nearest_landfill_name = "None found"
        distance_display = "N/A"
    
    # Display location info in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <p class="metric-label">Location</p>
            <p class="metric-value" style="font-size: 1.5rem;">{state}</p>
            <p style="color: #5a8a6f; margin: 0.5rem 0 0 0;">
                <strong>County:</strong> {county}<br>
                <strong>Coordinates:</strong> {analysis['site_lat']:.4f}, {analysis['site_lon']:.4f}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <p class="metric-label">Soil Characteristics</p>
            <p class="metric-value" style="font-size: 1.3rem;">{soil_type}</p>
            <p style="color: #5a8a6f; margin: 0.5rem 0 0 0;">
                <strong>Volume:</strong> {analysis['volume_cy']:,.0f} CY
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <p class="metric-label">Nearest Landfill</p>
            <p class="metric-value" style="font-size: 1.3rem;">{distance_display}</p>
            <p style="color: #5a8a6f; margin: 0.5rem 0 0 0; font-size: 0.85rem;">
                {nearest_landfill_name}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Regulatory information
    with st.expander("📋 Regulatory Thresholds & Standards", expanded=False):
        # Show groundwater depth info for New Mexico
        gw_depth_info = ""
        if state == "New Mexico" and groundwater_depth:
            gw_depth_info = f"""
        **Groundwater Depth:** {reg_thresholds['groundwater_depth_display']}
        """
        
        # Determine threshold compliance
        tph_threshold = reg_thresholds.get('tph_threshold_mgkg', reg_thresholds['tph_industrial_mgkg'])
        chloride_threshold = reg_thresholds.get('chloride_threshold_mgkg', None)
        
        tph_status = '✅ Below threshold' if analysis['tph_level'] <= tph_threshold else '⚠️ Exceeds threshold'
        
        if chloride_threshold:
            chloride_status = '✅ Below threshold' if analysis['chloride_level'] <= chloride_threshold else '⚠️ Exceeds threshold'
        else:
            chloride_status = ''
        
        st.markdown(f"""
        **Regulatory Agency:** {reg_thresholds['regulatory_agency']}
        
        **Regulation Type:** {reg_thresholds.get('regulation_type', 'Guidance')}
        {gw_depth_info}
        **TPH (Total Petroleum Hydrocarbons) Threshold:**
        - {tph_threshold:,} mg/kg
        
        **Chlorides Threshold:**
        - {reg_thresholds['chloride_soil_mgkg']}
        
        **Your Site Contamination Levels:**
        - TPH Level: {analysis['tph_level']:,} mg/kg {tph_status}
        - Chloride Level: {analysis['chloride_level']:,} mg/kg {chloride_status}
        
        *Note: {reg_thresholds['notes']}*
        """)
    
    st.markdown("---")
    
    # ========================================================================
    # PERFORM CALCULATIONS
    # ========================================================================
    
    with st.spinner("Analyzing remediation options..."):
        # Get truck and equipment params (with defaults for backward compatibility)
        num_trucks = analysis.get('num_trucks', 3)
        equipment_capacity_per_day = analysis.get('equipment_capacity_per_day', 300)
        landfill_has_backfill = analysis.get('landfill_has_backfill', False)
        extra_backfill_minutes = analysis.get('extra_backfill_minutes', 0)
        
        dig_haul = calculate_dig_and_haul(
            analysis['volume_cy'],
            analysis['site_lat'],
            analysis['site_lon'],
            analysis['needs_backfill'],
            analysis['tph_level'],
            analysis['chloride_level'],
            db,
            num_trucks=num_trucks,
            equipment_capacity_per_day=equipment_capacity_per_day,
            landfill_has_backfill=landfill_has_backfill,
            extra_backfill_minutes=extra_backfill_minutes,
            advanced_params=analysis['advanced_params']
        )
        
        onsite = calculate_onsite_remediation(
            analysis['volume_cy'],
            analysis['site_lat'],
            analysis['site_lon'],
            analysis.get('soil_permeability', 'medium'),
            analysis['tph_level'],
            analysis['chloride_level'],
            analysis['advanced_params']
        )
        
        surface = calculate_surface_facility(
            analysis['volume_cy'],
            analysis['site_lat'],
            analysis['site_lon'],
            analysis['needs_backfill'],
            analysis['tph_level'],
            analysis['chloride_level'],
            db,
            num_trucks=num_trucks,
            equipment_capacity_per_day=equipment_capacity_per_day,
            advanced_params=analysis['advanced_params']
        )
    
    # Generate recommendation
    recommended, scores = generate_recommendation(dig_haul, onsite, surface, analysis['priorities'])
    
    # ========================================================================
    # COMPARISON TABLE
    # ========================================================================
    
    st.markdown("### 📊 Solution Comparison")
    
    # Build options list
    options_list = []
    if dig_haul:
        options_list.append(('dig_haul', dig_haul))
    if onsite:
        options_list.append(('onsite', onsite))
    if surface:
        options_list.append(('surface', surface))
    
    # Create comprehensive comparison dataframe
    comparison_data = []
    for opt_type, opt in options_list:
        is_recommended = (opt_type == recommended)
        
        # Build key details string
        if opt_type == 'dig_haul':
            key_details = f"→ {opt['landfill_name']}\n({opt['distance_miles']:.0f} mi)"
            if not opt.get('backfill_available_at_landfill') and analysis.get('needs_backfill', True):
                extra_mins = opt.get('extra_backfill_minutes', 0)
                if extra_mins > 0:
                    key_details += f"\n⚠️ +{extra_mins} min/trip for backfill"
                else:
                    key_details += "\n⚠️ Separate backfill source"
            disposal_liability = "Permanent"
        elif opt_type == 'onsite':
            key_details = "Treated on your site\nSoil stays in place"
            disposal_liability = "None"
        else:  # surface
            key_details = f"→ {opt['facility_name']}\n({opt['distance_miles']:.0f} mi)"
            disposal_liability = "None"
        
        row = {
            '': '⭐ RECOMMENDED' if is_recommended else '',
            'Solution': opt['option_name'].replace('Clean Futures ', 'CF '),
            'Total Cost': f"${opt['total_cost']:,.0f}",
            'Cost/CY': f"${opt['cost_per_cy']:.2f}",
            'Timeline': f"{opt['project_days']} days",
            'CO₂': f"{opt['co2_tons']:.1f} tons",
            'Backfill': '✅ Included' if opt.get('includes_backfill', False) else '❌ Separate',
            'Liability': disposal_liability,
            'Details': key_details
        }
        
        comparison_data.append(row)
    
    df_comparison = pd.DataFrame(comparison_data)
    
    # Display table with custom styling
    st.dataframe(
        df_comparison,
        hide_index=True,
        use_container_width=True,
        column_config={
            '': st.column_config.TextColumn(label="", width="small"),
            'Solution': st.column_config.TextColumn(width="medium"),
            'Total Cost': st.column_config.TextColumn(width="small"),
            'Cost/CY': st.column_config.TextColumn(width="small"),
            'Timeline': st.column_config.TextColumn(width="small"),
            'CO₂': st.column_config.TextColumn(width="small"),
            'Backfill': st.column_config.TextColumn(width="small"),
            'Liability': st.column_config.TextColumn(width="small"),
            'Details': st.column_config.TextColumn(width="large"),
        }
    )
    
    # Add recommendation callout below the table
    st.markdown("---")
    
    # Show which option is recommended with explanation
    rec_opt = next((opt for opt_type, opt in options_list if opt_type == recommended), None)
    if rec_opt:
        rec_name = rec_opt['option_name']
        st.success(f"**⭐ Recommended Solution: {rec_name}** — Best match for your stated priorities (Cost: {analysis['priorities']['cost']}, Speed: {analysis['priorities']['speed']}, ESG: {analysis['priorities']['esg']})")
    
    st.markdown("---")
    
    # ========================================================================
    # DETAILED BREAKDOWNS
    # ========================================================================
    
    st.markdown("### 💰 Detailed Cost Breakdowns")
    
    col1, col2, col3 = st.columns(3)
    
    for idx, (opt_type, opt) in enumerate(options_list):
        col = [col1, col2, col3][idx]
        is_recommended = (opt_type == recommended)
        
        with col:
            if is_recommended:
                st.markdown('<div class="recommended-badge">⭐ RECOMMENDED</div>', unsafe_allow_html=True)
            
            st.markdown(f"**{opt['option_name']}**")
            
            if opt_type == 'dig_haul':
                breakdown = {
                    'Equipment': f"${opt['equipment_cost']:,.0f}",
                    'Trucking': f"${opt['trucking_cost']:,.0f}",
                    'Disposal': f"${opt['disposal_cost']:,.0f}",
                    'Backfill': f"${opt['backfill_cost']:,.0f}",
                }
                # Show bottleneck
                st.caption(f"⚡ Bottleneck: **{opt.get('bottleneck', 'N/A')}** ({opt.get('actual_daily_capacity', 0):.0f} CY/day)")
            elif opt_type == 'onsite':
                # Simple mode shows flat rate
                if opt['mobilization_cost'] == 0 and opt['amendment_cost'] == 0:
                    breakdown = {
                        f"Flat Rate (${opt.get('rate_per_cy', 30)}/CY)": f"${opt['processing_cost']:,.0f}",
                    }
                else:
                    breakdown = {
                        'Processing': f"${opt['processing_cost']:,.0f}",
                        'Mobilization': f"${opt['mobilization_cost']:,.0f}",
                        'Amendments': f"${opt['amendment_cost']:,.0f}",
                    }
            else:  # surface
                breakdown = {
                    'Equipment': f"${opt.get('equipment_cost', 0):,.0f}",
                    'Trucking': f"${opt['trucking_cost']:,.0f}",
                    'Processing': f"${opt['processing_cost']:,.0f}",
                }
                # Show bottleneck
                st.caption(f"⚡ Bottleneck: **{opt.get('bottleneck', 'N/A')}** ({opt.get('actual_daily_capacity', 0):.0f} CY/day)")
            
            for category, cost in breakdown.items():
                st.write(f"• {category}: {cost}")
            
            st.markdown(f"**Total: ${opt['total_cost']:,.0f}**")
    
    st.markdown("---")
    
    # ========================================================================
    # HOW COSTS WERE CALCULATED
    # ========================================================================
    
    st.markdown("### 📐 How Costs Were Calculated")
    
    with st.expander("**Dig & Haul to Landfill** - Calculation Details", expanded=False):
        dh = dig_haul
        if dh:
            # Determine backfill source info
            extra_bf_mins = dh.get('extra_backfill_minutes', 0)
            if analysis.get('needs_backfill', True):
                if dh.get('backfill_available_at_landfill', False):
                    backfill_source = "✅ At landfill (no extra trip)"
                    extra_time_note = ""
                else:
                    backfill_source = "⚠️ Separate source required"
                    extra_time_note = f" + **{extra_bf_mins} min backfill pickup**" if extra_bf_mins > 0 else ""
            else:
                backfill_source = "Not required"
                extra_time_note = ""
            
            st.markdown(f"""
**Parameters Used:**
| Parameter | Value |
|-----------|-------|
| Volume | {analysis['volume_cy']:,.0f} CY |
| Distance to Landfill | {dh['distance_miles']:.1f} miles |
| Truck Capacity | 18 CY |
| Number of Trucks | {dh.get('num_trucks', 3)} |
| Equipment Capacity | {analysis.get('equipment_capacity_per_day', 300)} CY/day |
| Truck Hourly Rate | $85/hr |
| Excavator Rate | $150/hr |
| Loader Rate | $125/hr |
| Work Hours/Day | 10 hours |
| Travel Speed | 45 mph |
| Disposal Cost | $25/CY |
| Backfill Cost | $10/CY |
| **Backfill Source** | **{backfill_source}** |

**Step-by-Step Calculation:**

1. **Trip Time:**
   - Travel time (one way) = {dh['distance_miles']:.1f} mi ÷ 45 mph = {dh['distance_miles']/45:.2f} hours
   - Base trip = Load (0.25 hr) + Travel ({dh['distance_miles']/45:.2f} hr) + Unload (0.5 hr) + Return ({dh['distance_miles']/45:.2f} hr) + Unload backfill (0.25 hr)
   - Base trip time = {dh.get('base_trip_time_hours', dh.get('trip_time_hours', 0)):.2f} hours{extra_time_note}
   - **Total trip time = {dh.get('trip_time_hours', 0):.2f} hours**

2. **Bottleneck Analysis:**
   - Truck capacity/day = {10/dh.get('trip_time_hours', 1):.1f} trips/truck × {dh.get('num_trucks', 3)} trucks × 18 CY = **{dh.get('truck_capacity_per_day', 0):.0f} CY/day**
   - Equipment capacity/day = **{dh.get('equipment_capacity_per_day', 300):.0f} CY/day** (based on your selection)
   - ⚡ **BOTTLENECK: {dh.get('bottleneck', 'N/A')}** → Actual daily capacity = **{dh.get('actual_daily_capacity', 0):.0f} CY/day**

3. **Duration:**
   - Project days = {analysis['volume_cy']:,.0f} CY ÷ {dh.get('actual_daily_capacity', 1):.0f} CY/day = **{dh['project_days']} days**
   - Number of trips = {dh.get('num_trips', 0)} trips

4. **Costs:**
   - Equipment = ($150 + $125) × {dh['project_days']} days × 10 hrs = **${dh['equipment_cost']:,.0f}**
   - Trucking = {dh.get('num_trips', 0)} trips × {dh.get('trip_time_hours', 0):.2f} hrs × $85/hr = **${dh['trucking_cost']:,.0f}**
   - Disposal = {analysis['volume_cy']:,.0f} CY × $25 = **${dh['disposal_cost']:,.0f}**
   - Backfill = {analysis['volume_cy']:,.0f} CY × $10 = **${dh['backfill_cost']:,.0f}**

5. **TOTAL = ${dh['total_cost']:,.0f}** (${dh['cost_per_cy']:.2f}/CY)

6. **CO₂ Emissions:** {dh['co2_tons']:.2f} tons
   {f"   - *Includes {dh.get('extra_backfill_co2_tons', 0):.2f} tons from backfill sourcing trips*" if extra_bf_mins > 0 else ""}
            """)
        else:
            st.write("No qualified landfill found for this contamination level.")
    
    with st.expander("**Clean Futures Onsite Remediation** - Calculation Details", expanded=False):
        os = onsite
        if os:
            st.markdown(f"""
**Simple Mode Calculation:**

In simple mode, onsite remediation uses a **flat all-inclusive rate of $30.00 per cubic yard**.

This rate includes:
- Mobilization/demobilization
- Treatment equipment
- Labor
- Soil amendments
- Testing and verification
- Clean soil returned in place (no backfill purchase needed)

**Calculation:**
- Volume: {analysis['volume_cy']:,.0f} CY
- Rate: $30.00/CY
- **TOTAL = {analysis['volume_cy']:,.0f} × $30.00 = ${os['total_cost']:,.0f}**

**Timeline Estimate:**
- Base treatment duration: 45 days (medium permeability soil)
- Adjusted for soil type and contamination levels
- **Estimated duration: {os['project_days']} days**

**CO₂ Emissions:**
- Estimated at 0.1 gallons fuel per CY (minimal equipment, no trucking)
- **{os['co2_tons']:.2f} tons CO₂**

*Note: Advanced mode allows detailed breakdown of mobilization, amendments, and processing costs.*
            """)
    
    with st.expander("**Clean Futures Surface Facility** - Calculation Details", expanded=False):
        sf = surface
        if sf:
            st.markdown(f"""
**How Surface Facilities Work:**

Unlike landfills, Clean Futures Surface Facilities provide **immediate backfill exchange**:
1. Operator arrives with contaminated soil
2. Drops off contaminated soil
3. **Picks up clean backfill** (from previously treated stockpile)
4. Returns to site with clean backfill
5. ✅ **Done!** No waiting for treatment.

Clean Futures treats the dropped-off soil behind the scenes and adds it to the stockpile for future use.

---

**Parameters Used:**
| Parameter | Value |
|-----------|-------|
| Volume | {analysis['volume_cy']:,.0f} CY |
| Distance to Facility | {sf['distance_miles']:.1f} miles |
| Truck Capacity | 18 CY |
| Number of Trucks | {sf.get('num_trucks', 3)} |
| Equipment Capacity | {analysis.get('equipment_capacity_per_day', 300)} CY/day |
| Truck Hourly Rate | $85/hr |
| Excavator Rate | $150/hr |
| Loader Rate | $125/hr |
| Processing Cost | $25/CY |
| Travel Speed | 45 mph |

**Step-by-Step Calculation:**

1. **Trip Time:**
   - Travel time (one way) = {sf['distance_miles']:.1f} mi ÷ 45 mph = {sf['distance_miles']/45:.2f} hours
   - Trip = Load at site (0.25 hr) + Travel ({sf['distance_miles']/45:.2f} hr) + Exchange at facility (0.5 hr) + Return ({sf['distance_miles']/45:.2f} hr) + Unload backfill (0.25 hr)
   - **Total trip time = {sf.get('trip_time_hours', 0):.2f} hours**

2. **Bottleneck Analysis:**
   - Truck capacity/day = {10/sf.get('trip_time_hours', 1):.1f} trips/truck × {sf.get('num_trucks', 3)} trucks × 18 CY = **{sf.get('truck_capacity_per_day', 0):.0f} CY/day**
   - Equipment capacity/day = **{sf.get('equipment_capacity_per_day', 300):.0f} CY/day**
   - ⚡ **BOTTLENECK: {sf.get('bottleneck', 'N/A')}** → Actual daily capacity = **{sf.get('actual_daily_capacity', 0):.0f} CY/day**

3. **Timeline:**
   - Project days = {analysis['volume_cy']:,.0f} CY ÷ {sf.get('actual_daily_capacity', 1):.0f} CY/day = **{sf['project_days']} days**
   - ✅ **No treatment wait** - backfill picked up same trip!

4. **Costs:**
   - Equipment (loading) = ($150 + $125) × {sf['project_days']} days × 10 hrs = **${sf.get('equipment_cost', 0):,.0f}**
   - Trucking = {sf.get('num_trips', 0)} trips × {sf.get('trip_time_hours', 0):.2f} hrs × $85/hr = **${sf['trucking_cost']:,.0f}**
   - Processing = {analysis['volume_cy']:,.0f} CY × $25/CY = **${sf['processing_cost']:,.0f}**

5. **TOTAL = ${sf['total_cost']:,.0f}** (${sf['cost_per_cy']:.2f}/CY)

**Advantages over Landfill:**
- ✅ Same timeline as Dig & Haul (just hauling days)
- ✅ Backfill included - no separate sourcing needed
- ✅ No long-term disposal liability
- ✅ Environmentally friendly (soil treated, not buried)
            """)
        else:
            st.write("No Clean Futures facility found.")
    
    st.markdown("---")
    
    # ========================================================================
    # PROS & CONS
    # ========================================================================
    
    st.markdown("### ✅ ⚠️ Advantages & Considerations")
    
    col1, col2, col3 = st.columns(3)
    
    pros_cons = {
        'dig_haul': {
            'pros': [
                'Fast execution',
                'Immediate removal',
                'No onsite disruption',
                'Predictable timeline'
            ],
            'cons': [
                'Highest carbon footprint',
                'Permanent disposal liability',
                'Backfill coordination needed',
                'Distance-dependent costs'
            ]
        },
        'onsite': {
            'pros': [
                'Lowest carbon footprint',
                'Original soil retained',
                'No disposal liability',
                'Cost-effective for large volumes',
                'Sustainable solution'
            ],
            'cons': [
                'Longer timeline',
                'Weather dependent',
                'Space requirements',
                'Ongoing site presence'
            ]
        },
        'surface': {
            'pros': [
                'Same fast timeline as landfill',
                'Backfill included (pick up same trip)',
                'No disposal liability',
                'No backfill sourcing hassle',
                'Environmentally friendly',
                'Single vendor solution'
            ],
            'cons': [
                'Transportation both ways',
                'Processing fee applies',
                'Facility must be nearby'
            ]
        }
    }
    
    for idx, (opt_type, opt) in enumerate(options_list):
        col = [col1, col2, col3][idx]
        
        with col:
            st.markdown(f"**{opt['option_name']}**")
            
            st.markdown('<div class="pros-list">', unsafe_allow_html=True)
            st.markdown("**✅ Advantages**")
            for pro in pros_cons[opt_type]['pros']:
                st.markdown(f"• {pro}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("")
            
            st.markdown('<div class="cons-list">', unsafe_allow_html=True)
            st.markdown("**⚠️ Considerations**")
            for con in pros_cons[opt_type]['cons']:
                st.markdown(f"• {con}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # RECOMMENDATION EXPLANATION
    # ========================================================================
    
    st.markdown("### 💡 Why This Recommendation?")
    
    if recommended == 'dig_haul':
        st.info("""
            **Dig & Haul** is recommended for your project because:
            - Fast execution meets your timeline needs
            - Volume and distance make trucking economical
            - Immediate site remediation is prioritized
            - Landfill proximity makes this cost-effective
        """)
    elif recommended == 'onsite':
        st.success("""
            **Onsite Remediation** is recommended for your project because:
            - Excellent cost-effectiveness for your volume
            - Lowest environmental impact (CO₂ emissions)
            - Original soil retained, reducing waste
            - No long-term disposal liability
            - Sustainable approach aligns with ESG goals
            - Treatment duration is acceptable for your timeline priorities
        """)
    else:  # surface
        st.success("""
            **Surface Facility** is recommended for your project because:
            - Fast execution (same as Dig & Haul - no treatment wait!)
            - Backfill included - pick up clean soil on the same trip
            - No backfill sourcing hassle or coordination
            - No long-term disposal liability (soil treated, not buried)
            - Environmentally friendly alternative to landfill
            - Facility proximity makes this cost-effective
        """)
    
    # ========================================================================
    # DOWNLOAD & RESTART
    # ========================================================================
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create downloadable report
        report_data = []
        for opt_type, opt in options_list:
            report_data.append({
                'Solution': opt['option_name'],
                'Recommended': 'Yes' if opt_type == recommended else 'No',
                'Total_Cost': opt['total_cost'],
                'Cost_Per_CY': opt['cost_per_cy'],
                'Project_Days': opt['project_days'],
                'CO2_Tons': opt['co2_tons'],
                'Includes_Backfill': 'Yes' if opt.get('includes_backfill', False) else 'No'
            })
        
        df_report = pd.DataFrame(report_data)
        csv = df_report.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Report (CSV)",
            data=csv,
            file_name=f"clean_futures_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔄 Start Over", use_container_width=True, key="start_over_bottom"):
            st.session_state.mode = None
            st.session_state.show_results = False
            st.session_state.analysis = None
            st.rerun()

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application"""
    
    # Initialize session state
    if 'mode' not in st.session_state:
        st.session_state.mode = None
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    
    # Show appropriate page
    if st.session_state.show_results:
        show_results()
    elif st.session_state.mode == 'simple':
        show_simple_questionnaire()
    elif st.session_state.mode == 'advanced':
        show_advanced_questionnaire()
    else:
        show_welcome_page()
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
        <div style='text-align: center; color: #5a8a6f; padding: 2rem 0;'>
            <p style='margin: 0; font-family: "Crimson Pro", serif; font-size: 1.2rem;'>
                <strong>Clean Futures</strong> | Making Our World Better and Cleaner
            </p>
            <p style='margin: 0.5rem 0 0 0; font-family: "Work Sans", sans-serif; font-size: 0.9rem;'>
                Permian Basin Solution Recommendation Tool | v{APP_VERSION}
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
