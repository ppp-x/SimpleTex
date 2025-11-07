from PyQt5.QtGui import QFont
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction,
    QFileDialog, QMessageBox, QStatusBar
)
from PyQt5.QtGui import QKeySequence, QTextCharFormat, QColor, QSyntaxHighlighter
from PyQt5.QtCore import Qt, QRegExp

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, language='plain'):
        super().__init__(parent)
        self.language = language
        self.highlighting_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QFont.Bold)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("darkGreen"))

        if language == 'php':
            keywords = ["<?php", "echo", "if", "else", "while", "for", "function", "return"]
            self.highlighting_rules += [(QRegExp(r"\b" + kw + r"\b"), keyword_format) for kw in keywords]
            self.highlighting_rules.append((QRegExp(r"//[^\n]*"), comment_format))
        elif language == 'bash':
            keywords = ["echo", "if", "then", "fi", "for", "while", "do", "done"]
            self.highlighting_rules += [(QRegExp(r"\b" + kw + r"\b"), keyword_format) for kw in keywords]
            self.highlighting_rules.append((QRegExp(r"#.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)

class TextEditor(QMainWindow):
    def __init__(self, filename=None):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        self.editor = QTextEdit(self)
        self.setCentralWidget(self.editor)
        self.editor.cursorPositionChanged.connect(self.update_cursor_position)
        self.editor.textChanged.connect(self.mark_unsaved)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.current_file = None
        self.unsaved_changes = False
        self.highlighter = None

        self.create_menus()

        if filename:
            self.load_file(filename)

    def create_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.open_file)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_file)

        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        edit_menu = menubar.addMenu("Edit")
        cut_action = QAction("Cut", self)
        cut_action.triggered.connect(self.editor.cut)
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.editor.copy)
        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

    def update_cursor_position(self):
        cursor = self.editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.status.showMessage(f"Line: {line}, Column: {col}")

    def mark_unsaved(self):
        self.unsaved_changes = True

    def load_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.editor.setText(content)
            self.current_file = path
            self.unsaved_changes = False
            self.setWindowTitle(f"{os.path.basename(path)} - SimpleTex Text Editor")
            self.set_highlighter(path)
        except Exception as e:
            self.editor.setText(f"Error opening file: {e}")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if path:
            self.load_file(path)

    def save_file(self):
        if self.current_file:
            path = self.current_file
        else:
            path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*)")
            if not path:
                return
            self.current_file = path

        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            self.unsaved_changes = False
            self.status.showMessage("File saved successfully", 3000)
            self.setWindowTitle(f"{os.path.basename(path)} - SimpleTex Text Editor")
        except Exception as e:
            self.editor.setText(f"Error saving file: {e}")

    def closeEvent(self, event):
        if self.unsaved_changes:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Do you want to save before exiting?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            if reply == QMessageBox.Yes:
                self.save_file()
                event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def set_highlighter(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext == ".php":
            self.highlighter = SyntaxHighlighter(self.editor.document(), language='php')
        elif ext in [".sh", ".bash"]:
            self.highlighter = SyntaxHighlighter(self.editor.document(), language='bash')
        else:
            self.highlighter = None

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    app = QApplication(sys.argv)
    window = TextEditor(filename)
    window.show()
    sys.exit(app.exec_())

