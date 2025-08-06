# Coding Standards

This codebase seeks to have ~~perfect~~ very good runtime and static type validation, so all functions must be type hinted for inputs and outputs. 

The use of the `Any` type is restricted to dealing with data who's type is considered "unknowable" or is outside the scope of responsibility of the given function. Examples of this can be seen in the cascading init functions in [`enemy_library.py`](../RPyG/content/enemy_library.py) when `Any` is used to mark where a given class no longer needs to have the data on what it is passing down as those downstream functions are responsible for that. also because having a type hint of `dict[str, dict[str, list[list[dict[str, str | int | bool | None]]]]]` is far less useful to everyone.


This project is hard locked to the standard library of python and is out right forbidden from using any external library (if you need pip to install it, you can't use it). This is part of the core and original goal of this project is to study python and learn the concepts of object oriented programming and programming as a whole.

The code in this project has a very aggressive defensive programming strategy, this leads to less bugs, better debugging, and protection from malformed user input (benign or otherwise). As such the follow code patterns are disallowed entirely.

The `ensure_type` function should be used to check the to the full depth of the type hint in your function inputs (until you reach the `Any` barrier at least)

### Implicit Boolean
This serves a dual purpose, it makes the intent of comparison very clear, and also avoids the "Truthiness Trap" where values that are non-truthy can be converted to a truthy by intentional or accidental type conversion. Such as in the example below, where `None` will be converted to `"None"` which is not an empty string and there for is considered Truthy.

```python
# Don't do this
if X:
    print("text")
if not Y:
    print("Text")
```

```python
port = str(os.getenv("port_number"))
if port:
    database.connect(port)
```

### Inline For Loop (List | Dict Comprehensions)
This also has 2 benefits, better code clarity as it is bluntly obvious what the intent of the operation is, and maintainability, as inline loop must be re-written as standard for loop if more than Exactly one operation is needed in the loop. Also the net diff in characters of code typed is so small that this is a trick solely reserved for code golf
```python
# Inline (84 char) Don't do this
class_instances = [Class(**class_content) for class_content in class_data.values()]

# Explicit (114 char including newlines & Spaces)
class_instances = []
for class_content in class_data.values():
    class_instances.append(Class(**class_content))
```

### Inline If Statement
This one is very similar to the last, save about 10 key strokes and mean that someone else needs to rewrite your operation later when it needs to do more than exactly one thing.
```python
# Inline (64 Char) Don't do this
def get_sign(number: int) -> str:
    return "Positive" if n > 0 else "Negative" if n < 0 else "Zero"

# Inline (96 Char including newlines & Spaces)
def get_sign(number: int) -> str:
    if n > 0:
        return "Positive"
    if n < 0:
        return "Negative"
    else "Zero"
```

### Single letter variable names
I feel this should be obvious but it is not 1954 and memory does not cost $1 per bit, so please use a real name for your variables. If you want to stack for loops and feel the need to use i, j, k  using `index`, `jndex`, and `kndex` is allowed, but I will rewrite those names before merging.
```python
# Don't do this - single letter variables make intent unclear
for i in range(len(parties)):
    for j in range(len(parties[i].members)):
        for k in range(len(inventory_items)):
            if parties[i].members[j].can_use(inventory_items[k]):
                parties[i].members[j].equip(inventory_items[k])
                break

# Do this - descriptive names make the logic obvious
for party_index in range(len(parties)):
    for member_index in range(len(parties[party_index].members)):
        for item_index in range(len(inventory_items)):
            current_member = parties[party_index].members[member_index]
            current_item = inventory_items[item_index]
            if current_member.can_use(current_item):
                current_member.equip(current_item)
                break

# Even better - use the actual objects when possible
for party in parties:
    for member in party.members:
        for item in inventory_items:
            if member.can_use(item):
                member.equip(item)
                break
```

### AI
This project actually predates the release of ChatGPT 3 buy a hand full of months (I started in October of 2022) and at it's core has always been about learning, practice and the joy of writing code to do things that are fun and interesting. 

The simple joy of expressing behavior in logic, and as is stated in [`CONTRIBUTING.MD`](../CONTRIBUTING.md) I know very well how quickly any modern AI tool like claude code (which I use for every single project that is not this by the way) could build any imaginable feature, rewrite the code in Rust, Go and IBM Cobol and add IaC for a server-less micro-service deployment to all 3 major CSP's in less time than a single person could read this whole codebase, and I think that is wonderful. 

But this is not the place for that. This project is a place to study the process of software craft, which means doing 500 refactors by hand because you notice all the weird stuff. Rewriting the same file 10 time because something about it feels weird. 

There are no KPIs no deadlines, no talent discussions. this is a safe place to build and have fun, so leave the power tools and home, grab a screwdriver and let's build something fun and cool.

-AJ