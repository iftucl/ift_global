from ift_global.email.css_stylesheets.stylesheet_one import stylesheet_one
from ift_global.email.css_stylesheets.stylesheet_two import stylesheet_two
from ift_global.email.css_stylesheets.stylesheet_three import stylesheet_three


stylesheets = {
    "1": stylesheet_one,
    "2": stylesheet_two,
    "3": stylesheet_three,
}

__all__ = [
    "stylesheets",
    "stylesheet_one",
    "stylesheet_two",
    "stylesheet_three",
]