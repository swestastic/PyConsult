import re

with open('Windows/DataStreamWindow.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix docstrings
text = text.replace('\"\\\"\"Create all sensor display frames\\\"\"\"', '\"\"\"Create all sensor display frames\"\"\"')
text = text.replace('\"\\\"\"Create a full semi-circular gauge with text inside.\\\"\"\"', '\"\"\"Create a full semi-circular gauge with text inside.\"\"\"')
text = text.replace('\"\\\"\"Move gauge needle and update text.\\\"\"\"', '\"\"\"Move gauge needle and update text.\"\"\"')
text = text.replace('\"\\\"\"Update all displayed values from the ReadStream\\\"\"\"', '\"\"\"Update all displayed values from the ReadStream\"\"\"')

text = text.replace('\"', '\"')

with open('Windows/DataStreamWindow.py', 'w', encoding='utf-8') as f:
    f.write(text)
