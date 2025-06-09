Title: Working Code is Good Code
Date: 2025-06-06

# Working Code is Good Code  

There are a lot of talented developers in this world who write very elegant code. You look at it and sit there in awe at how much gets done with so little. I'm not one of those developers. In fact, I think calling myself a Python developer is an insult to the folks who do it for real. I'm more of a programming enthusiast than a real developer. My one serious (hopefully commercial) project might pay off—eventually. 

Anyway, programming isn't my 9 to 5. I write mostly for fun except for when I'm banging my head on the desk trying to get that one serious project to work. I code an hour here, 30 minutes there--just whenever I can find the time. And because my life consists of almost entirely something other than software, I don't have a lot of time to focus on pretty code. As a (real) developer friend once told me, working code is good code. So, I get it to work however I can. And it's usually inelegant and, dare I say, awkward (Hey, I just closed the circle!). But it works and is, therefore good. For me, anyway. Here's an example of this "awkward python."  

I love Django. I've written many toys using Django, including 5 or 10 iterations of a library app (I'm kind of a bibliophile, so I like to keep track of what I own). My only "serious" project is also written using Django. What both have in common is keeping track of people's names. And, of course, there are at least two things we always want to be able to do with names: search for them and sort them. It's the sorting that got me thinking. If I want to sort a list of names by last name, the most obvious solution is, when inputting the names, use separate fields for first name, middle_name, last_name, and suffix (e.g. Jr. Sr. MD, etc). It's a simple solution used by many thousands of applications. This makes sorting a trivial matter. Just sort by `last_name`. But I hate it. I'd much rather type "Charles Emerson Winchester, III" than "Charles" [tab] "Emerson" [tab] "Winchester" [tab] "III." I'm getting old. My hands get tired. I need to cut down on my keystrokes.  

Since I do this kind of thing a fair amount, I wanted to automate the process of separating a full name into its parts and auto-populating database fields with the parts. That way, I can just type "Charles Emerson Winchester, III" and still sort names any way I like. So I did what any self-respecting Python developer would do and wrote a function. So, how does it work?     

We start by importing `namedtuple`, defining the function (which has a single `full_name` parameter), creating a named tuple `Name`, and then listing possible name suffixes, e.g. Jr., Sr., II, etc. This is our first act of deliberate, if clunky, simplicity. I want the function to identify the use of suffixes and doing a simple check against a list of possibles is the simplest way I know to do it. Sure, I could write a regex pattern that would better handle some edge cases like multi-word, unhyphenated last names, e.g. "Oscar de la Cruz" (which this function parses as first_name="Oscar", middle_name="de la", last_name="Cruz)", but that's a tradeoff I'm willing to live with for ease of readability. This way, we know exactly what we're looking at and because this isn't some enterprise-level, critical application, we're ok (or at least I'm ok) with having to handle the edge cases manually.

```python
from collections import namedtuple


def parse_name(full_name: str) -> namedtuple:
    """Returns named tuple for first name, middle name, last name, and suffix from a 
    full name input as string. For example, 'Charles Emerson Winchester, III' returns
    Name(first_name="Charles", middle_name='Emerson', last_name='Winchester', suffix='III')"""

    Name = namedtuple("Name", "first_name, middle_name, last_name, suffix")
    suffixes = [
        "Jr", "Jr.",
        "Sr", "Sr.", 
        "I", "II", "III", "IV", "V",
        "Esq", "Esq.",
        "MD", "M.D.",
        "PhD", "Ph.D."
    ]
```

Next, we use the built-in `.split()` method on the full name to separate the string at the spaces, making a list of the as-yet undefined name parts. Then there's the longish if/else block. It first determines whether there is suffix then walks through the possible name configurations. If there's only a suffix and one other string, we assume that the other string is a last name. If there is a suffix and two other strings, it's a safe bet that the other two strings are first name and last name, respectively. Finally, if there is a suffix and three or more additional strings, we assume that the first string is the first name, the next to last string (index position -2) is a last name, and the rest one or more middle names.

```python
    name_list = full_name.split()

    # First determine whether there is a suffix
    if name_list[-1] in suffixes:
        # Last name and suffix
        if len(name_list) == 2:
            first_name = ""
            middle_name = ""
            last_name = name_list[0]
            suffix = name_list[-1]
        # First name, last name, suffix
        elif len(name_list) == 3:
            first_name = name_list[0]
            middle_name = ""
            last_name = name_list[1]
            suffix = name_list[-1]
        # First name, middle name(s), last_name, suffix
        else:
            first_name = name_list[0]
            middle_name = " ".join(name_list[1:-2])
            last_name = name_list[-2]
            suffix = name_list[-1]
```

Finally, we go through the same steps determining which string in the list corresponds to which place in the name when there is no suffix. Again, we plow through the possible combinations, one by one. Nothing fancy. No clever shortcuts or complex pattern matching or ridiculous regex patterns (I think all regex patterns are ridiculous--awesome and immensely useful--but still ridiculous). And it's very easy to walk through each conditional and discern what the code is doing.

```python
    else:
        # One name is treated like last name, e.g. Plato, Aristotle, since last name is the most common sorting pattern
        if len(name_list) == 1:
            first_name = ""
            middle_name = ""
            last_name = name_list[0]
            suffix = ""
        # Two names assumed to be first name, last name
        elif len(name_list) == 2:
            first_name = name_list[0]
            middle_name = ""
            last_name = name_list[-1]
            suffix = ""
        # Finally, three or more assumed to be first name, middle name(s), last name
        else:
            first_name = name_list[0]
            middle_name = " ".join(name_list[1:-1])
            last_name = name_list[-1]
            suffix = ""
    
    # Create and assign name to namedtuple; strip any comma between last name and suffix
    name = Name(first_name, middle_name, last_name.rstrip(","), suffix)
    return name
```

