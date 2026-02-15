"""
c3_core.etl

ETL component for NeuroTransAnalytics-v4.
Responsible for extracting data from SQLite and normalizing it into EventFrames.
"""

from .etl_v4 import ETLPipeline

__all__ = ["ETLPipeline"]
