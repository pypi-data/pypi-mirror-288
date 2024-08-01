#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import os
import platform
from enum import Enum, auto


#--------------------------------------------------------------------------------
# 플랫폼 타입.
#--------------------------------------------------------------------------------
class PlatformType(Enum):
	UNKNOWN = auto()
	WINDOWS = auto()
	LINUX = auto()
	MACOS = auto()


#--------------------------------------------------------------------------------
# 현재 시스템의 플랫폼 타입 반환.
#--------------------------------------------------------------------------------
def GetPlatformType() -> PlatformType:
	systemName : str = platform.system()
	systemName = systemName.upper()
	if systemName == "WINDOWS":
		return PlatformType.WINDOWS
	elif systemName == "DARWIN":
		return PlatformType.MACOS
	elif systemName == "LINUX":
		return PlatformType.LINUX
	else:
		return PlatformType.UNKNOWN