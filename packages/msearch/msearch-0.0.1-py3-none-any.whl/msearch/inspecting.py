import inspect as inspectlib
import logging
import sys
import traceback
from importlib import import_module
from pkgutil import iter_modules
from typing import Any, Dict, Literal

import click
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax


def load_all_modules(mod) -> list[tuple[str, Any]]:
    out = []
    try:
        for module in iter_modules(mod.__path__ if hasattr(mod, "__path__") else []):
            try:
                # Corrected line: Use mod.__name__ for the package name and module.name for the module name
                full_module_name = f"{mod.__name__}.{module.name}"
                imported_module = import_module(full_module_name)

                out.append((module.name, imported_module))
            except Exception as e:
                print(f"Error loading module {module.name}: {e}")
    except Exception as e:
        traceback.print_exc()
        print(f"Error loading modules from {mod.__name__} {e}")

    return out

def is_standard_lib(module):
    if not inspectlib.ismodule(module):
        return False
    try:
        if hasattr(module, "__name__") and  module.__name__ in sys.builtin_module_names:
            return True  # Module is a built-in module
    except Exception as e:
        traceback.print_exc()  
        print(f"Error checking if module {module.__name__} is a standard library module: {e}")
        return False

def get_root_module(module):
    if hasattr(module, "__module__"):
        return get_root_module(module.__module__)
    elif hasattr(module, "__name__"):
        return module.__name__.split(".")[0]
    elif hasattr(module, "name"):
        return module.name.split(".")[0]
    elif hasattr(module, "__package__"):
        return module.__package__
    return None
def is_imported(module, obj):
    # print(f"Checking if {obj} is imported from {module}")
    # print(f"obj: {inspectlib.getmodule(obj)}")
    # print(f"Module: {inspectlib.getmodule(module)}")
    try:
        logging.debug(f"root module of obj {obj}: {get_root_module(inspectlib.getmodule(obj))}")
        logging.debug(f"root module of module {module}: {get_root_module(inspectlib.getmodule(module))}")
        if get_root_module(inspectlib.getmodule(obj)) == get_root_module(inspectlib.getmodule(module)):
            return False

        return True
    except Exception as e:
        traceback.print_exc()
        print(f"Error checking if {obj} is imported from {module}: {e}")
        if inspectlib.getmodule(obj) is None:
            print(f"{obj} has no module")
            return False
        return True


def get_full_name(obj):
    """
    Returns the full package, module, and class name (if applicable) for classes, functions, modules, and class member functions.
    """
    if inspectlib.isclass(obj) or inspectlib.isfunction(obj):
        return f"{obj.__module__}.{obj.__name__}"
    elif inspectlib.ismethod(obj):
        # For class member functions, include the class name in the path
        class_name = obj.__self__.__class__.__name__
        return f"{obj.__module__}.{class_name}.{obj.__name__}"
    elif inspectlib.ismodule(obj):
        return obj.__name__
    else:
        return "Unknown type"

def collect_info(obj: Any, depth: int = 1, current_depth: int = 0, signatures: bool = True, docs: bool = False, code: bool = False) -> Dict[str, Any]:
    if current_depth > depth:
        return {}
    
    members_dict = {}
    members = inspectlib.getmembers(obj)
    
    if current_depth == 0:
        members += load_all_modules(obj)
    for member, member_obj in members:
        if member.startswith("__") and member.endswith("__"):
            continue
        
        if is_standard_lib(member):
            continue
        if is_imported(obj, member_obj):
            continue

        
        # member_obj = getattr(obj, member)
        member_info = {}
        
        if inspectlib.isclass(member_obj) or inspectlib.ismodule(member_obj):
            member_info["type"] = "class" if inspectlib.isclass(member_obj) else "module"
            if docs:
                docstring = inspectlib.getdoc(member_obj)
                if docstring:
                    member_info["docstring"] = docstring
            member_info["path"] = get_full_name(member_obj)
            member_info["members"] = collect_info(member_obj, depth, current_depth + 1, signatures, docs, code)
        else:
            member_info["path"] = get_full_name(member_obj)
            member_info["type"] = "function" if inspectlib.isfunction(member_obj) else "attribute"
            if signatures and inspectlib.isfunction(member_obj):
                member_info["signature"] = str(inspectlib.signature(member_obj))
            if docs:
                docstring = inspectlib.getdoc(member_obj)
                if docstring:
                    member_info["docstring"] = docstring
            if code and inspectlib.isfunction(member_obj):
                try:
                    source_code = inspectlib.getsource(member_obj)
                    member_info["code"] = source_code
                except OSError:
                    member_info["code"] = "Source code not available"
        
        members_dict[member] = member_info
    
    return members_dict

