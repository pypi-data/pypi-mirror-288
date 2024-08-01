#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Any, Final, Optional, Type, TypeVar, Union, Tuple, Generic, List, Dict, Set, cast
import builtins


#--------------------------------------------------------------------------------
# 공유 클래스의 메타클래스 (클래스 타입 클래스).
#--------------------------------------------------------------------------------
class MetaClass(type):
	#--------------------------------------------------------------------------------
	# 클래스 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__instances : Dict[Type[MetaClass], SharedClass] = dict()


	#--------------------------------------------------------------------------------
	# 인스턴스 할당 요청 됨(생성자 호출됨).
	#--------------------------------------------------------------------------------
	def __call__(classType, *args: Any, **kwds: Any) -> Any:
		if classType in classType.__instances:
			instance = classType.__instances[classType]
			return instance
		else:
			instance = super().__call__(*args, **kwds)
			classType.__instances[classType] = instance

			
#--------------------------------------------------------------------------------
# 공유 클래스 (싱글톤 클래스).
# - class ChildClass(SharedClass): pass
# - value1 = ChildClass()
# - value2 = ChildClass()
# - value1 == value2
#--------------------------------------------------------------------------------
class SharedClass(metaclass = MetaClass):
	pass