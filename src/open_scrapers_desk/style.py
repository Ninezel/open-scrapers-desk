APP_STYLE = """
QMainWindow {
  background: #f4efe6;
}
QWidget {
  color: #13232f;
  font-family: "Segoe UI";
  font-size: 10pt;
}
QTabWidget::pane {
  border: 1px solid #d4c7b5;
  background: #fffdf8;
  border-radius: 12px;
}
QTabBar::tab {
  background: #e6d8c4;
  color: #3d4b57;
  padding: 10px 18px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  margin-right: 6px;
}
QTabBar::tab:selected {
  background: #fffdf8;
  color: #10202a;
}
QGroupBox {
  border: 1px solid #decfb9;
  border-radius: 14px;
  margin-top: 14px;
  padding: 14px;
  background: #fffaf1;
  font-weight: 600;
}
QGroupBox::title {
  subcontrol-origin: margin;
  left: 14px;
  padding: 0 6px;
}
QLineEdit, QComboBox, QSpinBox, QPlainTextEdit, QTextBrowser, QTableWidget, QListWidget {
  background: #fffdf9;
  border: 1px solid #d7c7b1;
  border-radius: 10px;
  padding: 6px;
}
QPushButton {
  background: #1d6b73;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 8px 14px;
  font-weight: 600;
}
QPushButton:hover {
  background: #17575d;
}
QPushButton:disabled {
  background: #8ca9ad;
}
QPushButton#SupportButton {
  background: #b45a2a;
}
QPushButton#SupportButton:hover {
  background: #91461f;
}
QHeaderView::section {
  background: #e9dcc8;
  color: #13232f;
  padding: 6px;
  border: none;
  border-bottom: 1px solid #d0bea7;
}
QTableWidget {
  gridline-color: #eadfce;
}
QLabel#HeroTitle {
  font-size: 22pt;
  font-weight: 700;
  color: #10202a;
}
QLabel#HeroSubtitle {
  color: #52626d;
  font-size: 11pt;
}
QLabel#StatusValue {
  font-size: 11pt;
  font-weight: 700;
  color: #1d6b73;
}
"""
