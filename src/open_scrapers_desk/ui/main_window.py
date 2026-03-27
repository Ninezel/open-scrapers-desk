from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QProcess, Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
  QAbstractItemView,
  QComboBox,
  QFileDialog,
  QFormLayout,
  QGridLayout,
  QGroupBox,
  QHBoxLayout,
  QLabel,
  QLineEdit,
  QListWidget,
  QListWidgetItem,
  QMainWindow,
  QMessageBox,
  QPlainTextEdit,
  QPushButton,
  QSplitter,
  QSpinBox,
  QTableWidget,
  QTableWidgetItem,
  QTabWidget,
  QTextBrowser,
  QVBoxLayout,
  QWidget,
)

from ..backend import (
  build_run_all_command,
  build_run_command,
  describe_command,
  list_scrapers,
  validate_backend,
)
from ..models import AppSettings, ResultFileSummary, ResultPayload, ResultRecord, ScraperSummary
from ..results import filter_records, format_meta_html, load_result_payload, scan_result_files
from ..settings import SettingsStore, default_output_dir


class MainWindow(QMainWindow):
  def __init__(self, settings_store: SettingsStore) -> None:
    super().__init__()
    self.settings_store = settings_store
    self.settings = settings_store.load()
    self.scrapers: list[ScraperSummary] = []
    self.result_files: list[ResultFileSummary] = []
    self.current_payload: ResultPayload | None = None
    self.current_process: QProcess | None = None
    self.current_process_label = ""
    self.param_inputs: dict[str, QLineEdit] = {}

    self.setWindowTitle("Open Scrapers Desk")
    self.resize(1480, 920)

    self._build_ui()
    self._apply_settings_to_form()
    self.refresh_backend_status()
    self.refresh_catalog()
    self.refresh_results()

  def _build_ui(self) -> None:
    root = QWidget()
    root_layout = QVBoxLayout(root)
    root_layout.setContentsMargins(22, 18, 22, 18)
    root_layout.setSpacing(14)

    hero_title = QLabel("Open Scrapers Desk")
    hero_title.setObjectName("HeroTitle")
    hero_subtitle = QLabel(
      "Browse collected datasets, run scraper jobs, and keep the toolkit approachable for non-programmers."
    )
    hero_subtitle.setObjectName("HeroSubtitle")
    hero_subtitle.setWordWrap(True)
    root_layout.addWidget(hero_title)
    root_layout.addWidget(hero_subtitle)

    hero_actions = QHBoxLayout()
    hero_actions.addStretch(1)
    self.support_button = QPushButton("Support Ninezel on Ko-fi")
    self.support_button.setObjectName("SupportButton")
    self.support_button.clicked.connect(self.open_kofi_link)
    hero_actions.addWidget(self.support_button)
    root_layout.addLayout(hero_actions)

    self.tabs = QTabWidget()
    self.tabs.addTab(self._build_overview_tab(), "Overview")
    self.tabs.addTab(self._build_run_tab(), "Run Scrapers")
    self.tabs.addTab(self._build_results_tab(), "Results Library")
    self.tabs.addTab(self._build_logs_tab(), "Logs & Help")
    root_layout.addWidget(self.tabs)

    self.setCentralWidget(root)

  def _build_overview_tab(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setSpacing(12)

    config_group = QGroupBox("Toolkit Connection")
    config_layout = QFormLayout(config_group)

    toolkit_row = QHBoxLayout()
    self.toolkit_path_edit = QLineEdit()
    self.toolkit_path_edit.setPlaceholderText("Path to the open-scrapers-toolkit repository")
    toolkit_browse = QPushButton("Browse")
    toolkit_browse.clicked.connect(self._browse_toolkit_path)
    toolkit_row.addWidget(self.toolkit_path_edit)
    toolkit_row.addWidget(toolkit_browse)
    config_layout.addRow("Toolkit path", self._wrap_layout(toolkit_row))

    node_row = QHBoxLayout()
    self.node_exec_edit = QLineEdit()
    self.node_exec_edit.setPlaceholderText("node")
    node_browse = QPushButton("Locate")
    node_browse.clicked.connect(self._browse_node_executable)
    node_row.addWidget(self.node_exec_edit)
    node_row.addWidget(node_browse)
    config_layout.addRow("Node executable", self._wrap_layout(node_row))

    output_row = QHBoxLayout()
    self.output_dir_edit = QLineEdit()
    self.output_dir_edit.setPlaceholderText("Where JSON result files should be stored")
    output_browse = QPushButton("Browse")
    output_browse.clicked.connect(self._browse_output_dir)
    output_row.addWidget(self.output_dir_edit)
    output_row.addWidget(output_browse)
    config_layout.addRow("Output directory", self._wrap_layout(output_row))

    kofi_row = QHBoxLayout()
    self.kofi_url_edit = QLineEdit()
    self.kofi_url_edit.setPlaceholderText("https://ko-fi.com/ninezel")
    self.kofi_url_edit.setToolTip("Set your Ko-fi page URL so the app can open it.")
    self.open_kofi_button = QPushButton("Open Ko-fi")
    self.open_kofi_button.setObjectName("SupportButton")
    self.open_kofi_button.clicked.connect(self.open_kofi_link)
    kofi_row.addWidget(self.kofi_url_edit)
    kofi_row.addWidget(self.open_kofi_button)
    config_layout.addRow("Ko-fi link", self._wrap_layout(kofi_row))

    button_row = QHBoxLayout()
    save_button = QPushButton("Save Settings")
    save_button.clicked.connect(self.save_settings)
    validate_button = QPushButton("Validate Backend")
    validate_button.clicked.connect(self.refresh_backend_status)
    refresh_button = QPushButton("Refresh Everything")
    refresh_button.clicked.connect(self.refresh_everything)
    open_output_button = QPushButton("Open Output Folder")
    open_output_button.clicked.connect(self.open_output_dir)
    button_row.addWidget(save_button)
    button_row.addWidget(validate_button)
    button_row.addWidget(refresh_button)
    button_row.addWidget(open_output_button)
    config_layout.addRow(button_row)

    layout.addWidget(config_group)

    status_group = QGroupBox("Status Snapshot")
    status_layout = QGridLayout(status_group)
    status_layout.setHorizontalSpacing(18)
    status_layout.setVerticalSpacing(10)

    self.toolkit_status_value = self._status_value_label()
    self.node_status_value = self._status_value_label()
    self.cli_mode_value = self._status_value_label()
    self.catalog_count_value = self._status_value_label()
    self.results_count_value = self._status_value_label()
    self.backend_message_value = QLabel("")
    self.backend_message_value.setWordWrap(True)

    rows = [
      ("Toolkit", self.toolkit_status_value),
      ("Node", self.node_status_value),
      ("CLI mode", self.cli_mode_value),
      ("Catalog", self.catalog_count_value),
      ("Result files", self.results_count_value),
      ("Notes", self.backend_message_value),
    ]
    for row_index, (label_text, widget) in enumerate(rows):
      status_layout.addWidget(QLabel(label_text), row_index, 0)
      status_layout.addWidget(widget, row_index, 1)

    layout.addWidget(status_group)

    recent_group = QGroupBox("Latest Result Files")
    recent_layout = QVBoxLayout(recent_group)
    self.recent_results_list = QListWidget()
    self.recent_results_list.itemDoubleClicked.connect(self._open_selected_recent_result)
    recent_layout.addWidget(self.recent_results_list)
    layout.addWidget(recent_group)

    layout.addStretch(1)
    return page

  def _build_run_tab(self) -> QWidget:
    page = QWidget()
    layout = QHBoxLayout(page)
    layout.setSpacing(12)

    left_group = QGroupBox("Scraper Catalog")
    left_layout = QVBoxLayout(left_group)
    filter_row = QHBoxLayout()

    self.scraper_filter_edit = QLineEdit()
    self.scraper_filter_edit.setPlaceholderText("Filter by name, source, or category")
    self.scraper_filter_edit.textChanged.connect(self.populate_scraper_list)
    self.scraper_category_combo = QComboBox()
    self.scraper_category_combo.addItems(["all", "news", "weather", "reports", "academic"])
    self.scraper_category_combo.currentTextChanged.connect(self._on_category_changed)
    filter_row.addWidget(self.scraper_filter_edit)
    filter_row.addWidget(self.scraper_category_combo)
    left_layout.addLayout(filter_row)

    self.scraper_list = QListWidget()
    self.scraper_list.currentItemChanged.connect(self._on_scraper_selected)
    left_layout.addWidget(self.scraper_list)
    layout.addWidget(left_group, 1)

    right_container = QWidget()
    right_layout = QVBoxLayout(right_container)
    right_layout.setSpacing(12)

    detail_group = QGroupBox("Selected Scraper")
    detail_layout = QVBoxLayout(detail_group)
    self.scraper_name_label = QLabel("Choose a scraper")
    self.scraper_name_label.setObjectName("StatusValue")
    self.scraper_description_label = QLabel("Scraper details will appear here.")
    self.scraper_description_label.setWordWrap(True)
    self.scraper_homepage_label = QLabel("")
    self.scraper_homepage_label.setOpenExternalLinks(True)
    detail_layout.addWidget(self.scraper_name_label)
    detail_layout.addWidget(self.scraper_description_label)
    detail_layout.addWidget(self.scraper_homepage_label)

    self.param_group = QGroupBox("Parameters")
    self.param_form = QFormLayout(self.param_group)

    run_group = QGroupBox("Run Controls")
    run_layout = QFormLayout(run_group)
    self.limit_spin = QSpinBox()
    self.limit_spin.setRange(1, 500)
    self.limit_spin.setValue(10)
    run_layout.addRow("Limit", self.limit_spin)

    output_file_row = QHBoxLayout()
    self.output_file_edit = QLineEdit()
    self.output_file_edit.setPlaceholderText("Output JSON file path")
    output_file_browse = QPushButton("Browse")
    output_file_browse.clicked.connect(self._browse_output_file)
    output_file_row.addWidget(self.output_file_edit)
    output_file_row.addWidget(output_file_browse)
    run_layout.addRow("Output file", self._wrap_layout(output_file_row))

    actions_row = QHBoxLayout()
    self.refresh_catalog_button = QPushButton("Refresh Catalog")
    self.refresh_catalog_button.clicked.connect(self.refresh_catalog)
    self.run_selected_button = QPushButton("Run Selected")
    self.run_selected_button.clicked.connect(self.run_selected_scraper)
    self.run_category_button = QPushButton("Run Category")
    self.run_category_button.clicked.connect(self.run_selected_category)
    self.run_all_button = QPushButton("Run All")
    self.run_all_button.clicked.connect(self.run_all_scrapers)
    actions_row.addWidget(self.refresh_catalog_button)
    actions_row.addWidget(self.run_selected_button)
    actions_row.addWidget(self.run_category_button)
    actions_row.addWidget(self.run_all_button)
    run_layout.addRow(actions_row)

    log_group = QGroupBox("Run Log")
    log_layout = QVBoxLayout(log_group)
    self.run_log = QPlainTextEdit()
    self.run_log.setReadOnly(True)
    log_layout.addWidget(self.run_log)

    right_layout.addWidget(detail_group)
    right_layout.addWidget(self.param_group)
    right_layout.addWidget(run_group)
    right_layout.addWidget(log_group, 1)
    layout.addWidget(right_container, 2)

    return page

  def _build_results_tab(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setSpacing(12)

    top_row = QHBoxLayout()
    self.result_search_edit = QLineEdit()
    self.result_search_edit.setPlaceholderText("Filter current records by title, summary, author, or tags")
    self.result_search_edit.textChanged.connect(self._refresh_record_table)
    refresh_button = QPushButton("Refresh Library")
    refresh_button.clicked.connect(self.refresh_results)
    open_button = QPushButton("Open Output Folder")
    open_button.clicked.connect(self.open_output_dir)
    load_button = QPushButton("Open JSON File")
    load_button.clicked.connect(self.open_result_file_dialog)
    top_row.addWidget(self.result_search_edit, 1)
    top_row.addWidget(refresh_button)
    top_row.addWidget(open_button)
    top_row.addWidget(load_button)
    layout.addLayout(top_row)

    splitter = QSplitter(Qt.Orientation.Horizontal)

    file_group = QGroupBox("Result Files")
    file_layout = QVBoxLayout(file_group)
    self.result_files_table = QTableWidget(0, 5)
    self.result_files_table.setHorizontalHeaderLabels(
      ["Scraper", "Category", "Source", "Records", "Fetched"]
    )
    self.result_files_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    self.result_files_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.result_files_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    self.result_files_table.verticalHeader().setVisible(False)
    self.result_files_table.itemSelectionChanged.connect(self._on_result_file_selected)
    file_layout.addWidget(self.result_files_table)
    splitter.addWidget(file_group)

    details_splitter = QSplitter(Qt.Orientation.Vertical)

    records_group = QGroupBox("Records")
    records_layout = QVBoxLayout(records_group)
    self.result_meta_label = QLabel("Select a result file to inspect its records.")
    self.result_meta_label.setWordWrap(True)
    self.record_table = QTableWidget(0, 4)
    self.record_table.setHorizontalHeaderLabels(["Title", "Published", "Source", "Location"])
    self.record_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    self.record_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.record_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    self.record_table.verticalHeader().setVisible(False)
    self.record_table.itemSelectionChanged.connect(self._on_record_selected)
    records_layout.addWidget(self.result_meta_label)
    records_layout.addWidget(self.record_table)
    details_splitter.addWidget(records_group)

    detail_group = QGroupBox("Record Detail")
    detail_layout = QVBoxLayout(detail_group)
    self.record_detail_browser = QTextBrowser()
    detail_layout.addWidget(self.record_detail_browser)
    details_splitter.addWidget(detail_group)

    splitter.addWidget(details_splitter)
    splitter.setSizes([520, 860])

    layout.addWidget(splitter, 1)
    return page

  def _build_logs_tab(self) -> QWidget:
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setSpacing(12)

    help_group = QGroupBox("Quick Start")
    help_layout = QVBoxLayout(help_group)
    help_browser = QTextBrowser()
    help_browser.setOpenExternalLinks(True)
    help_browser.setHtml(
      """
      <h2>Open Scrapers Desk</h2>
      <p>This desktop app connects to the <b>Open Scrapers Toolkit</b> repository and gives people a GUI for:</p>
      <ul>
        <li>browsing structured JSON results</li>
        <li>running single scrapers, whole categories, or the full catalog</li>
        <li>opening output folders and reviewing record metadata</li>
      </ul>
      <p><b>Backend checklist</b></p>
      <ol>
        <li>Clone the toolkit repository.</li>
        <li>Run <code>npm install</code> and <code>npm run build</code> in that repo.</li>
        <li>Point this app at the toolkit folder.</li>
      </ol>
      <p>The app includes a built-in Ko-fi support button and defaults it to Ninezel's Ko-fi page.</p>
      <p>Need the docs? Open the project README and wiki after publishing this repo to GitHub.</p>
      """
    )
    help_layout.addWidget(help_browser)
    support_row = QHBoxLayout()
    support_row.addStretch(1)
    self.help_support_button = QPushButton("Open Ninezel's Ko-fi")
    self.help_support_button.setObjectName("SupportButton")
    self.help_support_button.clicked.connect(self.open_kofi_link)
    support_row.addWidget(self.help_support_button)
    help_layout.addLayout(support_row)
    layout.addWidget(help_group)

    activity_group = QGroupBox("Activity Log")
    activity_layout = QVBoxLayout(activity_group)
    self.activity_log = QPlainTextEdit()
    self.activity_log.setReadOnly(True)
    activity_layout.addWidget(self.activity_log)
    layout.addWidget(activity_group, 1)

    return page

  @staticmethod
  def _wrap_layout(layout) -> QWidget:
    widget = QWidget()
    widget.setLayout(layout)
    return widget

  @staticmethod
  def _status_value_label() -> QLabel:
    label = QLabel("")
    label.setObjectName("StatusValue")
    return label

  def _apply_settings_to_form(self) -> None:
    self.toolkit_path_edit.setText(self.settings.toolkit_path)
    self.node_exec_edit.setText(self.settings.node_executable)
    self.output_dir_edit.setText(self.settings.output_dir)
    self.kofi_url_edit.setText(self.settings.kofi_url)
    self.scraper_category_combo.setCurrentText(self.settings.last_category or "all")
    self._refresh_support_button_state()

  def current_settings(self) -> AppSettings:
    toolkit_path = self.toolkit_path_edit.text().strip()
    output_dir = self.output_dir_edit.text().strip() or default_output_dir(toolkit_path)
    return AppSettings(
      toolkit_path=toolkit_path,
      node_executable=self.node_exec_edit.text().strip() or "node",
      output_dir=output_dir,
      kofi_url=self.kofi_url_edit.text().strip(),
      last_scraper_id=self.settings.last_scraper_id,
      last_category=self.scraper_category_combo.currentText(),
    )

  def save_settings(self) -> None:
    self.settings = self.current_settings()
    self.settings_store.save(self.settings)
    self.log_activity("Settings saved.")
    self.output_dir_edit.setText(self.settings.output_dir)
    self.kofi_url_edit.setText(self.settings.kofi_url)
    self._refresh_support_button_state()

  def refresh_everything(self) -> None:
    self.save_settings()
    self.refresh_backend_status()
    self.refresh_catalog()
    self.refresh_results()

  def refresh_backend_status(self) -> None:
    self.save_settings()
    status = validate_backend(self.settings.toolkit_path, self.settings.node_executable)
    self.toolkit_status_value.setText("Ready" if status.toolkit_ok else "Missing")
    self.node_status_value.setText(status.node_version if status.node_ok else "Unavailable")
    self.cli_mode_value.setText(status.cli_mode)
    self.backend_message_value.setText(status.message)
    self.log_activity(status.message)

  def refresh_catalog(self) -> None:
    self.save_settings()
    try:
      self.scrapers = list_scrapers(self.settings.toolkit_path, self.settings.node_executable)
      self.catalog_count_value.setText(str(len(self.scrapers)))
      self.populate_scraper_list()
      self.log_activity(f"Loaded {len(self.scrapers)} scrapers from the toolkit.")
    except Exception as error:  # noqa: BLE001
      self.scrapers = []
      self.catalog_count_value.setText("0")
      self.scraper_list.clear()
      self.log_activity(f"Could not load scraper catalog: {error}")
      QMessageBox.warning(self, "Catalog Load Failed", str(error))

  def populate_scraper_list(self) -> None:
    self.scraper_list.clear()
    filter_text = self.scraper_filter_edit.text().strip().lower()
    selected_category = self.scraper_category_combo.currentText()

    for scraper in self.scrapers:
      haystack = " ".join(
        [scraper.id, scraper.name, scraper.category, scraper.description]
      ).lower()
      if filter_text and filter_text not in haystack:
        continue
      if selected_category != "all" and scraper.category != selected_category:
        continue

      item = QListWidgetItem(f"{scraper.name} [{scraper.category}]")
      item.setData(Qt.ItemDataRole.UserRole, scraper.id)
      self.scraper_list.addItem(item)

      if scraper.id == self.settings.last_scraper_id:
        self.scraper_list.setCurrentItem(item)

    if self.scraper_list.count() > 0 and self.scraper_list.currentRow() == -1:
      self.scraper_list.setCurrentRow(0)

  def refresh_results(self) -> None:
    self.save_settings()
    self.result_files = scan_result_files(self.settings.output_dir)
    self.results_count_value.setText(str(len(self.result_files)))
    self.recent_results_list.clear()

    self.result_files_table.setRowCount(len(self.result_files))
    for row_index, summary in enumerate(self.result_files):
      values = [
        summary.scraper_name,
        summary.category,
        summary.source,
        str(summary.record_count),
        summary.fetched_at,
      ]
      for column_index, value in enumerate(values):
        item = QTableWidgetItem(value)
        item.setData(Qt.ItemDataRole.UserRole, str(summary.path))
        self.result_files_table.setItem(row_index, column_index, item)

      self.recent_results_list.addItem(f"{summary.scraper_name} - {summary.path.name}")

    if self.result_files:
      self.result_files_table.selectRow(0)
    else:
      self.record_table.setRowCount(0)
      self.record_detail_browser.setHtml("<i>No result files found yet.</i>")
      self.result_meta_label.setText("No result files found.")

    self.log_activity(f"Found {len(self.result_files)} result files.")

  def _on_category_changed(self, value: str) -> None:
    self.settings.last_category = value
    self.populate_scraper_list()

  def _selected_scraper(self) -> ScraperSummary | None:
    item = self.scraper_list.currentItem()
    if item is None:
      return None
    scraper_id = item.data(Qt.ItemDataRole.UserRole)
    return next((scraper for scraper in self.scrapers if scraper.id == scraper_id), None)

  def _on_scraper_selected(self, *_args) -> None:
    scraper = self._selected_scraper()
    if scraper is None:
      return

    self.settings.last_scraper_id = scraper.id
    self.scraper_name_label.setText(f"{scraper.name} [{scraper.category}]")
    self.scraper_description_label.setText(scraper.description)
    self.scraper_homepage_label.setText(
      f"<a href='{scraper.homepage}'>{scraper.homepage}</a>"
    )

    while self.param_form.rowCount():
      self.param_form.removeRow(0)
    self.param_inputs = {}

    if scraper.params:
      for parameter in scraper.params:
        field = QLineEdit()
        if parameter.example:
          field.setPlaceholderText(parameter.example)
        field.setToolTip(parameter.description)
        self.param_form.addRow(f"{parameter.key}", field)
        self.param_inputs[parameter.key] = field
    else:
      placeholder = QLabel("This scraper does not require extra parameters.")
      self.param_form.addRow(placeholder)

    default_output = Path(self.output_dir_edit.text() or self.settings.output_dir) / f"{scraper.id}.json"
    self.output_file_edit.setText(str(default_output))

  def run_selected_scraper(self) -> None:
    scraper = self._selected_scraper()
    if scraper is None:
      QMessageBox.information(self, "No Scraper Selected", "Choose a scraper first.")
      return

    params = {key: widget.text().strip() for key, widget in self.param_inputs.items()}
    output_path = self.output_file_edit.text().strip()
    if not output_path:
      QMessageBox.warning(self, "Output Path Required", "Choose an output JSON file path.")
      return

    try:
      program, args, working_dir = build_run_command(
        self.settings.toolkit_path,
        self.settings.node_executable,
        scraper.id,
        self.limit_spin.value(),
        output_path,
        params,
      )
    except Exception as error:  # noqa: BLE001
      QMessageBox.warning(self, "Run Failed", str(error))
      return

    self._start_process("run", program, args, working_dir)

  def run_selected_category(self) -> None:
    category = self.scraper_category_combo.currentText()
    if category == "all":
      QMessageBox.information(
        self,
        "Choose a Category",
        "Select a specific category first, or use Run All.",
      )
      return

    self._run_all_like(mode_label=f"run-all:{category}", category=category)

  def run_all_scrapers(self) -> None:
    self._run_all_like(mode_label="run-all", category="")

  def _run_all_like(self, mode_label: str, category: str) -> None:
    output_dir = self.output_dir_edit.text().strip() or self.settings.output_dir
    try:
      program, args, working_dir = build_run_all_command(
        self.settings.toolkit_path,
        self.settings.node_executable,
        self.limit_spin.value(),
        output_dir,
        category,
      )
    except Exception as error:  # noqa: BLE001
      QMessageBox.warning(self, "Run Failed", str(error))
      return

    self._start_process(mode_label, program, args, working_dir)

  def _start_process(
    self,
    label: str,
    program: str,
    args: list[str],
    working_dir: str,
  ) -> None:
    if self.current_process is not None and self.current_process.state() != QProcess.ProcessState.NotRunning:
      QMessageBox.information(self, "Process Running", "Wait for the current job to finish first.")
      return

    self.current_process_label = label
    process = QProcess(self)
    process.setWorkingDirectory(working_dir)
    process.setProgram(program)
    process.setArguments(args)
    process.readyReadStandardOutput.connect(self._consume_process_stdout)
    process.readyReadStandardError.connect(self._consume_process_stderr)
    process.finished.connect(self._finish_process)
    self.current_process = process

    command = describe_command(program, args)
    self.run_log.appendPlainText(f"$ {command}")
    self.log_activity(f"Started {label}: {command}")
    self._set_run_buttons_enabled(False)
    process.start()

  def _consume_process_stdout(self) -> None:
    if self.current_process is None:
      return
    text = bytes(self.current_process.readAllStandardOutput()).decode("utf-8", errors="replace")
    if text.strip():
      self.run_log.appendPlainText(text.rstrip())

  def _consume_process_stderr(self) -> None:
    if self.current_process is None:
      return
    text = bytes(self.current_process.readAllStandardError()).decode("utf-8", errors="replace")
    if text.strip():
      self.run_log.appendPlainText(text.rstrip())

  def _finish_process(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
    self._set_run_buttons_enabled(True)
    if exit_status == QProcess.ExitStatus.NormalExit and exit_code == 0:
      self.run_log.appendPlainText(f"{self.current_process_label} finished successfully.")
      self.log_activity(f"{self.current_process_label} finished successfully.")
      self.refresh_results()
    else:
      self.run_log.appendPlainText(
        f"{self.current_process_label} failed with exit code {exit_code}."
      )
      self.log_activity(f"{self.current_process_label} failed with exit code {exit_code}.")

  def _set_run_buttons_enabled(self, enabled: bool) -> None:
    self.run_selected_button.setEnabled(enabled)
    self.run_category_button.setEnabled(enabled)
    self.run_all_button.setEnabled(enabled)
    self.refresh_catalog_button.setEnabled(enabled)

  def _on_result_file_selected(self) -> None:
    selected_items = self.result_files_table.selectedItems()
    if not selected_items:
      return

    path = selected_items[0].data(Qt.ItemDataRole.UserRole)
    try:
      self.current_payload = load_result_payload(path)
      self.result_meta_label.setText(
        f"{self.current_payload.scraper_name} | {self.current_payload.category} | "
        f"{len(self.current_payload.records)} records | fetched {self.current_payload.fetched_at}"
      )
      self.record_detail_browser.setHtml(format_meta_html(self.current_payload.meta))
      self._refresh_record_table()
    except Exception as error:  # noqa: BLE001
      self.log_activity(f"Could not load result file {path}: {error}")
      QMessageBox.warning(self, "Result Load Failed", str(error))

  def _refresh_record_table(self) -> None:
    if self.current_payload is None:
      self.record_table.setRowCount(0)
      return

    records = filter_records(self.current_payload.records, self.result_search_edit.text())
    self.record_table.setRowCount(len(records))
    for row_index, record in enumerate(records):
      values = [record.title, record.published_at, record.source, record.location]
      for column_index, value in enumerate(values):
        item = QTableWidgetItem(value)
        item.setData(Qt.ItemDataRole.UserRole, record.id)
        self.record_table.setItem(row_index, column_index, item)

    if records:
      self.record_table.selectRow(0)
    else:
      self.record_detail_browser.setHtml("<i>No records match the current filter.</i>")

  def _on_record_selected(self) -> None:
    if self.current_payload is None:
      return

    selected_items = self.record_table.selectedItems()
    if not selected_items:
      return

    record_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
    record = next((item for item in self.current_payload.records if item.id == record_id), None)
    if record is None:
      return

    self.record_detail_browser.setHtml(self._record_html(record))

  def _record_html(self, record: ResultRecord) -> str:
    tags = ", ".join(record.tags) if record.tags else "None"
    authors = ", ".join(record.authors) if record.authors else "Unknown"
    meta_html = format_meta_html(record.metadata)
    link_html = (
      f"<p><a href='{record.url}'>{record.url}</a></p>"
      if record.url
      else "<p><i>No link available.</i></p>"
    )
    return f"""
    <h2>{record.title}</h2>
    <p><b>Source:</b> {record.source}<br>
    <b>Published:</b> {record.published_at or 'Unknown'}<br>
    <b>Location:</b> {record.location or 'Unknown'}<br>
    <b>Authors:</b> {authors}<br>
    <b>Tags:</b> {tags}</p>
    <p>{record.summary or '<i>No summary provided.</i>'}</p>
    {link_html}
    <h3>Metadata</h3>
    {meta_html}
    """

  def open_result_file_dialog(self) -> None:
    file_path, _ = QFileDialog.getOpenFileName(
      self,
      "Open Result JSON",
      self.settings.output_dir,
      "JSON Files (*.json)",
    )
    if not file_path:
      return

    try:
      self.current_payload = load_result_payload(file_path)
      self.result_meta_label.setText(
        f"{self.current_payload.scraper_name} | {len(self.current_payload.records)} records | {file_path}"
      )
      self.record_detail_browser.setHtml(format_meta_html(self.current_payload.meta))
      self._refresh_record_table()
      self.tabs.setCurrentIndex(2)
      self.log_activity(f"Opened external result file {file_path}.")
    except Exception as error:  # noqa: BLE001
      QMessageBox.warning(self, "Open Failed", str(error))

  def open_output_dir(self) -> None:
    output_dir = Path(self.output_dir_edit.text().strip() or self.settings.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    QDesktopServices.openUrl(QUrl.fromLocalFile(str(output_dir)))

  def open_kofi_link(self) -> None:
    self.save_settings()
    if not self.settings.kofi_url:
      QMessageBox.information(
        self,
        "Ko-fi Link Missing",
        "Add your Ko-fi URL on the Overview tab first, then the support button will open it.",
      )
      return

    opened = QDesktopServices.openUrl(QUrl(self.settings.kofi_url))
    if opened:
      self.log_activity(f"Opened Ko-fi link: {self.settings.kofi_url}")
    else:
      QMessageBox.warning(
        self,
        "Could Not Open Link",
        f"The app could not open this Ko-fi URL:\n{self.settings.kofi_url}",
      )

  def _refresh_support_button_state(self) -> None:
    has_link = bool(self.settings.kofi_url)
    self.support_button.setEnabled(has_link)
    self.open_kofi_button.setEnabled(has_link)
    self.help_support_button.setEnabled(has_link)
    if has_link:
      self.support_button.setToolTip(self.settings.kofi_url)
      self.open_kofi_button.setToolTip(self.settings.kofi_url)
      self.help_support_button.setToolTip(self.settings.kofi_url)
    else:
      self.support_button.setToolTip("Add your Ko-fi URL on the Overview tab.")
      self.open_kofi_button.setToolTip("Add your Ko-fi URL on the Overview tab.")
      self.help_support_button.setToolTip("Add your Ko-fi URL on the Overview tab.")

  def _browse_toolkit_path(self) -> None:
    path = QFileDialog.getExistingDirectory(self, "Choose Toolkit Repository", self.toolkit_path_edit.text())
    if path:
      self.toolkit_path_edit.setText(path)
      if not self.output_dir_edit.text().strip():
        self.output_dir_edit.setText(str(Path(path) / "output"))

  def _browse_node_executable(self) -> None:
    path, _ = QFileDialog.getOpenFileName(self, "Choose Node Executable", self.node_exec_edit.text())
    if path:
      self.node_exec_edit.setText(path)

  def _browse_output_dir(self) -> None:
    path = QFileDialog.getExistingDirectory(self, "Choose Output Directory", self.output_dir_edit.text())
    if path:
      self.output_dir_edit.setText(path)

  def _browse_output_file(self) -> None:
    path, _ = QFileDialog.getSaveFileName(
      self,
      "Choose Output File",
      self.output_file_edit.text(),
      "JSON Files (*.json)",
    )
    if path:
      self.output_file_edit.setText(path)

  def _open_selected_recent_result(self, *_args) -> None:
    current_item = self.recent_results_list.currentItem()
    if current_item is None:
      return
    selected_text = current_item.text()
    matched = next(
      (summary for summary in self.result_files if summary.path.name in selected_text),
      None,
    )
    if matched is None:
      return

    self.tabs.setCurrentIndex(2)
    for row_index, summary in enumerate(self.result_files):
      if summary.path == matched.path:
        self.result_files_table.selectRow(row_index)
        break

  def log_activity(self, message: str) -> None:
    if message.strip():
      self.activity_log.appendPlainText(message)