See, inelegant but simple, not a single regex or optimized third party library to be found. Just a list, a longish `if/else` block, the `.split()` and `"".join()` methods, and Bob's your uncle. Running `parse_name("Charles Emerson Winchester, III")` returns `Name(first_name='Charles', middle_name='Emerson', last_name='Winchester', suffix='III')`. Nice, huh?  

So what's my point? There is absolutely nothing sexy or elegant about this function. It uses lists, built-in methods, index references, one standard library module, and explicitly defines and steps through the different combinations of first_name, middle_name, last_name, and suffix. Can this be written more succintly? More elegantly? In such a way that it doesn't look like it was written by someone who just finished Chapter 3 of some "Learn Python" book? Yup. In fact, I asked ChatGPT to rewrite this function twice. First, I instructed it to write the function "as a very experienced developer who writes concise, elegant, efficient code." 26 lines of code later (vs. my 55), the job is done (using essentially the same approach)  

```python
from collections import namedtuple

Name = namedtuple("Name", "first_name middle_name last_name suffix")

SUFFIXES = {
    "Jr", "Jr.", "Sr", "Sr.", "I", "II", "III", "IV", "V",
    "Esq", "Esq.", "MD", "M.D.", "PhD", "Ph.D."
}


def parse_name(full_name: str) -> Name:
    """Parse a full name into first, middle, last, and suffix components."""
    parts = full_name.replace(",", "").split()
    
    suffix = parts[-1] if parts[-1] in SUFFIXES else ""
    parts = parts[:-1] if suffix else parts

    first = parts[0] if parts else ""
    last = parts[-1] if len(parts) > 1 else ""
    middle = " ".join(parts[1:-1]) if len(parts) > 2 else ""

    # Handle single-name input
    if len(parts) == 1:
        return Name("", "", parts[0], suffix)

    return Name(first, middle, last, suffix)

```
Next, I told ChatGPT to "rewrite my original function in a way that is not convoluted or confusing but still in as few lines of code as possible. You are free to use any library in the Python standard library or any known third party library as long as it assist you in carrying out these instructions. The output doesn't have to be a named tuple. I just need output that separates the name into its parts." In 24 lines, it produces a working function using `re` and a dictionary -- a different approach than mine, but same end result.

```python
import re

SUFFIXES = {
    "Jr", "Jr.", "Sr", "Sr.", "I", "II", "III", "IV", "V",
    "Esq", "Esq.", "MD", "M.D.", "PhD", "Ph.D."
}

def parse_name(full_name: str) -> dict:
    parts = re.sub(r",", "", full_name).split()
    suffix = parts.pop() if parts and parts[-1] in SUFFIXES else ""

    first = parts[0] if parts else ""
    last = parts[-1] if len(parts) > 1 else ""
    middle = " ".join(parts[1:-1]) if len(parts) > 2 else ""
    
    if len(parts) == 1:
        first, middle, last = "", "", parts[0]

    return {
        "first_name": first,
        "middle_name": middle,
        "last_name": last,
        "suffix": suffix
    }

```

These are both great solutions. So why do I still use (and prefer) my awkward, clunky but clear function? Because it’s mine, it works, and I can read and understand it. And I'm reasonably confident that in 10 years, it's still going to work.

## Readability 
The function flows linearly and "reasons" about the process in much (but not entirely) same way I reason about it in my head when I look at a name on a page and identify the parts. And because it follows what I view to be an organic pattern, I can come back to the code in six months and still know what I'm looking at without having to Google a regex flag.

## Stability
I intentionally wrote this function using only built-ins and one standard library module (Rewriting it with nothing but built-ins would be trivial). This means that unless there is a complete, fundamental rewrite of the Python language (in which case would it be Python? Think "Ship of Theseus"), this function will still work. I don't have to worry about Python 3.58 breaking my code. 

## But ...
This function has its issues. It makes a lot of simplistic assumptions about the way names are structured. It's culturally/linguistically limited to common (western) English. It doesn't handle any real edge cases. 

When I wrote this function, I assumed that there were existing pypi packages that would do the same thing and do it better, but I intentionally avoided them. I assumed they would probably do more than I needed and I wanted something short, simple, and tailor-made for my use-case. But when writing this post, I decided to do some exploring. As I expected, I'm by no means the first person to consider this problem. In particular, I found [Python-Nameparser](https://pypi.org/project/nameparser/). It's quite a remarkable and useful package, doing the same thing my function does but with additional features and great performance even in edge cases. It's somewhere between 2000 and 3000 lines of code, but it is well-written, well-structured, and remarkably easy to understand (even if it does make limited use of dreaded regexes). I'm pretty sure I'll be using this library moving forward rather than my own (which I have also published to pypi in a slightly but inconsequentially modified form). I may even refactor existing projects to use it.

So did I waste my time writing this function and, for that matter, this article? 

Because writing my own version taught me more than just reading the docs ever could. It helped me understand the problem, try solutions, and reason about edge cases in a hands-on way (even if I didn't solve them). And because the resulting code is mine—ugly, long-winded, plain—it makes sense to me. When it breaks (if it breaks), I know how to fix it.

There’s value in that.


And if you're in the early stages of learning to code—or just trying to write things that work instead of win awards—I hope this encourages you. Clever is fine. But clear is better. And sometimes the longest road is the one that gets you there with the fewest regrets.

Bob’s your uncle.

 

