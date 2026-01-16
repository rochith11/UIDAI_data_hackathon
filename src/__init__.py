"""
UIDAI State-Citizen Friction Intelligence System

A comprehensive analytical system for extracting policy intelligence from UIDAI's
administrative datasets (Enrolment, Demographic Updates, Biometric Updates).

Modules:
    - data_quality: Data cleaning, validation, and standardization
    - features: Feature engineering and derived metrics
    - detection: Friction detection modules (infrastructure, access, biometric, etc.)
    - visualization: Charts, maps, and visual analytics
    - reporting: PDF report generation
    - utils: Shared utilities, constants, and helper functions
"""

__version__ = "0.1.0"
__author__ = "UIDAI Hackathon Team"

# Import key components for easy access
from src.utils import constants, helpers

__all__ = ['constants', 'helpers']
