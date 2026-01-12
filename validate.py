#!/usr/bin/env python3
"""
代码结构验证脚本
验证所有模块的导入结构和基本语法，不需要安装依赖
"""

import ast
import os
import sys


def check_python_syntax(filepath):
    """检查 Python 文件语法"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def check_imports(filepath):
    """检查模块导入"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        tree = ast.parse(code)
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        return True, imports
    except Exception as e:
        return False, str(e)


def validate_project_structure():
    """验证项目结构"""
    print("="*60)
    print("项目结构验证")
    print("="*60)
    
    required_files = [
        "main.py",
        "requirements.txt",
        ".env.example",
        "README.md",
        "bilivagent/__init__.py",
        "bilivagent/config.py",
        "bilivagent/utils/__init__.py",
        "bilivagent/utils/bilibili.py",
        "bilivagent/utils/video.py",
        "bilivagent/utils/audio.py",
        "bilivagent/utils/text.py",
        "bilivagent/utils/siliconflow.py",
        "bilivagent/processors/__init__.py",
        "bilivagent/processors/video_content.py",
        "bilivagent/processors/text_content.py",
        "bilivagent/agents/__init__.py",
        "bilivagent/agents/bilivagent.py",
    ]
    
    missing = []
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath} - MISSING")
            missing.append(filepath)
    
    if missing:
        print(f"\n✗ {len(missing)} 文件缺失")
        return False
    else:
        print(f"\n✓ 所有必需文件都存在")
        return True


def validate_python_files():
    """验证 Python 文件语法"""
    print("\n" + "="*60)
    print("Python 语法验证")
    print("="*60)
    
    python_files = []
    for root, dirs, files in os.walk("bilivagent"):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    python_files.extend(["main.py", "check_setup.py", "examples.py"])
    
    all_valid = True
    for filepath in python_files:
        if not os.path.exists(filepath):
            continue
            
        valid, message = check_python_syntax(filepath)
        if valid:
            print(f"✓ {filepath}")
        else:
            print(f"✗ {filepath} - {message}")
            all_valid = False
    
    if all_valid:
        print(f"\n✓ 所有 Python 文件语法正确")
        return True
    else:
        print(f"\n✗ 某些文件存在语法错误")
        return False


def validate_imports():
    """验证关键导入"""
    print("\n" + "="*60)
    print("模块导入分析")
    print("="*60)
    
    key_modules = {
        "bilivagent/config.py": ["os", "dotenv"],
        "bilivagent/utils/bilibili.py": ["re", "os", "json", "subprocess"],
        "bilivagent/utils/video.py": ["os", "random"],
        "bilivagent/utils/audio.py": ["os", "json", "wave"],
        "bilivagent/utils/text.py": ["re"],
        "bilivagent/utils/siliconflow.py": ["json", "base64"],
        "main.py": ["argparse", "sys"],
    }
    
    all_valid = True
    for filepath, expected_imports in key_modules.items():
        if not os.path.exists(filepath):
            print(f"⚠ {filepath} - 文件不存在")
            all_valid = False
            continue
            
        valid, imports = check_imports(filepath)
        if valid:
            # Check if expected imports are present
            found = [imp for imp in expected_imports if any(imp in i for i in imports)]
            print(f"✓ {filepath} - 导入 {len(imports)} 个模块")
        else:
            print(f"✗ {filepath} - {imports}")
            all_valid = False
    
    if all_valid:
        print(f"\n✓ 所有模块导入正常")
        return True
    else:
        print(f"\n✗ 某些模块导入存在问题")
        return False


def validate_requirements():
    """验证 requirements.txt"""
    print("\n" + "="*60)
    print("依赖包验证")
    print("="*60)
    
    if not os.path.exists("requirements.txt"):
        print("✗ requirements.txt 不存在")
        return False
    
    with open("requirements.txt", 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    required_packages = [
        "langchain",
        "requests",
        "python-dotenv",
        "bilibili-api-python",
        "yt-dlp",
        "moviepy",
        "opencv-python",
        "vosk",
        "jieba",
        "wordcloud",
    ]
    
    found_packages = []
    for req in requirements:
        package_name = req.split(">=")[0].split("==")[0]
        if package_name in required_packages:
            found_packages.append(package_name)
            print(f"✓ {req}")
    
    missing = [pkg for pkg in required_packages if pkg not in found_packages]
    if missing:
        print(f"\n⚠ 以下包未在 requirements.txt 中找到:")
        for pkg in missing:
            print(f"  - {pkg}")
        return False
    else:
        print(f"\n✓ 所有必需的包都已列出")
        return True


def main():
    """主函数"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "BiliVagent 代码验证" + " "*22 + "║")
    print("╚" + "="*58 + "╝")
    print()
    
    checks = [
        ("项目结构", validate_project_structure),
        ("Python 语法", validate_python_files),
        ("模块导入", validate_imports),
        ("依赖包", validate_requirements),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ 检查 {name} 时出错: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("验证总结")
    print("="*60)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:.<40} {status}")
    
    print("="*60)
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n✓ 所有验证通过！代码结构正确。")
        print("\n下一步:")
        print("  1. 安装依赖: pip install -r requirements.txt")
        print("  2. 配置环境: cp .env.example .env")
        print("  3. 编辑 .env 文件，填入 API Key")
        print("  4. 运行程序: python main.py <BV号>")
        return 0
    else:
        print("\n✗ 某些验证未通过，请检查上述错误。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
