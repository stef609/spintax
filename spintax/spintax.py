import re
import random
# Import warnings and enable DeprecationWarning's for parse function
import warnings
warnings.simplefilter('always', DeprecationWarning)


def _replace_string(match):
    """
    Function to replace the spintax with a randomly chosen string
    :param match object:
    :return string:
    """
    global spintax_seperator
    random_picked = random.choice(re.findall(spintax_seperator, match.group(2)))
    return match.group(1) + random_picked + match.group(3)


def spin(string, seed=None):
    """
    Function used to spin the spintax string
    :param string:
    :param seed:
    :return string:
    """

    # If the user has chosen a seed for the random numbers use it
    if seed is not None:
        random.seed(seed)

    # Regex to find spintax seperator, defined here so it is not re-defined
    # on every call to _replace_string function
    global spintax_seperator
    spintax_seperator = r"(?:\\.|[^\|\\])+|(?<=[^\\]\|)|(?<!.)(?=\|)|(?<!.)(?=\|)|(?<=\|)(?=\|)"
    spintax_seperator = re.compile(spintax_seperator)

    # Regex to find all non escaped spintax brackets
    spintax_bracket = r'(?<!\\)((?:\\{2})*)\{([^}{}]+)(?<!\\)((?:\\{2})*)\}'
    spintax_bracket = re.compile(spintax_bracket)

    # Need to iteratively apply the spinning because of nested spintax
    while True:
        new_string = re.sub(spintax_bracket, _replace_string, string)
        if new_string == string:
            break
        string = new_string

    # Replaces the literal |, {,and }.
    string = re.sub(r'\\([{}|])', r'\1', string)
    # Removes double \'s
    string = re.sub(r'\\{2}', r'\\', string)

    return string


def parse(string, seed=None):
    """
    Old function used will be removed use spin() instead
    :param string:
    :param seed:
    :return list:
    """
    warnings.warn(
        "This function (parse) is being depreciated, please use spin(string)",
        DeprecationWarning
    )
    return [spin(string, seed)]
