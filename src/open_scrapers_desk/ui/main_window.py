from __future__ import annotations

from dataclasses import dataclass
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
  QInputDialog,
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
  fetch_health_summary,
  list_scrapers,
  validate_backend,
)
from ..models import (
  AppSettings,
  ResultFileSummary,
  ResultPayload,
  ResultRecord,
  ScraperParameter,
  ScraperSummary,
  SourceHealthRecord,
  WorkspaceProfile,
)
from ..results import (
  build_library_summary_html,
  build_payload_summary_html,
  filter_records,
  format_meta_html,
  load_result_payload,
  scan_result_files,
)
from ..settings import SettingsStore, default_output_dir


@dataclass(slots=True)
class QueuedJob:
  args: list[str]
  label: str
  program: str
  working_dir: str


class MainWindow(QMainWindow):
  def __init__(self, settings_store: SettingsStore) -> None:
    super().__init__()
    self.settings_store = settings_store
    self.settings = settings_store.load()
    self.scrapers: list[ScraperSummary] = []
    self.result_files: list[ResultFileSummary] = []
    self.health_records: list[SourceHealthRecord] = []
    self.current_payload: ResultPayload | None = None
    self.current_process: QProcess | None = None
    self.current_process_label = ""
    self.pending_jobs: list[QueuedJob] = []
    self.param_inputs: dict[str, QLineEdit] = {}

    self.setWindowTitle("Open Scrapers Desk")
    self.resize(1540, 960)

    self._build_ui()
    self._refresh_workspace_combo()
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
      "Browse collected datasets, queue scraper jobs, inspect source health, and keep the toolkit approachable for non-programmers."
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

    workspace_group = QGroupBox("Saved Workspaces")
    workspace_layout = QFormLayout(workspace_group)
    workspace_row = QHBoxLayout()
    self.workspace_combo = QComboBox()
    self.workspace_combo.currentTextChanged.connect(self._on_workspace_changed)
    save_workspace_button = QPushButton("Save Workspace")
    save_workspace_button.clicked.connect(self.save_workspace)
    load_workspace_button = QPushButton("Load Workspace")
    load_workspace_button.clicked.connect(self.load_selected_workspace)
    delete_workspace_button = QPushButton("Delete Workspace")
    delete_workspace_button.clicked.connect(self.delete_selected_workspace)
    workspace_row.addWidget(self.workspace_combo, 1)
    workspace_row.addWidget(save_workspace_button)
    workspace_row.addWidget(load_workspace_button)
    workspace_row.addWidget(delete_workspace_button)
    workspace_layout.addRow("Workspace", self._wrap_layout(workspace_row))
    layout.addWidget(workspace_group)

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
    self.output_dir_edit.setPlaceholderText("Where result files should be stored")
    output_browse = QPushButton("Browse")
    output_browse.clicked.connect(self._browse_output_dir)
    output_row.addWidget(self.output_dir_edit)
    output_row.addWidget(output_browse)
    config_layout.addRow("Output directory", self._wrap_layout(output_row))

    self.default_save_format_combo = QComboBox()
    self.default_save_format_combo.addItems(["json", "csv", "ndjson", "all"])
    config_layout.addRow("Default save format", self.default_save_format_combo)

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
    health_button = QPushButton("Refresh Source Health")
    health_button.clicked.connect(self.refresh_health_summary)
    refresh_button = QPushButton("Refresh Everything")
    refresh_button.clicked.connect(self.refresh_everything)
    open_output_button = QPushButton("Open Output Folder")
    open_output_button.clicked.connect(self.open_output_dir)
    button_row.addWidget(save_button)
    button_row.addWidget(validate_button)
    button_row.addWidget(health_button)
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
    self.health_count_value = self._status_value_label()
    self.backend_message_value = QLabel("")
    self.backend_message_value.setWordWrap(True)

    rows = [
      ("Toolkit", self.toolkit_status_value),
      ("Node", self.node_status_value),
      ("CLI mode", self.cli_mode_value),
      ("Catalog", self.catalog_count_value),
      ("Result files", self.results_count_value),
      ("Health rows", self.health_count_value),
      ("Notes", self.backend_message_value),
    ]
    for row_index, (label_text, widget) in enumerate(rows):
      status_layout.addWidget(QLabel(label_text), row_index, 0)
      status_layout.addWidget(widget, row_index, 1)

    layout.addWidget(status_group)

    health_group = QGroupBox("Source Health Snapshot")
    health_layout = QVBoxLayout(health_group)
    self.health_table = QTableWidget(0, 4)
    self.health_table.setHorizontalHeaderLabels(["Source", "Status", "Category", "Notes"])
    self.health_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    self.health_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.health_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    self.health_table.verticalHeader().setVisible(False)
    health_layout.addWidget(self.health_table)
    layout.addWidget(health_group)

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
    self.scraper_source_label = QLabel("")
    self.scraper_homepage_label = QLabel("")
    self.scraper_homepage_label.setOpenExternalLinks(True)
    detail_layout.addWidget(self.scraper_name_label)
    detail_layout.addWidget(self.scraper_description_label)
    detail_layout.addWidget(self.scraper_source_label)
    detail_layout.addWidget(self.scraper_homepage_label)

    self.param_group = QGroupBox("Parameters")
    self.param_form = QFormLayout(self.param_group)

    run_group = QGroupBox("Run Controls")
    run_layout = QFormLayout(run_group)
    self.limit_spin = QSpinBox()
    self.limit_spin.setRange(1, 500)
    self.limit_spin.setValue(10)
    run_layout.addRow("Limit", self.limit_spin)

    self.run_save_format_combo = QComboBox()
    self.run_save_format_combo.addItems(["json", "csv", "ndjson", "all"])
    run_layout.addRow("Save format", self.run_save_format_combo)

    output_file_row = QHBoxLayout()
    self.output_file_edit = QLineEdit()
    self.output_file_edit.setPlaceholderText("Output base file path")
    output_file_browse = QPushButton("Browse")
    output_file_browse.clicked.connect(self._browse_output_file)
    output_file_row.addWidget(self.output_file_edit)
    output_file_row.addWidget(output_file_browse)
    run_layout.addRow("Output file", self._wrap_layout(output_file_row))

    actions_row = QHBoxLayout()
    self.refresh_catalog_button = QPushButton("Refresh Catalog")
    self.refresh_catalog_button.clicked.connect(self.refresh_catalog)
    self.run_selected_button = QPushButton("Queue Selected")
    self.run_selected_button.clicked.connect(self.run_selected_scraper)
    self.run_category_button = QPushButton("Queue Category")
    self.run_category_button.clicked.connect(self.run_selected_category)
    self.run_all_button = QPushButton("Queue All")
    self.run_all_button.clicked.connect(self.run_all_scrapers)
    actions_row.addWidget(self.refresh_catalog_button)
    actions_row.addWidget(self.run_selected_button)
    actions_row.addWidget(self.run_category_button)
    actions_row.addWidget(self.run_all_button)
    run_layout.addRow(actions_row)

    queue_group = QGroupBox("Pending Job Queue")
    queue_layout = QVBoxLayout(queue_group)
    self.queue_list = QListWidget()
    queue_layout.addWidget(self.queue_list)
    queue_actions = QHBoxLayout()
    remove_queue_button = QPushButton("Remove Selected")
    remove_queue_button.clicked.connect(self.remove_selected_queue_job)
    clear_queue_button = QPushButton("Clear Queue")
    clear_queue_button.clicked.connect(self.clear_job_queue)
    queue_actions.addWidget(remove_queue_button)
    queue_actions.addWidget(clear_queue_button)
    queue_layout.addLayout(queue_actions)

    log_group = QGroupBox("Run Log")
    log_layout = QVBoxLayout(log_group)
    self.run_log = QPlainTextEdit()
    self.run_log.setReadOnly(True)
    log_layout.addWidget(self.run_log)

    right_layout.addWidget(detail_group)
    right_layout.addWidget(self.param_group)
    right_layout.addWidget(run_group)
    right_layout.addWidget(queue_group)
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

    library_group = QGroupBox("Library Snapshot")
    library_layout = QVBoxLayout(library_group)
    self.library_summary_browser = QTextBrowser()
    self.library_summary_browser.setMaximumHeight(220)
    library_layout.addWidget(self.library_summary_browser)
    layout.addWidget(library_group)

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
    self.payload_summary_browser = QTextBrowser()
    self.payload_summary_browser.setMaximumHeight(220)
    self.record_table = QTableWidget(0, 4)
    self.record_table.setHorizontalHeaderLabels(["Title", "Published", "Source", "Location"])
    self.record_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    self.record_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    self.record_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    self.record_table.verticalHeader().setVisible(False)
    self.record_table.itemSelectionChanged.connect(self._on_record_selected)
    records_layout.addWidget(self.result_meta_label)
    records_layout.addWidget(self.payload_summary_browser)
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
        <li>queueing scraper jobs instead of waiting for one run at a time</li>
        <li>checking source-health status before a big batch</li>
        <li>browsing structured JSON results and summary views</li>
        <li>running single scrapers, whole categories, or the full catalog</li>
        <li>using file-based website link scraping through the toolkit's bulk-link mode</li>
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

  def _refresh_workspace_combo(self, selected_name: str | None = None) -> None:
    selected = selected_name if selected_name is not None else self.settings.active_workspace
    self.workspace_combo.blockSignals(True)
    self.workspace_combo.clear()
    self.workspace_combo.addItem("Current Session")
    for workspace in sorted(self.settings.workspaces, key=lambda item: item.name.lower()):
      self.workspace_combo.addItem(workspace.name)
    if selected:
      index = self.workspace_combo.findText(selected)
      self.workspace_combo.setCurrentIndex(index if index >= 0 else 0)
    else:
      self.workspace_combo.setCurrentIndex(0)
    self.workspace_combo.blockSignals(False)

  def _apply_settings_to_form(self) -> None:
    self.toolkit_path_edit.setText(self.settings.toolkit_path)
    self.node_exec_edit.setText(self.settings.node_executable)
    self.output_dir_edit.setText(self.settings.output_dir)
    self.kofi_url_edit.setText(self.settings.kofi_url)
    self.default_save_format_combo.setCurrentText(self.settings.save_format or "json")
    self.run_save_format_combo.setCurrentText(self.settings.save_format or "json")
    self.scraper_category_combo.setCurrentText(self.settings.last_category or "all")
    self._refresh_support_button_state()

  def current_settings(self) -> AppSettings:
    toolkit_path = self.toolkit_path_edit.text().strip()
    output_dir = self.output_dir_edit.text().strip() or default_output_dir(toolkit_path)
    active_workspace = self.workspace_combo.currentText()
    return AppSettings(
      toolkit_path=toolkit_path,
      node_executable=self.node_exec_edit.text().strip() or "node",
      output_dir=output_dir,
      kofi_url=self.kofi_url_edit.text().strip(),
      save_format=self.default_save_format_combo.currentText(),
      last_scraper_id=self.settings.last_scraper_id,
      last_category=self.scraper_category_combo.currentText(),
      active_workspace="" if active_workspace == "Current Session" else active_workspace,
      workspaces=list(self.settings.workspaces),
    )

  def save_settings(self) -> None:
    updated = self.current_settings()

    if updated.active_workspace:
      replacement = WorkspaceProfile(
        name=updated.active_workspace,
        toolkit_path=updated.toolkit_path,
        node_executable=updated.node_executable,
        output_dir=updated.output_dir,
        save_format=updated.save_format,
      )
      updated.workspaces = [
        replacement if workspace.name == updated.active_workspace else workspace
        for workspace in updated.workspaces
      ]

    self.settings = updated
    self.settings_store.save(self.settings)
    self.output_dir_edit.setText(self.settings.output_dir)
    self.kofi_url_edit.setText(self.settings.kofi_url)
    self.run_save_format_combo.setCurrentText(self.settings.save_format)
    self._refresh_support_button_state()
    self._refresh_workspace_combo()
    self.log_activity("Settings saved.")

  def refresh_everything(self) -> None:
    self.save_settings()
    self.refresh_backend_status()
    self.refresh_catalog()
    self.refresh_results()
    self.refresh_health_summary()

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

  def refresh_health_summary(self) -> None:
    self.save_settings()
    try:
      self.health_records = fetch_health_summary(
        self.settings.toolkit_path,
        self.settings.node_executable,
      )
    except Exception as error:  # noqa: BLE001
      self.health_records = []
      self.health_table.setRowCount(0)
      self.health_count_value.setText("0")
      self.log_activity(f"Could not load source health summary: {error}")
      return

    self.health_count_value.setText(str(len(self.health_records)))
    self.health_table.setRowCount(len(self.health_records))
    for row_index, record in enumerate(self.health_records):
      values = [record.source, record.status, record.category, record.summary]
      for column_index, value in enumerate(values):
        self.health_table.setItem(row_index, column_index, QTableWidgetItem(value))

    self.log_activity(f"Loaded {len(self.health_records)} source-health rows.")

  def populate_scraper_list(self) -> None:
    self.scraper_list.clear()
    filter_text = self.scraper_filter_edit.text().strip().lower()
    selected_category = self.scraper_category_combo.currentText()

    for scraper in self.scrapers:
      haystack = " ".join(
        [
          scraper.id,
          scraper.name,
          scraper.category,
          scraper.description,
          scraper.source_name,
        ]
      ).lower()
      if filter_text and filter_text not in haystack:
        continue
      if selected_category != "all" and scraper.category != selected_category:
        continue

      suffix = f" - {scraper.source_name}" if scraper.source_name else ""
      item = QListWidgetItem(f"{scraper.name} [{scraper.category}]{suffix}")
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
    self.library_summary_browser.setHtml(build_library_summary_html(self.result_files))

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
      self.payload_summary_browser.setHtml("<i>No payload selected yet.</i>")
      self.record_detail_browser.setHtml("<i>No result files found yet.</i>")
      self.result_meta_label.setText("No result files found.")

    self.log_activity(f"Found {len(self.result_files)} result files.")

  def _on_workspace_changed(self, value: str) -> None:
    self.settings.active_workspace = "" if value == "Current Session" else value

  def _on_category_changed(self, value: str) -> None:
    self.settings.last_category = value
    self.populate_scraper_list()

  def _selected_scraper(self) -> ScraperSummary | None:
    item = self.scraper_list.currentItem()
    if item is None:
      return None
    scraper_id = item.data(Qt.ItemDataRole.UserRole)
    return next((scraper for scraper in self.scrapers if scraper.id == scraper_id), None)

  def _build_parameter_widget(self, parameter: ScraperParameter) -> tuple[QWidget | QLineEdit, QLineEdit]:
    field = QLineEdit()
    if parameter.example:
      field.setPlaceholderText(parameter.example)
    field.setToolTip(parameter.description)

    if "file" in parameter.key.lower():
      row = QHBoxLayout()
      browse_button = QPushButton("Browse")
      browse_button.clicked.connect(lambda: self._browse_param_file(field))
      row.addWidget(field)
      row.addWidget(browse_button)
      return self._wrap_layout(row), field

    return field, field

  def _on_scraper_selected(self, *_args) -> None:
    scraper = self._selected_scraper()
    if scraper is None:
      return

    self.settings.last_scraper_id = scraper.id
    self.scraper_name_label.setText(f"{scraper.name} [{scraper.category}]")
    self.scraper_description_label.setText(scraper.description)
    self.scraper_source_label.setText(
      f"Source: {scraper.source_name}" if scraper.source_name else ""
    )
    self.scraper_homepage_label.setText(f"<a href='{scraper.homepage}'>{scraper.homepage}</a>")

    while self.param_form.rowCount():
      self.param_form.removeRow(0)
    self.param_inputs = {}

    if scraper.params:
      for parameter in scraper.params:
        widget, field = self._build_parameter_widget(parameter)
        label = f"{parameter.key}{' *' if parameter.required else ''}"
        self.param_form.addRow(label, widget)
        self.param_inputs[parameter.key] = field
    else:
      placeholder = QLabel("This scraper does not require extra parameters.")
      self.param_form.addRow(placeholder)

    default_output = Path(self.output_dir_edit.text() or self.settings.output_dir) / f"{scraper.id}.json"
    self.output_file_edit.setText(str(default_output))

  def _collect_scraper_params(self) -> dict[str, str]:
    return {key: widget.text().strip() for key, widget in self.param_inputs.items() if widget.text().strip()}

  def run_selected_scraper(self) -> None:
    scraper = self._selected_scraper()
    if scraper is None:
      QMessageBox.information(self, "No Scraper Selected", "Choose a scraper first.")
      return

    params = self._collect_scraper_params()
    output_path = self.output_file_edit.text().strip()
    if not output_path:
      QMessageBox.warning(self, "Output Path Required", "Choose an output file path.")
      return

    try:
      program, args, working_dir = build_run_command(
        self.settings.toolkit_path,
        self.settings.node_executable,
        scraper.id,
        self.limit_spin.value(),
        output_path,
        params,
        self.run_save_format_combo.currentText(),
      )
    except Exception as error:  # noqa: BLE001
      QMessageBox.warning(self, "Run Failed", str(error))
      return

    self._queue_or_start_process("run", program, args, working_dir)

  def run_selected_category(self) -> None:
    category = self.scraper_category_combo.currentText()
    if category == "all":
      QMessageBox.information(
        self,
        "Choose a Category",
        "Select a specific category first, or use Queue All.",
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
        self.run_save_format_combo.currentText(),
      )
    except Exception as error:  # noqa: BLE001
      QMessageBox.warning(self, "Run Failed", str(error))
      return

    self._queue_or_start_process(mode_label, program, args, working_dir)

  def _queue_or_start_process(
    self,
    label: str,
    program: str,
    args: list[str],
    working_dir: str,
  ) -> None:
    job = QueuedJob(label=label, program=program, args=args, working_dir=working_dir)

    if self.current_process is not None and self.current_process.state() != QProcess.ProcessState.NotRunning:
      self.pending_jobs.append(job)
      self._refresh_queue_list()
      self.log_activity(f"Queued {label}: {describe_command(program, args)}")
      return

    self._start_process(job)

  def _start_process(self, job: QueuedJob) -> None:
    self.current_process_label = job.label
    process = QProcess(self)
    process.setWorkingDirectory(job.working_dir)
    process.setProgram(job.program)
    process.setArguments(job.args)
    process.readyReadStandardOutput.connect(self._consume_process_stdout)
    process.readyReadStandardError.connect(self._consume_process_stderr)
    process.finished.connect(self._finish_process)
    self.current_process = process

    command = describe_command(job.program, job.args)
    self.run_log.appendPlainText(f"$ {command}")
    self.log_activity(f"Started {job.label}: {command}")
    process.start()

  def _refresh_queue_list(self) -> None:
    self.queue_list.clear()
    for job in self.pending_jobs:
      self.queue_list.addItem(f"{job.label}: {describe_command(job.program, job.args)}")

  def remove_selected_queue_job(self) -> None:
    row = self.queue_list.currentRow()
    if row < 0 or row >= len(self.pending_jobs):
      return
    removed = self.pending_jobs.pop(row)
    self._refresh_queue_list()
    self.log_activity(f"Removed queued job: {removed.label}")

  def clear_job_queue(self) -> None:
    if not self.pending_jobs:
      return
    self.pending_jobs.clear()
    self._refresh_queue_list()
    self.log_activity("Cleared the pending job queue.")

  def _start_next_queued_job(self) -> None:
    if not self.pending_jobs:
      return
    next_job = self.pending_jobs.pop(0)
    self._refresh_queue_list()
    self._start_process(next_job)

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
    process = self.current_process
    self.current_process = None

    if exit_status == QProcess.ExitStatus.NormalExit and exit_code == 0:
      self.run_log.appendPlainText(f"{self.current_process_label} finished successfully.")
      self.log_activity(f"{self.current_process_label} finished successfully.")
      self.refresh_results()
    else:
      self.run_log.appendPlainText(
        f"{self.current_process_label} failed with exit code {exit_code}."
      )
      self.log_activity(f"{self.current_process_label} failed with exit code {exit_code}.")

    if process is not None:
      process.deleteLater()

    self._start_next_queued_job()

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
      self.payload_summary_browser.setHtml(build_payload_summary_html(self.current_payload))
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
      self.payload_summary_browser.setHtml(build_payload_summary_html(self.current_payload))
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

  def save_workspace(self) -> None:
    suggested_name = self.workspace_combo.currentText()
    if suggested_name == "Current Session":
      suggested_name = ""
    name, accepted = QInputDialog.getText(
      self,
      "Save Workspace",
      "Workspace name:",
      text=suggested_name,
    )
    if not accepted or not name.strip():
      return

    self.save_settings()
    workspace = WorkspaceProfile(
      name=name.strip(),
      toolkit_path=self.toolkit_path_edit.text().strip(),
      node_executable=self.node_exec_edit.text().strip() or "node",
      output_dir=self.output_dir_edit.text().strip() or default_output_dir(self.toolkit_path_edit.text().strip()),
      save_format=self.default_save_format_combo.currentText(),
    )
    others = [item for item in self.settings.workspaces if item.name != workspace.name]
    others.append(workspace)
    self.settings.workspaces = others
    self.settings.active_workspace = workspace.name
    self.settings_store.save(self.settings)
    self._refresh_workspace_combo(workspace.name)
    self.log_activity(f"Saved workspace '{workspace.name}'.")

  def load_selected_workspace(self) -> None:
    selected_name = self.workspace_combo.currentText()
    if selected_name == "Current Session":
      return

    workspace = next(
      (item for item in self.settings.workspaces if item.name == selected_name),
      None,
    )
    if workspace is None:
      return

    self.toolkit_path_edit.setText(workspace.toolkit_path)
    self.node_exec_edit.setText(workspace.node_executable)
    self.output_dir_edit.setText(workspace.output_dir)
    self.default_save_format_combo.setCurrentText(workspace.save_format)
    self.run_save_format_combo.setCurrentText(workspace.save_format)
    self.settings.active_workspace = workspace.name
    self.save_settings()
    self.log_activity(f"Loaded workspace '{workspace.name}'.")
    self.refresh_everything()

  def delete_selected_workspace(self) -> None:
    selected_name = self.workspace_combo.currentText()
    if selected_name == "Current Session":
      QMessageBox.information(
        self,
        "No Saved Workspace",
        "Select a saved workspace first.",
      )
      return

    self.settings.workspaces = [
      workspace for workspace in self.settings.workspaces if workspace.name != selected_name
    ]
    if self.settings.active_workspace == selected_name:
      self.settings.active_workspace = ""
    self.settings_store.save(self.settings)
    self._refresh_workspace_combo()
    self.log_activity(f"Deleted workspace '{selected_name}'.")

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
      "JSON Files (*.json);;All Files (*.*)",
    )
    if path:
      self.output_file_edit.setText(path)

  def _browse_param_file(self, field: QLineEdit) -> None:
    path, _ = QFileDialog.getOpenFileName(
      self,
      "Choose Parameter File",
      field.text(),
      "Text Files (*.txt);;All Files (*.*)",
    )
    if path:
      field.setText(path)

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
