# Clean Futures Solution Recommendation Tool

## Overview

An intelligent decision support system for soil remediation in the Permian Basin. This tool compares three remediation approaches and provides data-driven recommendations based on your specific project parameters.

## Three Remediation Options Analyzed

1. **Dig & Haul to Landfill** - Excavate contaminated soil, transport to qualified landfill, replace with clean backfill
2. **Clean Futures Onsite Remediation** - Treat soil in place using proven remediation methods
3. **Clean Futures Surface Facility Treatment** - Transport to facility for treatment, return clean soil to site

## Features

### Two Operating Modes

**Simple Mode** - Quick estimates with minimal input
- Basic site information (GPS, contamination type/levels, dimensions)
- Standard assumptions for equipment and costs
- Fast preliminary recommendations
- Perfect for initial planning and budgeting

**Advanced Mode** - Detailed analysis with custom parameters
- Comprehensive site data including soil permeability
- Custom equipment specifications and pricing
- Precise recommendations with full control
- Ideal for final decision-making

### Comprehensive Analysis

- **Cost Breakdown** - Detailed costs for equipment, trucking, disposal, processing, and backfill
- **Timeline Estimates** - Project duration from mobilization to completion
- **Environmental Impact** - CO2 emissions calculated for each option
- **Distance Calculations** - Automatic routing to nearest qualified facilities
- **Smart Recommendations** - AI-powered suggestions based on your priorities (cost, speed, ESG)

### Database Features

- **14 Qualified Landfills** across the Permian Basin with acceptance criteria
- **4 Clean Futures Surface Facilities** strategically located
- **Easily Editable JSON Database** - Update facilities, costs, and parameters as needed
- **Geographic Optimization** - Finds nearest qualified facility based on GPS coordinates

## Installation & Setup

### Requirements

```bash
pip install streamlit pandas plotly --break-system-packages
```

### File Structure

```
clean_futures_recommendation_tool.py    # Main application
permian_facilities_db.json              # Facilities database (editable)
```

### Running the Application

```bash
streamlit run clean_futures_recommendation_tool.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

### Step 1: Choose Your Mode
- Select **Simple Mode** for quick estimates
- Select **Advanced Mode** for detailed analysis

### Step 2: Enter Project Information
- **GPS Coordinates** - Site location (lat/lon)
- **Contamination Type** - TPH, Chloride, or Both
- **Contamination Levels** - Concentrations in mg/kg
- **Site Dimensions** - Surface area (sq ft) and depth (ft)

### Step 3: Set Priorities
- **Cost Importance** - Low, Medium, or High
- **Speed Importance** - Low, Medium, or High
- **ESG/Sustainability** - Low, Medium, or High

### Step 4: Advanced Options (Advanced Mode Only)
- Custom equipment specifications
- Override default pricing
- Soil permeability characteristics
- Operations parameters

### Step 5: Review Results
- Compare all three options side-by-side
- Review detailed cost breakdowns
- Examine pros and cons
- Download comprehensive CSV report

## Understanding the Results

### Cost Metrics
- **Total Cost** - Complete project cost including all components
- **Cost per CY** - Unit cost for easy comparison
- **Cost Breakdown** - Detailed itemization by category

### Timeline
- **Project Days** - Estimated duration from start to completion
- Factors in equipment capacity, transportation, and treatment duration

### Environmental Impact
- **CO2 Emissions** - Total carbon footprint in tons
- Calculated from fuel consumption across all equipment and vehicles
- Includes excavation, trucking, and onsite operations

### Recommendation Logic

The tool scores each option based on your stated priorities:

- **High Cost Priority** → Recommends lowest cost option
- **High Speed Priority** → Recommends fastest timeline
- **High ESG Priority** → Recommends lowest CO2 and sustainable treatment

The algorithm balances multiple factors to provide the best overall recommendation for your unique situation.

## Database Customization

### Editing `permian_facilities_db.json`

The database is structured in two main sections:

#### Landfills
```json
{
  "id": "LF001",
  "company": "COMPANY NAME",
  "site_name": "SITE NAME",
  "county": "COUNTY",
  "latitude": 31.499316,
  "longitude": -101.931524,
  "accepts_tph": true,
  "tph_max_mgkg": 5000,
  "accepts_chloride": true,
  "chloride_max_mgkg": 10000,
  "disposal_cost_cy": 25,
  "backfill_available": true,
  "backfill_cost_cy": 10
}
```

#### Clean Futures Facilities
```json
{
  "id": "CF001",
  "facility_name": "Clean Futures Facility 1",
  "region": "Delaware Basin",
  "latitude": 31.9195,
  "longitude": -103.6285,
  "processing_cost_cy": 25,
  "includes_backfill": true,
  "backfill_cost_cy": 0,
  "typical_turnaround_days": 30,
  "notes": "Treated soil returned to site"
}
```

### Adding New Facilities

1. Open `permian_facilities_db.json` in a text editor
2. Add new entry to "landfills" or "clean_futures_facilities" array
3. Follow the existing structure
4. Save and restart the application

## Default Assumptions (Simple Mode)

- **Trucks:** 3 trucks at 18 CY capacity each
- **Equipment:** Standard excavator (150 $/hr) and loader (125 $/hr)
- **Work Schedule:** 10 hours per day
- **Disposal Cost:** $25/CY
- **Backfill Cost:** $10/CY
- **Processing Cost:** $25/CY for both onsite and surface facility
- **Soil Permeability:** Medium (affects onsite treatment duration)

All assumptions can be customized in Advanced Mode.

## Technical Details

### Distance Calculations
- Uses Haversine formula for accurate GPS distance calculations
- Accounts for Earth's curvature
- Returns distances in miles

### Volume Calculations
```
Volume (CY) = (Surface Area sq ft × Depth ft) / 27
```

### CO2 Calculations
```
CO2 (lbs) = Fuel Gallons × 22.38 lbs CO2/gallon
CO2 (tons) = CO2 (lbs) / 2000
```

### Trip Time Calculations
- Factors in loading time, travel time (both directions), and unloading time
- Assumes average speed of 45 mph for highway travel
- Includes wait time at landfills/facilities

## Pros & Cons Summary

### Dig & Haul
**Pros:** Fast execution, immediate removal, no onsite disruption, predictable timeline
**Cons:** Highest carbon footprint, disposal liability, backfill coordination, distance-dependent

### Onsite Remediation
**Pros:** Lowest CO2, original soil retained, no disposal liability, cost-effective for large volumes, sustainable
**Cons:** Longer timeline, weather dependent, space requirements, ongoing site presence

### Surface Facility
**Pros:** Clean soil returned, controlled environment, no disposal liability, single vendor, good for complex contamination
**Cons:** Transportation costs (both ways), facility scheduling, moderate timeline

## Future Enhancements

Potential features for future versions:
- Real-time landfill availability checking
- Integration with soil testing databases
- Regulatory compliance verification
- Multi-site project planning
- Gantt chart timeline visualization
- Mobile app version
- Expansion to other geographic regions

## Support & Contact

For questions, updates, or custom features:
- Update facility database as needed
- Adjust default parameters in code
- Contact Clean Futures for technical support

## Version History

**v1.0** - Initial Release
- Simple and Advanced modes
- 14 Permian Basin landfills
- 4 Clean Futures facilities
- Full cost, timeline, and CO2 analysis
- Smart recommendation engine
- Downloadable reports

---

**Clean Futures** | Making Our World Better and Cleaner
