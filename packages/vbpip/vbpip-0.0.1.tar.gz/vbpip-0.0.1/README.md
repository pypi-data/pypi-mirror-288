# 项目目标
基于pypi网站，类比pip，实现简单的vb包管理。

# 基本指令
```shell
>> vb install package_name     调用pip安装package_name包
>> vb uninstall package_name   调用pip卸载package_name包
>> vb load package_name        将包复制到vb项目所在目录下的lib/package_name,并将包中的.bas/.frm/.cls引入到.vbp工程文件
>> vb unload package_name      将vb项目目录下的lib/package_name移除,同时从VB工程中移除引用
```