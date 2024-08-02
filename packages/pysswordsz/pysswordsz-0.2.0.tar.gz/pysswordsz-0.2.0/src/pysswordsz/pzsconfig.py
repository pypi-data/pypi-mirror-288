from pathlib import Path
from collections.abc import Callable
import typer
import yaml
import platform
import os

def belongto(oripart:Callable, target:Callable) -> bool:
    for i in oripart :
        if i in target :
            return True
    return False

def setting_config():
    # 处理配置位置
    overpath = os.getenv("PYSSWORDSZ")
    if overpath is None :
        if platform.system() == "Windows" :
            overpath = "AppData/Local/pysswordsz"
        else :
            overpath = ".config/pysswordsz"
        conPath = Path.home() / overpath
    else :
        conPath = overpath
    return conPath

def newConfig() -> None:
    data = {
        "columns": ["url","user","comment"],
        "keyfolder":setting_config(),
        "datafolder":setting_config()
    }
    changefolder = typer.confirm("是否更改密钥KEY文件的保存位置?\nDo you want to change the KEY file location?\n--> ")
    if changefolder :
        data["keyfolder"] = typer.prompt("请输入密钥KEY文件的保存位置\nPlease input the KEY file location\n--> ")
    changefolder = typer.confirm("是否更改数据DATA文件的保存位置?\nDo you want to change the DATA file location?\n--> ")
    if changefolder :
        data["datafolder"] = typer.prompt("请输入数据DATA文件的保存位置\nPlease input the DATA file location\n--> ")
    os.mkdir(setting_config())
    with open(setting_config() / "config.yaml", "w", encoding="utf-8") as fx :
        yaml.dump(data, fx)

class pszconfig(object):
    def __init__(self) -> None:
        self.__home = setting_config() / "config.yaml"
        with open(self.__home, "r", encoding="utf-8") as ftxt:
            self.__data = yaml.load(ftxt.read(),Loader=yaml.FullLoader)
    def __saveconfig(self) -> None :
        with open(self.__home, "w", encoding="utf-8") as fx :
            yaml.dump(self.__data, fx)
    def keyfolder(self) -> Path:
        fp = self.__data["keyfolder"]
        return Path(fp)
    def datafolder(self) -> Path:
        fp = self.__data["datafolder"]
        return Path(fp)
    @property
    def columns(self) -> list:
        return self.__data["columns"]
    @property
    def vaultlist(self) -> list:
        if "vaultlist" in self.__data.keys():
            return self.__data["vaultlist"]
        else :
            return []
    @property
    def vault(self) -> str:
        if "vault" in self.__data.keys():
            return self.__data["vault"]
        else :
            raise ValueError("No vault is set!")
    def list(self) -> None:
        print(self.__data)
    def setting(self, name:str, value:str) -> None:
        if name == "columns":
            if "," in value :
                newcols = value.spilt(",")
            else:
                newcols = list(set(self.columns.append(value)))
            if belongto(newcols,["uuid","name","password","createtime"]) :
                raise KeyError('"uuid" "name" "password" and "createtime" are reserved names.')
            else:
                self.__data[name] = newcols
        else:
            self.__data[name] = value
        self.__saveconfig()
        print("Complete the configuration settings!")
    def remove(self, name:str) :
        if name not in self.__data.keys():
            raise KeyError("The configuration does not exist!")
        if name in ["columns","keyfolder","datafolder"]:
            if name == "columns":
                self.__data[name] = ["url","user","comment"]
            else :
                self.__data[name] = setting_config()
        else :
            self.__data.pop(name)
        self.__saveconfig()
        print("Complete removing config {} !".format(name))