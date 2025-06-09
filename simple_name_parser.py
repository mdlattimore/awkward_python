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