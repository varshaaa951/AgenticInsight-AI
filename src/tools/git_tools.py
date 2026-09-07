import os
import ast
import tempfile
from typing import Dict, Any, List
from git import Repo

def clone_and_analyze_repo(repo_url: str) -> Dict[str, Any]:
    """
    Clones a public GitHub repo into a temporary directory and 
    statically analyzes Python files using AST (Abstract Syntax Tree).
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f" Cloning {repo_url} into temporary directory...")
        Repo.clone_from(repo_url, temp_dir, depth=1)
        
        total_files = 0
        total_lines = 0
        functions_found: List[str] = []
        classes_found: List[str] = []
        
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(".py"):
                    total_files += 1
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            total_lines += len(content.splitlines())
                            
                            # Parse code into AST without executing it
                            tree = ast.parse(content)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.FunctionDef):
                                    functions_found.append(node.name)
                                elif isinstance(node, ast.ClassDef):
                                    classes_found.append(node.name)
                    except Exception:
                        # Skip files that fail encoding or parsing
                        continue

        return {
            "total_python_files": total_files,
            "total_lines_of_code": total_lines,
            "total_functions": len(functions_found),
            "total_classes": len(classes_found),
            "sample_functions": functions_found[:5],
            "sample_classes": classes_found[:5]
        }