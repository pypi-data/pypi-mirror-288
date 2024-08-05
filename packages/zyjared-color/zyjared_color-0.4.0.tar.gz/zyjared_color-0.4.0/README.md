# zyjared-color

Personal font color utility library for Python, primarily used in PowerShell.

## Installation

```sh
pip install zyjared-color
```

## Usage

### Basic Usage

Create a styled text using the `Color` class:

```python
from zyjared_color import Color

text = Color('Hello World!').red().bold()
print(text)
```

You can achieve the same result using `StaticColor` class methods:

```python
from zyjared_color import StaticColor as Colors

text = Colors.red('Hello World!').bold()
print(text)
```

Or using aliases:

```python
from zyjared_color import red, bold, italic

text = red('Hello World!').bold()
print(text)

text = italic(text)
print(text)
```

### Chaining Usage

You can chain multiple style methods together:

```python
from zyjared_color import red

text = red('Hello World!').bold().italic().underline().through()
print(text)
```

### Nested Usage

Combine different styling methods and functions:

```python
from zyjared_color import red, bold, italic, underline, through, blue

text = through(underline(italic(bold(red('Hello World!')))))
print(text)

# add more text
text = text + ' !!! ' + blue('Hello World!')
print(text)

# change text color
text.yellow()
print(text)
```

## HTML / CSS

```python
from zyjared_color.html import ColorHtml as Color, StaticColorHtml as StaticColor
from zyjared_color.html import blue, red, bold, italic, underline, through

text = ColorHtml('Hello World!').red().bold()
print(text)

# custom styles
text = ColorHtml("Hello World!", {"opacity": 0.5, "font-weight": "bold"})
print(text)
```

**example:** Display `ColorHtml` in Jupyter Notebook

```python
from zyjared_color.html import ColorHtml as Color, StaticColorHtml as StaticColor
from zyjared_color.html import blue, red, bold, italic, underline, through
from IPython.display import display, HTML

text = Color('Hello World!').red().bold()

# f'{text}' or str(text)
display(HTML(f'{text}'))
```
