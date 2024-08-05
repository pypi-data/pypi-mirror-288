import importlib
import sys

def check_dependencies():
    dependencies = {
        "numpy": "1.18.0",
        "torch": "1.7.0",
        "tqdm": "4.45.0",
        "regex": "2020.4.4"
    }
    
    missing = []
    for module, min_version in dependencies.items():
        try:
            imp = importlib.import_module(module)
            version = imp.__version__
            if version < min_version:
                missing.append(f"{module}>={min_version}")
        except ImportError:
            missing.append(f"{module}>={min_version}")
    
    if missing:
        print(f"Error: Missing required dependencies: {', '.join(missing)}")
        print("Please install the missing dependencies and try again.")
        sys.exit(1)
    

