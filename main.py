import sys
import os
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,

    QTextEdit,
    QTextBrowser,
    QLabel,
    QPushButton,
    QInputDialog,
    QScrollArea
)
from PyQt6.QtGui import QKeySequence, QShortcut
from markdown2 import markdown
import qtawesome as qta
from PyQt6.QtCore import Qt, QSize

# TODO: Add markdown rendering
# TODO: add notes delete feature
# TODO: add search feature

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.file_name = ''
        # Check if notes folder exists or not, if not then create one.
        if os.path.exists(os.path.expanduser('~/notes')) == False:
            os.makedirs(os.path.expanduser('~/notes'))

        os.chdir(os.path.expanduser("~/notes"))

        self.setWindowTitle("Gimli")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(800)

        # Sidebar
        self.side_bar = QWidget(self)
        self.side_bar.setMaximumWidth(50)
        scratch_pad_icon = qta.icon('ph.notepad')
        scratch_pad = QPushButton(scratch_pad_icon, '')
        scratch_pad.setIconSize(QSize(22, 22))
        scratch_pad.clicked.connect(self.change_scratch_pad_view)
        notes_icon = qta.icon('mdi.notebook')
        notes = QPushButton(notes_icon,'')
        notes.setIconSize(QSize(22, 22))
        notes.clicked.connect(self.change_notes_view)
        side_bar_layout = QVBoxLayout()
        self.side_bar.setLayout(side_bar_layout)
        side_bar_layout.addWidget(scratch_pad)
        side_bar_layout.addWidget(notes)
        side_bar_layout.addStretch()

        # Scratch Pad
        self.scratch_pad_widget = QWidget()
        scratch_pad_widget_layout = QVBoxLayout()
        self.scratch_pad_widget.setLayout(scratch_pad_widget_layout)
        self.scratch_pad_edit_text = QTextEdit()
        self.scratch_pad_edit_text.setTabStopDistance(4*4)
        self.scratch_pad_edit_text.setStyleSheet('padding: 15px; font-size: 18px')
        with open('scratch_pad.md', 'r') as f:
            self.scratch_pad_edit_text.setPlainText(f.read())
        self.scratch_pad_edit_text.textChanged.connect(self.save_scratch_pad)
        scratch_pad_label = QLabel('Scratch Pad')
        scratch_pad_label.setStyleSheet('font-size: 25px; font-weight: bold;')
        scratch_pad_widget_layout.addWidget(scratch_pad_label)
        scratch_pad_widget_layout.addWidget(self.scratch_pad_edit_text)

        # Scrollable File View Widget
        self.file_view_scroll_area = QScrollArea()
        self.file_view_scroll_area.setWidgetResizable(True)
        self.file_view_content = QWidget()
        self.file_view_content.setMinimumWidth(100)
        self.file_view_layout = QVBoxLayout(self.file_view_content)
        self.file_view_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.file_view_scroll_area.setWidget(self.file_view_content)

        file_create_button_icon = qta.icon('ei.plus')
        file_create_button = QPushButton(file_create_button_icon,'')
        file_create_button.clicked.connect(self.create_file)
        self.file_view_layout.addWidget(file_create_button)
        self.file_view_layout.addWidget(QLabel('All Notes'))

        self.button_list = []
        for filename in os.listdir():
            if os.path.isfile(filename) and filename != "scratch_pad.md":
                filename = filename.split('.')[0]
                self.add_file_button(filename)

        # Notes Widget
        self.notes_widget = QWidget(self)
        notes_widget_layout = QHBoxLayout()
        self.notes_widget.setLayout(notes_widget_layout)

        self.notes_editor = QWidget(self)
        self.notes_editor_layout = QVBoxLayout()
        self.notes_editor.setLayout(self.notes_editor_layout)

        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet("padding: 15px; font-size: 18px")
        self.text_edit.setTabStopDistance(4*4)
        self.text_edit.textChanged.connect(self.save_file)

        self.notes_mode = 'View'
        self.markdown_viewer = QTextBrowser()
        self.markdown_viewer.setOpenExternalLinks(True)
        self.markdown_viewer.setStyleSheet('padding: 15px;')
        self.markdown_viewer.hide()

        # Notes heading
        self.notes_heading_widget = QWidget()
        self.notes_heading_widget_layout = QHBoxLayout()
        self.notes_heading_widget.setLayout(self.notes_heading_widget_layout)
        self.notes_title = QLabel(self.file_name)
        self.toggle_markdown = False
        self.markdown_render_btn = QPushButton(self.notes_mode)
        self.markdown_render_btn.hide()
        self.markdown_render_btn.clicked.connect(self.render_markdown)
        self.notes_title.setStyleSheet('font-size: 25px; font-weight: bold;')
        self.notes_heading_widget_layout.addWidget(self.notes_title)
        self.notes_heading_widget_layout.addStretch()
        self.notes_heading_widget_layout.addWidget(self.markdown_render_btn)
        self.notes_title.hide()

        self.notes_editor_layout.addWidget(self.notes_heading_widget)
        self.notes_editor_layout.addWidget(self.text_edit)
        self.notes_editor_layout.addWidget(self.markdown_viewer)

        notes_widget_layout.addWidget(self.file_view_scroll_area)
        notes_widget_layout.addWidget(self.notes_editor)

        notes_widget_layout.setStretchFactor(self.file_view_scroll_area, 1)
        notes_widget_layout.setStretchFactor(self.notes_editor, 5)

        # Root layout
        self.root_layout = QHBoxLayout()
        self.setLayout(self.root_layout)
        self.root_layout.addWidget(self.side_bar)
        self.root_layout.addWidget(self.notes_widget)

        self.root_layout.setStretchFactor(self.side_bar, 1)
        self.root_layout.setStretchFactor(self.notes_widget, 10)

        self.show()

    def change_scratch_pad_view(self):
        self.notes_widget.hide()
        self.scratch_pad_widget.show()
        self.root_layout.addWidget(self.scratch_pad_widget)
        self.root_layout.setStretchFactor(self.side_bar, 1)
        self.root_layout.setStretchFactor(self.scratch_pad_widget, 10)
    
    def save_scratch_pad(self):
        with open('scratch_pad.md', 'w') as f:
            f.write(self.scratch_pad_edit_text.toPlainText())

    def change_notes_view(self):
        self.scratch_pad_widget.hide()
        self.notes_widget.show()

    def create_file(self):
        text, ok = QInputDialog.getText(self, 'Create Note', 'Name of Your Note')
        if ok and text:
            file_path = text + '.md'
            if not os.path.exists(file_path):
                with open(file_path, 'x') as f:
                    pass
                self.add_file_button(text)

    def add_file_button(self, filename):
        temp_button = QPushButton(filename)
        temp_button.setStyleSheet('border: 0; background: transparent; text-align: left; padding: 10px;')
        temp_button.clicked.connect(self.file_edit)
        self.button_list.append(temp_button)
        self.file_view_layout.insertWidget(len(self.file_view_layout.children()) - 1, temp_button)

    def file_edit(self):
        clicked_button = self.sender() # get button detail for filename
        self.file_name = clicked_button.text() + '.md'
        self.notes_title.setText(clicked_button.text())
        self.notes_title.show()
        self.markdown_render_btn.show()

        # Read file
        with open(self.file_name, 'r') as f:
            self.text_edit.setPlainText(f.read())
            self.markdown_viewer.setHtml(markdown(self.text_edit.toPlainText()))
            self.setWindowTitle(self.file_name)

    def save_file(self):
        if self.file_name:
            with open(self.file_name, 'w') as f:
                f.write(self.text_edit.toPlainText())
    
    def render_markdown(self):
        if self.toggle_markdown == False:
            self.toggle_markdown = True
            self.notes_mode = 'Edit'
            self.text_edit.hide()
            self.markdown_viewer.show()
            self.markdown_render_btn.setText(self.notes_mode)
            # self.markdown_viewer.setHtml(markdown(self.text_edit.toPlainText()))
        elif self.toggle_markdown == True:
            self.markdown_viewer.hide()
            self.text_edit.show()
            self.toggle_markdown = False
            self.notes_mode = 'View'
            self.markdown_render_btn.setText(self.notes_mode)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
