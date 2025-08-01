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
    """
Takes a string and count then returns a list of count instances of string
    """
    repeat_list = []
    for _ in range(repeat_count):
        repeat_list.append(source_string)
    
    return repeat_list
```

Most if not all functions also use a statement like the one below to ensure that the correct type of object is being passed to funcitons, while not mandatory it is encouraged. 
```python
from utilites import ensure_type
ensure_type(instance, expected_type, variable_name)

```


I know that AI makes coding trivial, and that claude code can make this project from a single prompt.

But this is a Noble Code Project, and much in vein of someone selling handmade mugs on Etsy for $15 in 2012 I'm doing this because I want to, and because it's fun.

So please don't turn Claude code or cursor loose on this and open a PR with 8k new lines of code, I know there are a lot of things that can be done better, and they will be. 

Just have fun, and enjoy expressing behavior in logic.

- Andrew