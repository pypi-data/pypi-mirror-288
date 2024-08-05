# Clict
Python Dict with classlike access to its contents (dot.notation,creates missing keys on the fly,...)

## Dict VS Clict:
### Creation & Initialisation:
 Dict only one step:
```py
x={'y': 'z'}
```
or
```py
x=dict(y=z)
```

Clict you need to call the class first:
```py
a=Clict()
```
Then these work:
```py
a.b='c' 				
	# or
a['b']= 'c'
# you can call the class and populate when doing so,
Clict(a=1, b=2) 

```
note: this works recursively if the key doesnt exist for that Clict , its created as a new Clict so this works
for initializing deeply nested 'dicts' :
```py
a=Clict()
a.b.c.d.e.f.g.h.i.j=''
```

### Usage:
you can both assign and recall values by the dot notation as with the conventional dict square brackets, and they can be mixed in a single lookup, However where you can create a dict with 
```py
a={}
```
Clict unfortunatly cannot be a drop in replacement for dicts as the only way to create one is by calling the Class on it. Then you can assign values to keys in it. 
```py
a=Clict(
)

```
