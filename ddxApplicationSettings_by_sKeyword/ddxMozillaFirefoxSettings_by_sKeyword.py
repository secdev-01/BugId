import os;

from dxConfig import dxConfig;

from fsFirstExistingFile import fsFirstExistingFile;

from cFileSystemItem import cFileSystemItem;
sProgramFilesPath_x86 = os.getenv("ProgramFiles(x86)") or os.getenv("ProgramFiles");
sProgramFilesPath_x64 = os.getenv("ProgramW6432");

dxConfigSettings = {
  "bApplicationTerminatesWithMainProcess": False,
};

# Firefox stable (if installed, otherwise use Firefox Developer Edition if installed).
sApplicationBinaryPath_x64 = sProgramFilesPath_x64 and fsFirstExistingFile(
  r"%s\Mozilla Firefox\firefox.exe" % sProgramFilesPath_x64,
);
sApplicationBinaryPath_x86 = fsFirstExistingFile(
  r"%s\Mozilla Firefox\firefox.exe" % sProgramFilesPath_x86,
);
sApplicationBinaryPath = sApplicationBinaryPath_x64 or sApplicationBinaryPath_x86;

oFirefoxProfileFolder = cFileSystemItem(os.getenv("TEMP")).foGetChild("Firefox-profile");

def fasGetFirefoxStaticArguments(bForHelp):
  fFirefoxCleanup();
  return [
    "--no-remote",
    "-profile", oFirefoxProfileFolder.sPath,
  ];

def fasGetFirefoxOptionalArguments(bForHelp = False):
  return bForHelp and ["<dxConfig.sDefaultBrowserTestURL>"] or [dxConfig["sDefaultBrowserTestURL"]];

def fFirefoxSetup(bFirstRun):
  if bFirstRun:
    # We need to disable the Firefox sandbox, or it won't work with page heap.
    os.environ["MOZ_DISABLE_CONTENT_SANDBOX"] = "1";
    os.environ["MOZ_DISABLE_GMP_SANDBOX"] = "1";
    os.environ["MOZ_DISABLE_NPAPI_SANDBOX"] = "1";
    os.environ["MOZ_DISABLE_GPU_SANDBOX "] = "1";
  # We want to start with a clean state and we use an empty profile folder to
  # do that; create the profile folder if it does not exist and delete everything
  # in it if it does exist.
  fFirefoxCleanup();

def fFirefoxCleanup():
  if not oFirefoxProfileFolder.fbIsFolder():
    assert oFirefoxProfileFolder.fbCreateAsFolder(), \
        "Cannot create Firefox profile folder %s" % oFirefoxProfileFolder.sPath;
  else:
    # Delete the profile to clean up after application ran.
    assert oFirefoxProfileFolder.fbDeleteDescendants(), \
        "Cannot clean up Firefox profile folder %s" % oFirefoxProfileFolder.sPath;

# Known applications can have regular expressions that map source file paths in its output to URLs, so the details HTML for any detected bug can have clickable
# links to an online source repository:
srMozillaCentralSourceURLMappings = "".join([
  r"c:[\\/]builds[\\/]moz2_slave[\\/][^\\/]+[\\/]build[\\/](?:src[\\/])?", # absolute file path
  r"(?P<path>[^:]+\.\w+)", # relative file path
  r"(:| @ |, line )", # separator
  r"(?P<lineno>\d+)",  # line number
]);
dsURLTemplate_by_srSourceFilePath = {srMozillaCentralSourceURLMappings: "https://dxr.mozilla.org/mozilla-central/source/%(path)s#%(lineno)s"};

ddxMozillaFirefoxSettings_by_sKeyword = {
  "firefox": {
    "sBinaryPath": sApplicationBinaryPath,
    "fasGetStaticArguments": fasGetFirefoxStaticArguments,
    "fasGetOptionalArguments": fasGetFirefoxOptionalArguments,
    "dxConfigSettings": dxConfigSettings,
    "fSetup": fFirefoxSetup,
    "fCleanup": fFirefoxCleanup,
    "dsURLTemplate_by_srSourceFilePath": dsURLTemplate_by_srSourceFilePath,
  },
  "firefox_x86": {
    "sBinaryPath": sApplicationBinaryPath_x86,
    "fasGetStaticArguments": fasGetFirefoxStaticArguments,
    "fasGetOptionalArguments": fasGetFirefoxOptionalArguments,
    "dxConfigSettings": dxConfigSettings,
    "fSetup": fFirefoxSetup,
    "fCleanup": fFirefoxCleanup,
    "sISA": "x86",
    "dsURLTemplate_by_srSourceFilePath": dsURLTemplate_by_srSourceFilePath,
  },
  "firefox_x64": {
    "sBinaryPath": sApplicationBinaryPath_x64,
    "fasGetStaticArguments": fasGetFirefoxStaticArguments,
    "fasGetOptionalArguments": fasGetFirefoxOptionalArguments,
    "dxConfigSettings": dxConfigSettings,
    "fSetup": fFirefoxSetup,
    "fCleanup": fFirefoxCleanup,
    "sISA": "x64",
    "dsURLTemplate_by_srSourceFilePath": dsURLTemplate_by_srSourceFilePath,
  },
};
