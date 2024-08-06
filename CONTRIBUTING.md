## Contributing

This project is now openly accepting contributions.

Please create a branch from `main` and open a PR (Pull Request) for approval.

PRs should include a reasonable description of the changes made and must pass a test run of `python3 main.py --auto`.

All PRs are subject to approval and may be rejected or returned pending additional development.

Please make a point of pulling from `main` regularly to avoid merge conflicts.

This project is built with the intention of running on any Python environment. As such, the use of non-standard packages is not allowed; this unfortunately includes UI libraries like Turtle, Curses, or Tkinter. This is an intentional part of the project design and goals.

## Roadmap

There is not an offical roadmap but the general planning and ideas for progress are kept in `todo.md`

Looking for ideas? Check out `todo.md`.

Have some ideas? Add them to `todo.md`.

Find a bug? Open an issue or add it to `bugs.md`.

## Code Standards

All functions should have basic type hinting and ideally a description. Below is an example function:

```python
def string_repeater(source_string: str, repeat_count: int) -> list:
    repeat_list = []
    for _ in range(repeat_count):
        repeat_list.append(source_string)
    
    return repeat_list
```

Most if not all functions also use a statement like the one below to ensure that the correct type of object is being passed to funcitons, while not mandatory it is encouraged. 
```python
if not isinstance(input_varible, bool):
        raise ValueError("The 'input_varible' parameter must be of type bool. Received type: {}".format(type(input_varible).__name__))
```


There is an expectation that nearly all functions should be part of a class that handles them. There will always be exceptions, but do your best to avoid orphan functions and please use the `@staticmethod` decorator where applicable.