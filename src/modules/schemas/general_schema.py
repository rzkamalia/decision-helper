import os
from dataclasses import dataclass, fields
from typing import Any

from langchain_core.runnables import RunnableConfig


@dataclass(kw_only=True)
class Configuration:
    user_id: str  # Required

    @classmethod
    def from_runnable_config(cls, config: RunnableConfig) -> "Configuration":
        """Create a Configuration object from a RunnableConfig object.

        Raises:
            ValueError: If any required configuration is missing.
        """
        configurable = config.get("configurable", {}) if config else {}

        values: dict[str, Any] = {}
        missing_fields = []

        for f in fields(cls):
            if not f.init:
                continue
            value = os.environ.get(f.name.upper(), configurable.get(f.name))
            if value is None:
                missing_fields.append(f.name)
            else:
                values[f.name] = value

        if missing_fields:
            raise ValueError(f"Missing required config values: {', '.join(missing_fields)}")

        return cls(**values)
