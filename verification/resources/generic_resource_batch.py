"""Public CLI alias; fixed source-specific native programs own their full DAGs."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generic_resource_worker import main

if __name__ == '__main__':
    main()
