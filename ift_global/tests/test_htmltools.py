from ift_global.email.html_tools import build_html_table, inject_stylesheet
from ift_global.email.css_stylesheets import stylesheet_two
import pandas as pd
import pytest


def test_dataframe_to_html():
    input_data = pd.DataFrame({'a' : [2, 10]})
    assert isinstance(build_html_table(input_data=input_data), str)
    assert build_html_table(input_data=input_data) == '<table><tr><th>a</th></tr><tr><td>2</td></tr><tr><td>10</td></tr></table>'

def test_list_of_dictionary_to_html():
    input_data = [{'a' : 2, 'b' : 8, 'c' : 4}, {'c' : 2, 'a' : 3, 'b' : 4}, {'c' : 2, 'b' : 3, 'a' : 5}]
    assert isinstance(build_html_table(input_data=input_data), str)
    assert build_html_table(input_data=input_data) == '<table><tr><th>a</th><th>b</th><th>c</th></tr><tr><td>2</td><td>8</td><td>4</td></tr><tr><td>3</td><td>4</td><td>2</td></tr><tr><td>5</td><td>3</td><td>2</td></tr></table>'

def test_dictionary_of_lists_to_html():
    input_data = {'a' : [2, 15, 16], 'b' : [3, 24, 10], 'c' : [4, 13, 23]}
    assert isinstance(build_html_table(input_data=input_data), str)
    assert build_html_table(input_data=input_data) == '<table><tr><th>a</th><th>b</th><th>c</th></tr><tr><td>2</td><td>3</td><td>4</td></tr><tr><td>15</td><td>24</td><td>13</td></tr><tr><td>16</td><td>10</td><td>23</td></tr></table>'

def raise_unexpected_input_data_to_html_table():
    with pytest.raises(KeyError,   match='Class type must be dict list or pd df, you provided str'):
        build_html_table(input_data='abc')

def test_inject_stylesheet():
    html_string="""<html>
    <h1>My first e-mail</h1>    
    <br> 
    <p>Hello World </p>
    <div>
    <ul>
    <li>one</li>
    <li>two</li>
    </ul>
    </div>
    <div>
    <br>
    <table><tr><th>a</th><th>b</th><th>c</th></tr><tr><td>2</td><td>8</td><td>4</td></tr><tr><td>3</td><td>4</td><td>2</td></tr><tr><td>5</td><td>3</td><td>2</td></tr></table>
    </div>
    </html>"""
    assert inject_stylesheet(html_string=html_string, style_sheet=stylesheet_two).endswith('</body></html>')