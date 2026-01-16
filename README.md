# UIDAI State-Citizen Friction Intelligence System

A comprehensive analytical system for extracting policy intelligence from UIDAI's administrative datasets to identify friction points in state-citizen interactions and provide actionable recommendations.

## Overview

This system transforms raw interaction data (enrolments, demographic updates, biometric updates) into actionable friction diagnostics that enable precision governance. Every metric answers: "Where is friction? What does it cost? How do we fix it?"

## Project Structure

```
.
├── src/
│   ├── data_quality/       # Data cleaning, validation, and standardization
│   ├── features/           # Feature engineering and derived metrics
│   ├── detection/          # Friction detection modules
│   ├── visualization/      # Charts, maps, and visual analytics
│   ├── reporting/          # PDF report generation
│   └── utils/              # Shared utilities and constants
│       ├── constants.py    # Thresholds, cost estimates, parameters
│       └── helpers.py      # Common utility functions
├── archive/                # Raw data files
│   ├── api_data_aadhar_enrolment/
│   ├── api_data_aadhar_demographic/
│   └── api_data_aadhar_biometric/
├── output/                 # Generated outputs (created at runtime)
│   ├── cleaned/
│   ├── features/
│   ├── friction_reports/
│   ├── visualizations/
│   └── logs/
├── config.yaml             # Configuration file
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

1. **Clone the repository** (or ensure you're in the project directory)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.yaml` to customize:
- Data file paths
- Analysis parameters
- Friction detection thresholds
- Cost estimates
- Visualization settings
- Report structure

## Usage

### Basic Analysis Pipeline

```python
# Import modules
from src.data_quality import cleaning
from src.features import engineering
from src.detection import infrastructure, access, biometric
from src.visualization import charts
from src.reporting import generator

# 1. Load and clean data
enrolment_df = cleaning.load_and_clean('enrolment')
demographic_df = cleaning.load_and_clean('demographic')
biometric_df = cleaning.load_and_clean('biometric')

# 2. Engineer features
features_df = engineering.create_features(enrolment_df, demographic_df, biometric_df)

# 3. Detect friction points
infrastructure_friction = infrastructure.detect(features_df)
access_friction = access.detect(features_df)
biometric_friction = biometric.detect(features_df)

# 4. Generate visualizations
charts.create_all_visualizations(features_df, infrastructure_friction, access_friction)

# 5. Generate report
generator.create_pdf_report(output_path='output/UIDAI_Friction_Intelligence_Report.pdf')
```

## Key Features

### Friction Detection Modules

1. **Infrastructure Stress Detector**: Identifies capacity mismatches
2. **Access Failure Detector**: Distinguishes low demand from access barriers
3. **Age Structure Analyzer**: Provides demographic pressure forecasts
4. **Migration Signal Detector**: Detects population movement patterns
5. **Data Quality Debt Quantifier**: Calculates cost of poor data quality
6. **Biometric Stress Analyzer**: Identifies authentication challenges
7. **Anomaly Detector**: Flags unusual spikes or drops in activity

### Analytical Capabilities

- **Cross-dataset triangulation**: Validates hypotheses across multiple data sources
- **Economic impact estimation**: Calculates costs and ROI for interventions
- **Budget prioritization**: Ranks districts by service pressure
- **Actionable recommendations**: Specific interventions with timelines and ownership

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run property-based tests only
pytest -k "property"

# Run specific module tests
pytest tests/test_data_quality.py
```

## Output

The system generates:
- **Cleaned datasets**: Standardized and validated data
- **Feature matrices**: Derived metrics for analysis
- **Friction reports**: JSON/CSV files with detected friction points
- **Visualizations**: Charts, maps, and graphs
- **PDF Report**: Comprehensive 25-35 page report with:
  - Executive summary
  - 7 core analytical sections
  - District-level prioritization matrices
  - Economic impact estimates
  - Implementation roadmap

## Development

### Adding New Friction Detectors

1. Create a new module in `src/detection/`
2. Implement detection logic following the pattern:
   ```python
   def detect(features_df, thresholds):
       # Detection logic
       return friction_events_df
   ```
3. Add configuration to `config.yaml`
4. Write property-based tests in `tests/`

### Adding New Visualizations

1. Add visualization function to `src/visualization/`
2. Follow design principles:
   - One insight per chart
   - Actionable titles
   - Colorblind-friendly palettes
   - Professional aesthetics

## Team Structure

- **Member 1**: Data Quality & Infrastructure Stress
- **Member 2**: Access Failure & Age Structure Analysis
- **Member 3**: Migration & Data Quality Debt
- **Member 4**: Biometric Stress & Anomaly Detection
- **Member 5**: Visualization & Report Generation (integrator role)

## Requirements Traceability

This implementation addresses requirements 8.1-8.5:
- **8.1**: Budget prioritization and composite friction scoring
- **8.2**: District ranking by service pressure
- **8.3**: Underutilized center identification
- **8.4**: Cost-per-interaction metrics
- **8.5**: Budget allocation recommendations with impact estimates

## License

[Specify license here]

## Contact

[Specify contact information here]

## Acknowledgments

Built for the UIDAI Hackathon to enable precision governance through data-driven friction analysis.
