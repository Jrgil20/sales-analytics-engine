#!/usr/bin/env python3
"""Script de compatibilidad hacia atrás.

Redirige la ejecución hacia 'main.py' para preservar compatibilidad con scripts históricos.
"""

from main import main

if __name__ == "__main__":
    main()
