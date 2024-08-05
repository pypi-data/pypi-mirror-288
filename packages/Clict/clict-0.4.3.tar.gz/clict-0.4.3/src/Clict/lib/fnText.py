#!/usr/bin/env python
from random import randint
import os


def color_str(txt,lrgb):
	mask='\x1b[0;38;2;{COLOR}m{TXT}\x1b[m'
	ANSI = '\x1b[0;38;2;{COLOR}m{TXT}\x1b[m'.format(COLOR=';'.join(CC['drk']),TXT='{TXT}')
	O='\x1b[1;38;2;{COLOR}m{TXT}\x1b[m'.format(COLOR=';'.join(CC['lgt']),TXT=O)
	C='\x1b[1;38;2;{COLOR}m{TXT}\x1b[m'.format(COLOR=';'.join(CC['lgt']),TXT=C)

	ITEMS=[]
	for item in __s.keys():
		KEY=ANSI.format(TXT=item)
		VAL=super().__getitem__(item)
		if isinstance(VAL,str):
			VAL=ANSI.format(TXT=repr(VAL))
		ITEMS += ['{KEY} : {VAL}'.format(KEY=KEY, VAL=VAL)]
	ITEMS=','.join(ITEMS)
	retstr='{O}{TXT}{C}'.format(TXT=ITEMS,O=O,C=C)
	return retstr


def color_set():
	from Clict.lib import fnterm
	term=fnterm.info()
	bgval=term['color']['bg']['sum']
	cs={}
	rnd = lambda i: randint(i, 192)
	rgb = lambda: randint(0, 2)
	cs['mid'] = [rnd(0), rnd(0), rnd(0)]
	cs['drk'] = [(i // 3) * 2 for i in cs['mid']]
	cs['lgt'] = [(i // 3) * 4 for i in cs['mid']]

	a=lambda : sum(cs['mid']) < 255
	b=lambda : sum(cs['mid']) > 96
	cond=a if (int(bgval,base=16)< 0x8888) else b
	while cond():
		change = rgb()
		newval = rnd(cs['mid'][change])
		cs['mid'][change] = newval
		cs['drk'][change] = (newval // 3) * 2
		cs['lgt'][change] = (newval // 3) * 4
	for cc in cs:
		cs[cc] = [i for i in cs[cc]]
	return cs



def tree_str(s):
	import sys
	from textwrap import shorten
	# from src.isPyPackage.ansi_colors import reset,rgb,yellow,red
	def hasDict(s):
		return any([True for key in s if isinstance(s[key], dict)])

	def overview(s):
		dicts = [item for item in s if isinstance(s[item], dict)]
		sd = len(dicts)
		ld = len(s) - sd
		sd = rgb('yellow', sd)
		ld = rgb('red', ld)
		reset=rgb('reset')
		print(f'({sd}Groups+{ld}items){reset}', end='')

	def pTree(s, **k):
		fancystr = ''
		depth = k.get('depth', 0)
		maxd = 100
		limi = 100
		d = s
		keys = len(d.keys())
		plines = []
		for key in s:
			dkey = shorten(
				f"\x1b[32m{d[key]}\x1b[0m" if callable(d[key]) else str(d[key]), 80
			)
			keys -= 1
			TREE = "┗━┳╼' " if keys == 0 else "┣━━┳╼' "
			plines += [f"{TREE}{str(key)} :"]
			if isinstance(d[key], Clict):
				# plines[-1]=plines[-1].replace('━','┳',2,1)
				clines = repr(d[key]).split('\n')
				for l, line in enumerate(clines):
					clines[l] = f"┃ {line}" if keys != 0 else f"  {line}"
				# fancystr+="  ┗━━ " if keys == 0 else "  ┣━━ "
				# fancystr+=f"\x1b[1;34m{str(key)}\t:\x1b[0m\t"
				# fancystr+='\n'.join(["  ┃  " * (depth)+line for  line in repr(s[key])])
				plines += clines
			else:
				plines[-1] = plines[-1].replace('┳', '━') + dkey
		return '\n'.join(plines)

	return pTree(s)


def gencolor():
	c = Clict()
	rnd = lambda i: randint(i, 192)
	rgb = lambda: randint(0, 2)
	c.mid = [rnd(0), rnd(0), rnd(0)]
	c.drk = [(i // 3) * 2 for i in c.mid]
	c.lgt = [(i // 3) * 4 for i in c.mid]

	while sum(c.mid) < 255:
		change = rgb()
		newval = rnd(c.mid[change])
		c.mid[change] = newval
		c.drk[change] = (newval // 3) * 2
		c.lgt[change] = (newval // 3) * 4
	for cc in c:
		c[cc] = [str(i) for i in c[cc]]
	return c
