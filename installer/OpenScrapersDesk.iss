#define MyAppName "Open Scrapers Desk"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Open Scrapers contributors"
#define MyAppURL "https://github.com/Ninezel/open-scrapers-desk"
#define MyAppExeName "OpenScrapersDesk.exe"

[Setup]
AppId={{2BF1A714-BC7B-4188-BD4B-69767454D97A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\Open Scrapers Desk
DefaultGroupName=Open Scrapers Desk
WizardStyle=modern
OutputDir=..\release
OutputBaseFilename=OpenScrapersDesk-Setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
Source: "..\dist\OpenScrapersDesk\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\Open Scrapers Desk"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Open Scrapers Desk"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Open Scrapers Desk"; Flags: nowait postinstall skipifsilent
