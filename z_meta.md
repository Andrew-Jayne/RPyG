🧠 What is Metaprogramming Really?

At its core:

Metaprogramming is code that manipulates or generates other code — during runtime, compile-time, or even before.

In Python specifically, it means:
	•	Writing functions or classes that create, alter, or wrap other classes/functions.
	•	Leveraging introspection, decorators, type manipulation, and metaclasses to define reusable, flexible, dynamic behavior without writing everything by hand.

⸻

🧰 Key Forms of Metaprogramming in Python

Technique	Description	Use Case Example
Decorators	Wrap or modify functions/classes	@property, @dataclass, @staticmethod
Introspection	Inspect classes, methods, fields at runtime	dir(obj), hasattr(), type(), __dict__
Dynamic class creation	Build new classes on the fly	type("MyClass", (Base,), {...})
Metaclasses	Customize class creation itself	ORMs like SQLAlchemy, Django models
Code generation	Emit Python source from templates or data	Protocol buffer generators, DSLs
Generic typing hacks	Modify or analyze types	Generic[T], TypeVar, __class_getitem__


⸻

🔧 So… What Does It Look Like?

Here are real Python examples of metaprogramming in action.

⸻

🌀 1. Custom Decorator (classic intro)

def log_call(fn):
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__} with {args} {kwargs}")
        return fn(*args, **kwargs)
    return wrapper

@log_call
def say_hi(name):
    return f"Hi {name}"

Result:

say_hi("Alice")
# Calling say_hi with ('Alice',) {}
# 'Hi Alice'

Here you’re literally injecting code into another function.

⸻

🧱 2. Dynamic Class Creation

attrs = {"x": 42, "show": lambda self: print(self.x)}
MyDynamicClass = type("MyDynamicClass", (object,), attrs)

obj = MyDynamicClass()
obj.show()  # prints: 42

You just created a class… at runtime.

⸻

🧬 3. Metaclass (real metaprogramming)

class Meta(type):
    def __new__(cls, name, bases, dct):
        print(f"Building class: {name}")
        dct["injected"] = lambda self: "I'm injected"
        return super().__new__(cls, name, bases, dct)

class MyClass(metaclass=Meta):
    pass

m = MyClass()
print(m.injected())  # "I'm injected"

Metaclasses let you customize the class creation process itself.
You can:
	•	Enforce structure
	•	Auto-register classes
	•	Inject methods or properties
	•	Do serialization magic

⸻

⚙️ 4. Generic Type Magic (what you’re close to)

from typing import TypeVar, Generic

T = TypeVar("T")

class Wrapper(Generic[T]):
    def __init__(self, value: T):
        self.value = value

def unwrap_type(typ):
    print(typ.__origin__)  # Wrapper
    print(typ.__args__)    # (int,)

unwrap_type(Wrapper[int])

You’re already playing in this space. This is runtime type manipulation — a mild but useful form of metaprogramming, especially when building extensible systems (e.g., asset registries, content pipelines, or interpreters).

⸻

🧠 When Should You Use Metaprogramming?

✅ Use it when:
	•	You need to reduce boilerplate across similar classes or functions
	•	You’re building extensible systems or frameworks
	•	You want to validate or alter class structures
	•	You’re automating registration, binding, or serialization

🛑 Avoid it when:
	•	The behavior could be done more cleanly with composition
	•	It makes the codebase unreadable or opaque
	•	You’re adding cleverness instead of clarity

⸻

💡 Real Use Cases
	•	@dataclass dynamically builds __init__, __repr__, etc.
	•	pydantic uses metaclasses + descriptors to validate models
	•	Django models use metaclasses to register fields
	•	ORMs dynamically build SQL mappings
	•	Games: autoload entities, register attack types, enforce field layouts

⸻

✅ TL;DR

Concept	Python Tool
Wrap a function	@decorator
Modify a class	metaclass
Generate a class	type(name, bases, dict)
Reflect on structure	dir(), __annotations__
Automate logic	Combine the above