def render_dict(members_dict: Dict[str, Any], indent: int = 0) -> None:
    console = Console()
    for name, info in members_dict.items():
      
        console.print(" " * indent + f"[bold green]{name}[/bold green]:")
        name = info.get("path", name)
        console.print(f"{' ' * indent}[bold cyan]{name}[/bold cyan]:")
        if "type" in info:
            console.print(f"{' ' * (indent + 2)}[bold]Type:[/bold] {info['type']}")
        if "signature" in info:
            console.print(f"{' ' * (indent + 2)}[bold]Signature:[/bold] {info['signature']}")
        if "docstring" in info:
            console.print(Markdown(info["docstring"]))
        if "code" in info:
            console.print(Syntax(info["code"], "python", word_wrap=True, background_color="white"))
        if "members" in info:
            render_dict(info["members"], indent + 2)
        console.print()

def get_info(module, depth: int = 1, signatures: bool = True, docs: bool = False, code: bool = False):
    console = Console()
    console.print(f"[bold cyan]{module.__name__}[/bold cyan]:")
    if docs:
        docstring = inspectlib.getdoc(module)
        if docstring:
            console.print(Markdown(docstring))
    collected_info = collect_info(module, depth, signatures=signatures, docs=docs, code=code)
    render_dict(collected_info)

def inspect_library(module_or_class, depth, detail: Literal["all", "sigs", "docs", "code", "sd", "imp"] | None = None, markdown=False):
    parts = module_or_class.split(".")
    module_name = ".".join(parts[:-1]) if len(parts) > 1 else module_or_class
    class_name = parts[-1] if len(parts) > 1 else None

    try:
        module = import_module(module_name)
        obj = module
        if class_name:
            obj = getattr(module, class_name)
    except ImportError as e:
        print(f"Error importing module {module_name}: {e}")
        return
    except AttributeError as e:
        module = import_module(module_name)
        for member in load_all_modules(module):
            if class_name == member[0]:
                obj = member[1]
                break

        else:
            print(f"Error accessing attribute {class_name} in {module_name}: {e}")
            return
    signatures = any("sigs" in detail, "all" in detail)
    docs = any("docs" in detail, "all" in detail, "sd" in detail)
    code = any("code" in detail, "all" in detail)
    get_info(obj, depth, signatures, docs, code)

def inspect_repo(repo_path, depth, detail: Literal["all", "sigs", "docs", "code", "sd", "imp"] | None = None, markdown=False):
    
    try:
        sys.path.append(repo_path)
        module = import_module(repo_path)
    except ImportError as e:
        print(f"Error importing module {repo_path}: {e}")
        return
    except AttributeError as e:
        print(f"Error accessing attribute {repo_path}: {e}")
        return
    signatures = any("sigs" in detail, "all" in detail)
    docs = any("docs" in detail, "all" in detail, "sd" in detail)
    code = any("code" in detail, "all" in detail)
    get_info(module, depth, signatures, docs, code)

    # get the python executable path
    executable = sys.executable
# Example usage
@click.command("inspect")
@click.argument("module_or_class", type=click.STRING)
@click.option("--depth" , "-d", type=click.INT, default=0)
@click.option("--sigs", "-s", default=False)
@click.option("--docs", "-doc", default=False)
@click.option("--code", "-c", default=False)
@click.option("--imports", "-imp", default=False)
@click.option("--mode", "-m", type=click.Choice(["all", "sigs", "docs", "code", "sd", "imp"]), default=None)
@click.option("--markdown", "-md", default=False)
def inspect_cli(module_or_class, depth, signatures, docs, code, imports, mode=None, markdown=False):
    """Inspect a Python module or class. Optionally specify the depth of inspection and the level of detail.

    Args:
        module_or_class (str): The name of the module or class to inspect.
        depth (int): The depth of inspection.
        signatures (bool): Include function signatures in the inspection.
        docs (bool): Include docstrings in the inspection.
        code (bool): Include source code in the inspection.
        imports (bool): Include imported modules in the inspection.
        mode (str): The level of detail to include in the inspection.
        markdown (bool): Return the inspection results as Markdown.
    """
    if mode:
        signatures = any("sigs" in mode, "all" in mode, "sd" in mode)
        docs = any("docs" in mode, "all" in mode, "sd" in mode)
        code = "code" in mode
        imports = "imp" in mode
    else:
        if code and signatures and imports and docs:
            mode = "all"
        elif code and signatures and docs:
            mode = "sd"
        elif signatures:
            mode = "sigs"
        elif docs:
            mode = "docs"
        elif imports:
            mode = "imp"

            
    inspect_library(module_or_class, depth, detail=mode, markdown=markdown)

if __name__ == "__main__":
    inspect_cli()


