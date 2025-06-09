Title: Working Code Is Good CodeDate: 2025-06-06

Working Code Is Good Code

There are a lot of talented developers in this world who write elegant code. You look at it and marvel at how much gets done with so little. I'm not one of those developers. Honestly, calling myself a Python developer feels like an insult to the folks who do it for real. I'm more of a programming enthusiast than a professional. My one serious (hopefully commercial) project might eventually pay off.

Programming isn’t my 9 to 5. I write mostly for fun—except for when I’m banging my head on the desk trying to get that one serious project to work. I code an hour here, thirty minutes there—whenever I can. And because my life consists mostly of things other than software, I don’t have much time to make my code pretty. As a (real) developer friend once told me: working code is good code. So, I get it to work however I can. It's usually inelegant. Sometimes even awkward (hey, I just closed the circle!). But it works. And for me, that’s good enough.

Here’s an example.

The Problem: Sorting Names

I love Django. I've built a bunch of toys with it, including five or ten iterations of a personal library app (I'm a bibliophile, so I like to track what I own). My one serious project is also written in Django. What these projects have in common is the need to keep track of people’s names.

There are at least two things you always want to do with names: search and sort. Sorting by last name is especially common. The simplest way to do that is to use separate fields for first name, middle name, last name, and suffix (e.g. Jr., Sr., MD). That makes sorting easy: just sort by last_name.

But I hate that. I'd much rather type:

Charles Emerson Winchester, III

...than tab through four fields and enter:

Charles → [tab] Emerson → [tab] Winchester → [tab] III

I'm getting old. My hands get tired. I need to cut down on keystrokes.

So I built a little function that lets me enter a full name as a single string and then parses it into its parts. That way, I can just type "Charles Emerson Winchester, III" and still store and sort names however I like.

My Clunky but Clear Approach

Here’s the function:

from collections import namedtuple

def parse_name(full_name: str) -> namedtuple:
    Name = namedtuple("Name", "first_name, middle_name, last_name, suffix")
    suffixes = [
        "Jr", "Jr.",
        "Sr", "Sr.",
        "I", "II", "III", "IV", "V",
        "Esq", "Esq.",
        "MD", "M.D.",
        "PhD", "Ph.D."
    ]

    name_list = full_name.split()

    if name_list[-1] in suffixes:
        if len(name_list) == 2:
            first_name = ""
            middle_name = ""
            last_name = name_list[0]
            suffix = name_list[-1]
        elif len(name_list) == 3:
            first_name = name_list[0]
            middle_name = ""
            last_name = name_list[1]
            suffix = name_list[-1]
        else:
            first_name = name_list[0]
            middle_name = " ".join(name_list[1:-2])
            last_name = name_list[-2]
            suffix = name_list[-1]
    else:
        if len(name_list) == 1:
            first_name = ""
            middle_name = ""
            last_name = name_list[0]
            suffix = ""
        elif len(name_list) == 2:
            first_name = name_list[0]
            middle_name = ""
            last_name = name_list[-1]
            suffix = ""
        else:
            first_name = name_list[0]
            middle_name = " ".join(name_list[1:-1])
            last_name = name_list[-1]
            suffix = ""

    name = Name(first_name, middle_name, last_name.rstrip(","), suffix)
    return name

I know, I know—it’s not elegant. But it’s readable. It flows the way I think when I break names down. It doesn't rely on regex or clever one-liners. Just a list, a long if/else block, split() and join(), and a standard library import.

Running parse_name("Charles Emerson Winchester, III") returns:

Name(first_name='Charles', middle_name='Emerson', last_name='Winchester', suffix='III')

Nice, right?

Could It Be Prettier?

Absolutely. In fact, I asked ChatGPT to rewrite this function twice:

Version 1: More Elegant

from collections import namedtuple

Name = namedtuple("Name", "first_name middle_name last_name suffix")

SUFFIXES = {
    "Jr", "Jr.", "Sr", "Sr.", "I", "II", "III", "IV", "V",
    "Esq", "Esq.", "MD", "M.D.", "PhD", "Ph.D."
}

def parse_name(full_name: str) -> Name:
    parts = full_name.replace(",", "").split()
    suffix = parts[-1] if parts[-1] in SUFFIXES else ""
    parts = parts[:-1] if suffix else parts

    first = parts[0] if parts else ""
    last = parts[-1] if len(parts) > 1 else ""
    middle = " ".join(parts[1:-1]) if len(parts) > 2 else ""

    if len(parts) == 1:
        return Name("", "", parts[0], suffix)

    return Name(first, middle, last, suffix)

Version 2: Even Shorter

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

These are great. They're elegant and efficient. But I still prefer my version.

Why?

Why I Stick With Mine

Readability

My function flows in a way that mirrors how I mentally break down names. It’s verbose, but I can come back in six months and still understand it.

Stability

It uses only built-ins and one standard module. No dependencies. No surprises.

Intentional Simplicity

I know exactly what this function handles—and what it doesn’t. For example, it misparses names like "Oscar de la Cruz" (last name should be "de la Cruz"), but I can live with that for now. When I encounter an edge case I care about, I’ll handle it manually.

A Word About nameparser

Could I have used an existing package like nameparser? Absolutely—and in fact, I did. I loved it. It worked remarkably well and handled a bunch of edge cases. I even said I'd probably go back and refactor older projects to use it.

But here’s the thing: using nameparser didn’t help me understand the problem better. Writing my own function did. And for this project, where I needed something lightweight and wanted more hands-on control, rolling my own turned out to be a great little learning experience.

The Point

This function isn’t pretty. But it’s clear. It works. It gets the job done. It reflects how I think. That makes it good code—for me. And if you’re someone learning to code or working with limited time, don’t let cleverness be the enemy of clarity.

Write what works. Read it later. Fix what breaks. And maybe—just maybe—you’ll learn more doing it the awkward way.

Bob’s your uncle.