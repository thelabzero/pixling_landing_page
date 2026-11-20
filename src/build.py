"""Build everything into public/:  python3 src/build.py"""
import runpy, os
H = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(H, 'page', 'build.py'))
runpy.run_path(os.path.join(H, 'site', 'build.py'))
