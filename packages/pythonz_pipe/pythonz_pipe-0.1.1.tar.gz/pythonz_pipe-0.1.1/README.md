# pythonz_pipe

simple implementation of pipe for pythonz

# example

```python
from pythonz_pipe import pipe

print(pipe(5).and_then(range).then_finally(list))  # [0, 1, 2, 3, 4]
print(pipe(5) / range // list)  # [0, 1, 2, 3, 4]
f = pipe().and_then(range).and_then(list)
print(f.call(5))  # [0, 1, 2, 3, 4]
print(f(5))  # [0, 1, 2, 3, 4]
```
