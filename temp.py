import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextBrowser
import markdown

class MarkdownViewer(QWidget):
    def __init__(self, markdown_text):
        super().__init__()
        self.setWindowTitle("Markdown Viewer")
        self.resize(800, 600)
        
        # Convert Markdown to HTML using markdown2
        html_content = markdown.markdown(markdown_text)
        
        # Set up the QTextBrowser to display HTML content
        self.text_browser = QTextBrowser()
        self.text_browser.setHtml(html_content)
        
        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_browser)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Sample Markdown text
    markdown_text = "# Sample Markdown <br> This is a sample markdown document. <br> ![Sample Image](https://www.example.com/image.jpg) <br> [Example Link](https://www.example.com)"
    
    viewer = MarkdownViewer(markdown_text)
    viewer.show()
    
    sys.exit(app.exec())
