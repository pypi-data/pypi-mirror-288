# -*- coding: UTF-8 -*-
"""
项目目标：基于pypi网站，类比pip，实现vb的包管理功能
基本指令：
    vb install package_name     同pip install
    vb uninstall package_name   同pip uninstall
    vb load package_name        将包复制到项目所在目录下的lib/package_name，并引入工程
    vb unload package_name      将项目目录下的lib/package_name移除，同时从VB工程中移除
"""
import argparse
import os
import shutil
import site
import subprocess
from pathlib import Path


def copy_directory_recursive(source_dir, destination_dir):
    """遍历复制文件夹"""
    # 如果目标目录不存在，则创建
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for root, dirs, files in os.walk(source_dir):
        # 处理目录
        for dir_ in dirs:
            source_path = os.path.join(root, dir_)
            destination_path = os.path.join(destination_dir, os.path.relpath(source_path, source_dir))
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)

        # 处理文件
        for file in files:
            source_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_dir, os.path.relpath(source_file_path, source_dir))
            shutil.copy2(source_file_path, destination_file_path)


def get_global_site_packages():
    """获取全局站点包路径"""
    return site.getsitepackages()[0]


def pip_install_handler(args):
    """调用pip下载包"""
    target = args.target
    index = f' -i {args.index}' if args.index else ''
    command = f'pip install {target} {index}'
    subprocess.run(command, shell=True)


def pip_uninstall_handler(args):
    """调用pip卸载包"""
    target = args.target
    command = f'pip uninstall {target}'
    subprocess.run(command, shell=True)


def vb_project_load(args):
    """将pypi文件复制到项目所在文件，并引入.vbp工程
    Module=Utils; csv-merger.bas
    Module=Utils2; Utils2.bas
    Form=FrmMain.frm
    Form=Form1.frm
    Class=Class1; Class1.cls
    Class=Class2; Class2.cls
    """
    import_object = ('.bas', 'frm', '.cls')
    target = args.target  # 包名
    # 复制站点包到当前项目下的libs文件夹
    path_libs = os.path.join(os.getcwd(), 'libs', target)
    if not os.path.exists(path_libs):
        os.makedirs(path_libs, exist_ok=True)
    path_target_package = Path(get_global_site_packages()).joinpath(fr'Lib\site-packages\{target}')
    copy_directory_recursive(path_target_package, path_libs)
    # 查找.vbp工程文件
    vbp_name = ''
    for fn in os.listdir(os.getcwd()):
        if fn.endswith('.vbp'):
            vbp_name = fn
    # 如果没有vbp文件，就不做引用
    if not vbp_name:
        return
    # 否则读取.vbp文件数据
    with open(vbp_name, 'r', encoding='ANSI') as f:
        vbp_lines_trim = [line.strip().replace(' ', '') for line in f.readlines()]
    vbp_newlines = []
    # 遍历引用frm、cls、bas
    for root, dns, fns in os.walk(path_libs):
        for fn in fns:
            fp = os.path.join(root, fn)
            if not fn.endswith(import_object):
                continue
            relpath = os.path.relpath(fp, os.getcwd())
            if fn.endswith('.bas'):
                with open(fp, 'r', encoding='ANSI') as f:
                    bas_line = f.readline().strip()
                    while not bas_line.startswith('Attribute VB_Name'):
                        bas_line = f.readline().strip()
                    module = bas_line.split('=')[-1].replace('"', '').strip()
                vbp_newline = f'Module={module}; {relpath}'
                if not vbp_newline.replace(' ', '') in vbp_lines_trim:
                    vbp_newlines.append(vbp_newline)
            elif fn.endswith('.frm'):
                vbp_newline = f'Form={relpath}'
                vbp_newlines.append(vbp_newline)
            elif fn.endswith('.cls'):
                with open(fp, 'r', encoding='ANSI') as f:
                    cls_line = f.readline().strip()
                    while not cls_line.startswith('Attribute VB_Name'):
                        cls_line = f.readline().strip()
                    cls = cls_line.split('=')[-1].replace('"', '').strip()
                vbp_newline = f'Class={cls}; {relpath}'
                if not vbp_newline.replace(' ', '') in vbp_lines_trim:
                    vbp_newlines.append(vbp_newline)
            else:
                pass
    with open(vbp_name, 'a', encoding='ANSI') as f:
        for vbp_newline in vbp_newlines:
            if vbp_newline.strip().replace(' ', '') in vbp_lines_trim:
                continue
            f.write(f'{vbp_newline}\n')


def vb_project_unload(args):
    """将模块从.vbp工程移除"""
    target = args.target  # 包名
    # 要移除的模块
    path_libs_package = Path(os.getcwd()).joinpath(fr'libs\{target}')
    # 查找.vbp工程文件
    vbp_name = ''
    for fn in os.listdir(os.getcwd()):
        if fn.endswith('.vbp'):
            vbp_name = fn
    # 如果没有vbp文件，就不做引用
    if not vbp_name:
        return
    # 否则读取.vbp文件数据，查找需要删除的模块
    with open(vbp_name, 'r', encoding='ANSI') as f:
        vbp_lines = [line.strip() for line in f.readlines()]
    vbp_newlines = []
    for vbp_line in vbp_lines:
        relpath = os.path.relpath(path_libs_package, os.getcwd())
        if relpath not in vbp_line:
            vbp_newlines.append(vbp_line)
    if not vbp_newlines:
        return
    # 开始删除模块
    with open(vbp_name, 'w', encoding='ANSI') as f:
        for vbp_newline in vbp_newlines:
            f.write(f'{vbp_newline}\n')
    shutil.rmtree(os.path.join(os.getcwd(), 'libs', target))


def main():
    # 创建解析器
    parser = argparse.ArgumentParser(description="这是一个详细的命令行参数解析示例")

    # 定义install及其参数
    parser.add_argument("action", type=str, help="支持vb install/unintsall/load/unload package_name")
    parser.add_argument("target", nargs='?', type=str, help="要操作的pypi模块")
    parser.add_argument("-i", '--index', type=str, help="镜像地址")

    # 解析命令行参数
    args = parser.parse_args()

    if args.action == 'install' and args.target != '':
        pip_install_handler(args)
    elif args.action == 'uninstall' and args.target != '':
        pip_uninstall_handler(args)
    elif args.action == 'load':
        vb_project_load(args)
    elif args.action == 'unload':
        vb_project_unload(args)
    else:
        pass


if __name__ == '__main__':
    main()
