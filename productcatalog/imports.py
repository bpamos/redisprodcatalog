import redis
import redisearch
import os
import abc, json, pathlib
from abc import abstractmethod
from dataclasses import dataclass, field
import numpy as np
from pathlib import Path
# for type annotations
from typing import Any, Dict, List, Optional, Union, Collection
PathOrStr = Union[Path,str]