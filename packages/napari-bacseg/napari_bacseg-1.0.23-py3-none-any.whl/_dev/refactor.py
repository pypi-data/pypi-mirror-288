import os
import xml.etree.ElementTree as ET
import re
def parse_ui_file(ui_file_path):

    tree = ET.parse(ui_path)
    root = tree.getroot()

    widgets = root.findall(".//widget")

    gui_elements = {}

    for widget in widgets:
        # Get the type of widget and its name property
        widget_type = widget.get('class')
        name = widget.get('name')

        if widget_type in ["QComboBox", "QCheckBox", "QLineEdit","QDoubleSpinBox",
                           "QSpinBox", "QSlider", "QLabel", "QPushButton","QProgressBar"]:

            gui_elements[name] = widget_type

    return gui_elements

def replacement(match):
    widget = match.group(1)
    if widget in qwidget_names:
        return f'self.gui.{widget}'
    return match.group(0)

ui_path = r"/napari_bacseg/GUI\widget_ui.ui"
gui_elements = parse_ui_file(ui_path)
qwidget_names = list(gui_elements.keys())

directory = r"C:\napari-napari_bacseg"


python_files = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            if "\\funcs\\" in path or "\\_widget.py" in path:
                if "GUI" not in path:
                    python_files.append(path)

pattern = re.compile(r'self\.(\w+)')

for path in python_files:

    if "gui.py" not in path and "bacseg_ui.py" not in path:

        with open(path, 'r') as f:
            content = f.read()

        updated_content = pattern.sub(replacement, content)

        with open(path, 'w') as f:
            f.write(updated_content)






