#!/usr/bin/env python3
"""
Bulk File Renamer - 批量文件重命名工具

这个命令行工具允许用户批量重命名文件夹中的文件，
支持多种模式：添加前缀、添加后缀、替换文本、正则表达式替换等。
"""

import os
import sys
import re
import argparse
from pathlib import Path


def add_prefix(filename, prefix):
    """给文件名添加前缀"""
    name, ext = os.path.splitext(filename)
    return f"{prefix}{name}{ext}"


def add_suffix(filename, suffix):
    """给文件名（不含扩展名部分）添加后缀"""
    name, ext = os.path.splitext(filename)
    return f"{name}{suffix}{ext}"


def replace_text(filename, old_text, new_text):
    """替换文件名中的文本"""
    name, ext = os.path.splitext(filename)
    new_name = name.replace(old_text, new_text)
    return f"{new_name}{ext}"


def regex_replace(filename, pattern, replacement):
    """使用正则表达式替换文件名"""
    name, ext = os.path.splitext(filename)
    new_name = re.sub(pattern, replacement, name)
    return f"{new_name}{ext}"


def rename_with_pattern(filename, pattern):
    """
    使用格式化模式重命名文件
    支持的格式有:
    {name} - 原始文件名（不含扩展名）
    {ext} - 文件扩展名（包含点）
    {index} - 文件索引号
    {counter:03d} - 计数器（带前导零）
    """
    name, ext = os.path.splitext(filename)
    return pattern.format(name=name, ext=ext)


def bulk_rename(directory, mode, **kwargs):
    """批量重命名文件夹中的文件"""
    if not os.path.isdir(directory):
        print(f"错误: '{directory}' 不是有效的目录")
        return

    # 获取目录中的所有文件（不包括子目录）
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        print(f"目录 '{directory}' 中没有文件")
        return

    # 排序文件列表以确保一致的重命名顺序
    files.sort()
    
    # 预览更改
    changes = []
    counter = 1
    
    for index, filename in enumerate(files, 1):
        if mode == "prefix":
            new_name = add_prefix(filename, kwargs.get("prefix", ""))
        elif mode == "suffix":
            new_name = add_suffix(filename, kwargs.get("suffix", ""))
        elif mode == "replace":
            new_name = replace_text(filename, kwargs.get("old_text", ""), kwargs.get("new_text", ""))
        elif mode == "regex":
            new_name = regex_replace(filename, kwargs.get("pattern", ""), kwargs.get("replacement", ""))
        elif mode == "pattern":
            pattern_str = kwargs.get("pattern", "{name}{ext}")
            new_name = pattern_str.format(
                name=os.path.splitext(filename)[0],
                ext=os.path.splitext(filename)[1],
                index=index,
                counter=counter
            )
            counter += 1
        else:
            print(f"错误: 未知的模式 '{mode}'")
            return

        # 如果新名称与旧名称相同，跳过
        if new_name == filename:
            continue

        changes.append((filename, new_name))

    # 显示预览
    if not changes:
        print("没有文件需要重命名")
        return

    print("\n预览更改:")
    print("-" * 60)
    for old_name, new_name in changes:
        print(f"{old_name} -> {new_name}")
    print("-" * 60)
    
    # 确认是否继续
    if not kwargs.get("force", False):
        response = input("\n确认执行这些更改? (y/n): ").strip().lower()
        if response != 'y':
            print("操作已取消")
            return

    # 执行重命名
    success_count = 0
    error_count = 0
    
    for old_name, new_name in changes:
        try:
            old_path = os.path.join(directory, old_name)
            new_path = os.path.join(directory, new_name)
            
            # 检查目标文件是否已存在
            if os.path.exists(new_path):
                print(f"错误: 无法重命名 '{old_name}' -> '{new_name}' (目标文件已存在)")
                error_count += 1
                continue
                
            os.rename(old_path, new_path)
            success_count += 1
            
        except Exception as e:
            print(f"错误: 重命名 '{old_name}' -> '{new_name}' 失败: {str(e)}")
            error_count += 1

    print(f"\n完成: {success_count} 个文件重命名成功, {error_count} 个失败")


def main():
    parser = argparse.ArgumentParser(description="批量重命名文件工具")
    
    parser.add_argument("directory", help="包含要重命名文件的目录路径")
    
    # 创建子解析器以处理不同的模式
    subparsers = parser.add_subparsers(dest="mode", help="重命名模式")
    
    # 前缀模式
    prefix_parser = subparsers.add_parser("prefix", help="给文件名添加前缀")
    prefix_parser.add_argument("prefix", help="要添加的前缀")
    
    # 后缀模式
    suffix_parser = subparsers.add_parser("suffix", help="给文件名（不含扩展名）添加后缀")
    suffix_parser.add_argument("suffix", help="要添加的后缀")
    
    # 替换模式
    replace_parser = subparsers.add_parser("replace", help="替换文件名中的文本")
    replace_parser.add_argument("old_text", help="要替换的文本")
    replace_parser.add_argument("new_text", help="替换成的新文本")
    
    # 正则表达式模式
    regex_parser = subparsers.add_parser("regex", help="使用正则表达式替换文件名")
    regex_parser.add_argument("pattern", help="正则表达式模式")
    regex_parser.add_argument("replacement", help="替换字符串")
    
    # 模式格式化
    pattern_parser = subparsers.add_parser("pattern", help="使用格式化模式重命名")
    pattern_parser.add_argument("pattern", help="重命名格式，例如: 'file_{counter:03d}{ext}'")
    
    # 通用选项
    for p in [prefix_parser, suffix_parser, replace_parser, regex_parser, pattern_parser]:
        p.add_argument("-f", "--force", action="store_true", help="不询问确认直接执行")
    
    args = parser.parse_args()
    
    # 如果没有指定模式
    if not args.mode:
        parser.print_help()
        sys.exit(1)
    
    # 根据不同模式处理参数
    kwargs = {}
    if args.mode == "prefix":
        kwargs = {"prefix": args.prefix}
    elif args.mode == "suffix":
        kwargs = {"suffix": args.suffix}
    elif args.mode == "replace":
        kwargs = {"old_text": args.old_text, "new_text": args.new_text}
    elif args.mode == "regex":
        kwargs = {"pattern": args.pattern, "replacement": args.replacement}
    elif args.mode == "pattern":
        kwargs = {"pattern": args.pattern}
    
    if hasattr(args, "force"):
        kwargs["force"] = args.force
    
    bulk_rename(args.directory, args.mode, **kwargs)


if __name__ == "__main__":
    main()
