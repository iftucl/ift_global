from typing import Union
import css_inline
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from ift_global.email.css_stylesheets.footer import footer


def jinja_to_html(template_dir: str, template_name: str, stylesheet: str, loc_vars) -> str:
    """
    Build Jinja.

    Builds from Jinja2 template to HTML.

    ----------
    :param str template_dir: Directory containing Jinja2 templates.
    :param str template_name: Jinja template file for conversion.
    :param str stylesheet: Character string containing CSS styling.
        Make sure you include in your Jinja template the following
        line at the top of the doc:
        <style>
            {{stylesheet}}
        </style>
    :return: HTML document in the form of a string

    :Examples:
            >>> html_table = sirs_common.email.html_tools.jinja_to_html(
            ...     template_dir='/path/to/docs/', 
            ...     template_name='my_template.j2',
            ...     stylesheet='2',
            ...     loc_var=vars()
            ... )
    """
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'htm', 'xml'])  # Enable autoescaping for HTML and XML files
    )
    
    env.globals = {**env.globals, **loc_vars}
    env.globals['build_html_table'] = build_html_table
    env.globals['style_sheet'] = stylesheet
    
    template = env.get_template(template_name)
    html_body = template.render() + footer
    inliner = css_inline.CSSInliner(keep_style_tags=True)

    return inliner.inline(html_body)


def build_html_table(input_data: Union[list, dict, pd.DataFrame]) -> str:
    """
    Build an HTML table from various input data types.

    This function creates an HTML table representation from a dictionary, 
    a list of dictionaries, or a pandas DataFrame.

    :param input_data: The data to be converted into an HTML table
    :type input_data: Union[list, dict, pd.DataFrame]
    :return: HTML string representing a table
    :rtype: str
    :raises TypeError: If the input_data is not a dict, list, or DataFrame
    :raises ValueError: If the list of dictionaries have inconsistent keys

    :Example:

    >>> import pandas as pd
    >>> from sirs_common.email.html_tools import build_html_table
    >>> 
    >>> # Using a pandas DataFrame
    >>> df_input = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    >>> html_table = build_html_table(df_input)
    >>> 
    >>> # Using a dictionary
    >>> dict_input = {"A": [1, 2], "B": [3, 4]}
    >>> html_table = build_html_table(dict_input)
    >>> 
    >>> # Using a list of dictionaries
    >>> list_input = [{"A": 1, "B": 3}, {"A": 2, "B": 4}]
    >>> html_table = build_html_table(list_input)

    .. note::
       - If a dictionary is provided, each key should have a list (vector) representing a column.
       - If a list is provided, all dictionaries within the list must have the same keys.
       - The function will sort the keys alphabetically when creating the table headers.

    .. warning::
       Ensure that all data can be safely converted to strings, as the function 
       uses `str()` to convert values when building the table.
    """
    class_type = input_data.__class__.__name__
    
    if class_type not in ('dict', 'list', 'DataFrame'):
        raise TypeError(f'Class type must be dict, list, or pd DataFrame; you provided {class_type}')

    if isinstance(input_data, pd.DataFrame):
        input_data = input_data.to_dict('list')

    if isinstance(input_data, dict):
        html = '<table><tr><th>' + '</th><th>'.join(input_data.keys()) + '</th></tr>'
        for row in zip(*input_data.values()):
            row_char = [str(val) for val in row]
            html += '<tr><td>' + '</td><td>'.join(row_char) + '</td></tr>'
    elif isinstance(input_data, list):
        sorted_input = sorted(input_data[0])
        html = '<table><tr><th>' + '</th><th>'.join(sorted_input) + '</th></tr>'
        
        for dict_items in input_data:
            try:
                sorted_items = [str(dict_items[item_key]) for item_key in sorted_input]
                html += '<tr><td>' + '</td><td>'.join(sorted_items) + '</td></tr>'
            except KeyError as e:
                print(e.__cause__)
                raise ValueError('All dictionaries within this list must have the same keys. Not possible to build table.')
    
    html += '</table>'
    
    return html


def inject_stylesheet(html_string: str, style_sheet: str) -> str:
    """
    Inject stylesheet into HTML.

    :param html_string: HTML body as a character string.
    :type html_string: str
    :param style_sheet: A stylesheet as per CSS stored in sirs_common.
    :type style_sheet: str
    :return: Enriched HTML string.
    :rtype: str
    """
    
    if html_string.startswith('<html>'):
        html_string = html_string.replace('<html>', '')
    
    html_enriched = '<html><style>{}</style>{}'.format(
        style_sheet,
        html_string
    )

    if not html_enriched.endswith('</html>'):
        html_enriched += ''.join([footer, '</html>'])
    else:
        html_enriched = html_enriched.replace('</html>', ''.join([footer, '</html>']))

    inliner = css_inline.CSSInliner(keep_style_tags=True)

    return inliner.inline(html_enriched)