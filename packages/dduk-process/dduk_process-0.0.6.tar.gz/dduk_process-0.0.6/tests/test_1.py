#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union, List, Dict, cast
import builtins
import os
from src.dduk.process.processmanager import ProcessManager # 성공.
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
		
		processManager = ProcessManager()
		processManager.FindProcess()

		builtins.print("tests.test_1.Test_1.test_Main()")
		builtins.print(timestamp)