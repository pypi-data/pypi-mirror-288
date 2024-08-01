#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union, List, Dict, cast
import builtins
import os
import psutil
from .processinfo import ProcessInfo


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------


#--------------------------------------------------------------------------------
# 프로세스 매니저.
#--------------------------------------------------------------------------------
class ProcessManager():
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------

	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 파괴됨.
	#--------------------------------------------------------------------------------
	def __del__(self) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 프로세스 즉시 파괴.
	#--------------------------------------------------------------------------------
	def DestroyProcessImmediateByID(self, processID : int) -> bool:
		try:
			process = psutil.Process(processID)
			process.kill() # 프로세스 강제 종료.
			return True
		except psutil.NoSuchProcess as exception: # 프로세스 못찾음.
			return False
		except psutil.AccessDenied as exception: # 접근 권한 없음.
			return False
		except psutil.ZombieProcess as exception: # 좀비 프로세스.
			return False


	#--------------------------------------------------------------------------------
	# 프로세스 파괴.
	#--------------------------------------------------------------------------------
	def DestroyProcessByID(self, processID : int, timeout : float = 5.0) -> bool:
		try:
			process = psutil.Process(processID)
			if timeout > 0.0:
				process.terminate() # 프로세스 종료 요청.
				try:
					process.wait(timeout) # 종료 대기.
					return True
				except Exception.TimeoutExpired:
					return self.DestroyProcessImmediateByID(processID) # 프로세스 강제 종료.
			else:
				return self.DestroyProcessImmediateByID(processID) # 프로세스 강제 종료.
		except psutil.NoSuchProcess as exception: # 프로세스 못찾음.
			return False
		except psutil.AccessDenied as exception: # 접근 권한 없음.
			return False
		except psutil.ZombieProcess as exception: # 좀비 프로세스.
			return False


	#--------------------------------------------------------------------------------
	# 프로세스 아이디 검색.
	#--------------------------------------------------------------------------------
	def FindProcessInfosByID(self, targetProcessID : int) -> ProcessInfo:
		for process in psutil.process_iter(["pid", "name", "exe"]):
			try:
				processID = process.info["pid"]
				processName = process.info["name"]
				processFilePath = process.info["exe"]
				if processID == targetProcessID:
					processInfo = ProcessInfo()
					processInfo.ID = processID
					processInfo.Name = processName
					processInfo.FilePath = processFilePath
					return processInfo
				
			except psutil.NoSuchProcess as exception: # 프로세스 못찾음.
				pass
			except psutil.AccessDenied as exception: # 접근 권한 없음.
				pass
			except psutil.ZombieProcess as exception: # 좀비 프로세스.
				pass

		return None


	#--------------------------------------------------------------------------------
	# 프로세스 이름 검색.
	#--------------------------------------------------------------------------------
	def FindProcessInfosByName(self, targetProcessName : str) -> dict[int, ProcessInfo]:
		processInfos : dict[int, ProcessInfo] = dict()
		for process in psutil.process_iter(["pid", "name", "exe"]):
			try:
				processID = process.info["pid"]
				processName = process.info["name"]
				processFilePath = process.info["exe"]
				if processName == targetProcessName:
					processInfo = ProcessInfo()
					processInfo.ID = processID
					processInfo.Name = processName
					processInfo.FilePath = processFilePath
					processInfos[processID] = processInfo
				
			except psutil.NoSuchProcess as exception: # 프로세스 못찾음.
				pass
			except psutil.AccessDenied as exception: # 접근 권한 없음.
				pass
			except psutil.ZombieProcess as exception: # 좀비 프로세스.
				pass

		return processInfos