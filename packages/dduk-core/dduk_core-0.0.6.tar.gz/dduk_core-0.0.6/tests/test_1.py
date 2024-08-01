#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union, Tuple, List, Dict, Set, cast
import builtins
import os
# from src import dduk
# from dduk import utils # dduk 못알아먹음.
# from ..src.dduk.utils import strutil # 상대 접근 실패.
from src.dduk.utils import strutil # 성공.
# import src.dduk.utils.strutil # 성공.
import unittest


#--------------------------------------------------------------------------------
# 유닛테스트.
#--------------------------------------------------------------------------------
class Test_1(unittest.TestCase):
	#--------------------------------------------------------------------------------
	# 유닛테스트.
	#--------------------------------------------------------------------------------
	def test_Main(self):
		# timestamp = src.dduk.utils.strutil.GetTimestampString()
		timestamp = strutil.GetTimestampString()
		builtins.print("tests.test_1.Test_1.test_Main()")
		builtins.print(timestamp)