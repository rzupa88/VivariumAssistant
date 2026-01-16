from __future__ import annotations

from pathlib import Path
import yaml

from packages.core.config_schema import EnclosureConfig, ProfileConfig

REPO_ROOT = Path(__file__).resolve().parents[2]

def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping at {path}")
    return data

def load_enclosure(enclosure_id: str) -> EnclosureConfig:
    path = REPO_ROOT / "config" / "enclosures" / f"{enclosure_id}.yaml"
    return EnclosureConfig.model_validate(_load_yaml(path))

def load_profile(profile_id: str) -> ProfileConfig:
    path = REPO_ROOT / "config" / "profiles" / f"{profile_id}.yaml"
    return ProfileConfig.model_validate(_load_yaml(path))
