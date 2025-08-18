#!/usr/bin/env python3
"""
Script to fix all import paths in the agent-python project
"""
import os
import re

def fix_imports_in_file(file_path):
    """Fix imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace relative imports with absolute imports
        patterns = [
            (r'from graph_arc\.', r'from src.graph_arc.'),
            (r'from config\.', r'from src.config.'),
            (r'from utils\.', r'from src.utils.'),
            (r'from core\.', r'from src.core.'),
            (r'from data\.', r'from src.data.'),
            (r'from tools\.', r'from src.tools.'),
            (r'from loaders\.', r'from src.loaders.'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed imports in: {file_path}")
            return True
        else:
            print(f"⏭️  No changes needed: {file_path}")
            return False
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def fix_all_imports():
    """Fix imports in all Python files"""
    src_dir = "C:\\Abhi\\Capital_one_hacathon\\agent-python\\src"
    fixed_count = 0
    
    print("🔧 Fixing imports in all Python files...")
    print("=" * 50)
    
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if fix_imports_in_file(file_path):
                    fixed_count += 1
    
    print("=" * 50)
    print(f"🎉 Fixed imports in {fixed_count} files")

if __name__ == "__main__":
    fix_all_imports()
