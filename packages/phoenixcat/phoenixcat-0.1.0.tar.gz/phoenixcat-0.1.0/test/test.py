import sys
import pkginfo

# import numpy
import numpy.random

from phoenixcat.configuration import ExecuteOrderMixin, PostInitMixin

# from phoenixcat.trainer.
import dataclasses
from dataclasses import dataclass
from diffusers.configuration_utils import ConfigMixin


class A(PostInitMixin):

    def __init__(self):
        super().__init__()
        print("A.__init__")

    def __post_init__(self):
        print("A.__post_init__")


class B(A):

    def __init__(self):
        print("B.__init__")
        super().__init__()

    def __post_init__(self):
        print("B.__post_init__")
        super().__post_init__()


class C(A):

    def __init__(self):
        print("C.__init__")
        super().__init__()

    def __post_init__(self):
        print("C.__post_init__")
        super().__post_init__()


class D(B, C):

    def __init__(self):
        print("D.__init__")
        self.aa = 11
        super().__init__()

    # def __post_init__(self):
    #     print("D.__post_init__")
    #     super().__post_init__()


model = D()
# exit()


class INC:

    def __init__(self):
        self.b = 2


class MyClass(Pipeline):

    def __init__(self):
        super().__init__()
        self.a = INC()

    def __post_init__(self):
        return super().__post_init__()

    @property
    def is_end(self):
        return False

    @ExecuteOrderMixin.register_execute_main('epoch')
    def main(self, aa):
        # print('-------------')
        print('main')
        print(aa)

    @ExecuteOrderMixin.register_execute_order(
        'epoch', order=1, interval=1, execute_time='before'
    )
    def f1(self):
        print('f1')

    @ExecuteOrderMixin.register_execute_order(
        'epoch', order=3, interval='a.b', execute_time='before'
    )
    def f2(self):
        print('f2')

    @ExecuteOrderMixin.register_execute_order(
        'epoch', order=2, interval=2, execute_time='before'
    )
    def f3(self):
        print('f3')

    @ExecuteOrderMixin.register_execute_order(
        'epoch', order=1, interval=1, execute_time='after'
    )
    def f4(self):
        print('f4')

    @ExecuteOrderMixin.register_execute_order(
        'epoch', order=3, interval=1, execute_time='after'
    )
    def f5(self):
        print('f5')

    @ExecuteOrderMixin.register_execute_order(
        'epoch', order=2, interval=2, execute_time='after'
    )
    def f6(self):
        print('f6')


m = MyClass()
# print(getattr(m, 'a'))
print('------------------------')
m.main(11)
print('------------------------')
m.main(22)
print('------------------------')
m.main(33)

exit()

# from phoenixcat.trainer.train_pipeline import TrainPipelineMixin

# from accelerate import Accelerator


# class MyClass:


#     def my_method(self):
#         print("This is an instance method.")


# # 创建一个实例
# obj = MyClass()

# # 获取绑定方法
# bound_method = obj.my_method

# # 打印绑定方法所属的实例
# print(bound_method.__self__)  # 输出：<__main__.MyClass object at 0x...>
# exit()

# model = TrainPipelineMixin("bb", None)
# model.cc = 'aa'
# # # print(model.__qualname__)
# # # print(Accelerator().init_trackers('aaa'))
# model.reset_flag()

# exit()

import types


class MyClass:

    aa = []

    def __init__(self) -> types.NoneType:
        # self.b = types.MethodType(self.a, self)
        # print(self.b.__self__)

        self.aa.append(11)

    def a(self, function=None):

        if function is None:
            # print(self.__qualname__)
            function = self

        # print('has __self__', hasattr(function, '__self__'))

        def wrapper(*args, **kwargs):
            # print('inner has __self__', hasattr(function, '__self__'))
            # print("Before function call")
            result = function(*args, **kwargs)
            # print("After function call")
            return result

        return wrapper

    @a
    def b(self):
        print("Inside the method")


class SubClass(MyClass):
    pass


# 创建类的实例
aa = MyClass()
bb = MyClass()

print(aa.aa)
print(bb.aa)
print(MyClass.aa)

print(callable(aa))
print(callable(aa.b))
