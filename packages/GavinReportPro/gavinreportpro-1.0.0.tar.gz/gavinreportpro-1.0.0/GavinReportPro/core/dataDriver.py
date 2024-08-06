"""
============================
Modifier:TheRuffian
Time:2023-02-16 17:09:14
E-mail:theruffian@163.com
1.数据驱动读取失败问题修改，数据读取增加一层列表包裹
============================
Original Author:柠檬班-木森
Time:2020/11/25  14:14
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
from functools import wraps
import json
import yaml


def _create_test_name(index, name):
    if index + 1 < 10:
        test_name = name + "_00" + str(index + 1)
    elif index + 1 < 100:
        test_name = name + "_0" + str(index + 1)
    else:
        test_name = name + "_" + str(index + 1)
    return test_name


def _update_func(new_func_name, params, test_desc, func, *args, **kwargs):
    @wraps(func)
    def wrapper(self):
        return func(self, params, *args, **kwargs)

    wrapper.__wrapped__ = func
    wrapper.__name__ = new_func_name
    wrapper.__doc__ = test_desc
    return wrapper


def ddt(cls):
    """
    :param cls: 测试类
    :return:
    """
    for name, func in list(cls.__dict__.items()):
        if hasattr(func, "PARAMS"):
            for index, case_data in enumerate(getattr(func, "PARAMS")):
                new_test_name = _create_test_name(index, name)
                if isinstance(case_data, dict) and case_data.get("title"):
                    test_desc = str(case_data.get("title"))
                elif isinstance(case_data, dict) and case_data.get("desc"):
                    test_desc = str(case_data.get("desc"))
                elif (not isinstance(case_data, str)) and hasattr(case_data, 'title'):
                    test_desc = str(case_data.title)
                else:
                    test_desc = func.__doc__
                func2 = _update_func(new_test_name, case_data, test_desc, func)
                setattr(cls, new_test_name, func2)
            else:
                delattr(cls, name)
    return cls


def list_and_dict_data(datas):
    """
    :param datas: 测试数据 [[]...] or [{}...]
    :return:
    """
    result = []

    def wrapper(func):
        if isinstance(datas, dict):
            result.append(datas)
            setattr(func, "PARAMS", result)
        else:
            setattr(func, "PARAMS", datas)
        return func

    return wrapper


def yaml_data(file_path):
    """
    file_path: yaml文件路径
    return: yaml datas
    """
    result = []

    def wrapper(func):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                datas = yaml.load(f, Loader=yaml.FullLoader)
                result.append(datas)
                print(result)
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="gbk") as f:
                datas = yaml.load(f, Loader=yaml.FullLoader)
                result.append(datas)
        setattr(func, "PARAMS", result)
        return func

    return wrapper


def json_data(file_path):
    """
    file_path: json path
    :return: json datas
    """

    def wrapper(func):
        result = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                datas = json.load(f)
                result.append(datas)
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="gbk") as f:
                datas = json.load(f)
                result.append(datas)
        setattr(func, "PARAMS", result)
        return func

    return wrapper
