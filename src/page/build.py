"""Assemble index.html from src.html + inlined fonts + Dino wedge engine.  Run: python3 src/page/build.py"""
import os
H=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(H,'..','..'))
s=open(os.path.join(H,'src.html')).read()
s=s.replace('/*FONTS*/',open(os.path.join(H,'fonts.css')).read()).replace('/*WEDGE*/',open(os.path.join(H,'wedge.js')).read())
open(os.path.join(ROOT,'public','index.html'),'w').write(s); print('wrote public/index.html',len(s))
