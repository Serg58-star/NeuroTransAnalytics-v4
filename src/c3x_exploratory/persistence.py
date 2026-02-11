"""
c3x_exploratory.persistence

This module implements the deterministic artifact persistence layer for 
C3.x exploratory procedures. It handles JSON serialization, artifact 
hashing, and file management.
"""

import os
import json
import hashlib
import datetime
from dataclasses import asdict
from typing import Any, Dict

# Import all result classes for reconstruction
from src.shared.artifacts import DistributionStructureResult, TemporalStructureResult

# Root directory for artifacts
ARTIFACT_ROOT = "artifacts/exploratory"


def _parameter_hash(parameters: Dict[str, Any]) -> str:
    """
    Computes a deterministic 6-character SHA256 hash of parameters.
    """
    # Sort keys for determinism
    encoded = json.dumps(parameters, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:6]


class ArtifactEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle non-serializable types.
    """
    def default(self, obj):
        # Already handled by asdict most of the time, but for direct use:
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        try:
            import numpy as np
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, (np.int64, np.int32)):
                return int(obj)
            if isinstance(obj, (np.float64, np.float32)):
                return float(obj)
        except ImportError:
            pass
        return super().default(obj)


def save_artifact(artifact: Any) -> str:
    """
    Saves a C3.x artifact as a deterministic JSON file.
    
    Returns:
        str: Absolute or relative path to the saved file.
    """
    procedure_name = artifact.procedure_name
    params = artifact.input_parameters
    
    # 1. Prepare directory
    dir_path = os.path.join(ARTIFACT_ROOT, procedure_name)
    os.makedirs(dir_path, exist_ok=True)
    
    # 2. Compute filename components
    # Use the timestamp already present in the artifact, or now()
    ts_raw = getattr(artifact, "timestamp", datetime.datetime.now().isoformat())
    # Task 10 requires ISO format without microseconds and specific delimiter
    try:
        ts_obj = datetime.datetime.fromisoformat(ts_raw)
        ts_str = ts_obj.strftime("%Y-%m-%dT%H-%M-%S")
    except ValueError:
        ts_str = ts_raw.replace(":", "-").split(".")[0]
        
    param_hash = _parameter_hash(params)
    filename = f"{ts_str}_{param_hash}.json"
    filepath = os.path.join(dir_path, filename)
    
    # 3. Serialize and Save
    data = asdict(artifact)
    
    # Explicitly ensure timestamp matches the filename precision if it was updated
    # but requirement 10.7 says "No mutation of original artifact". 
    # We will just write what we have.
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, cls=ArtifactEncoder, indent=4)
        
    return filepath


def load_artifact(filepath: str) -> Any:
    """
    Loads and reconstructs a C3.x artifact from a JSON file.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Artifact not found: {filepath}")
        
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    procedure_name = data.get("procedure_name")
    
    # Reconstruction map
    reconstructors = {
        "MultimodalityDetection": DistributionStructureResult,
        "ChangePointDetection": TemporalStructureResult
    }
    
    if procedure_name not in reconstructors:
        raise ValueError(f"Unknown procedure in artifact: {procedure_name}")
        
    cls = reconstructors[procedure_name]
    
    # Validation
    if "procedure_version" not in data or not data["procedure_version"]:
        raise ValueError(f"Artifact version missing in {filepath}")
        
    return cls(**data)
