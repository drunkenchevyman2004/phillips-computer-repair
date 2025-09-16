<#!> Synopsis:
<#!> This PowerShell script performs a basic cleanup of a Windows system.
<#!> It clears the Recycle Bin, removes temporary files from key system
<#!> directories, deletes temporary data from each user’s profile, and
<#!> executes the built‑in Disk Cleanup utility using a saved
<#!> configuration.  The script should be run with administrative
<#!> privileges.
<#!>
<#!> References:
<#!> – The Recycle Bin can be emptied using PowerShell commands; the
<#!>   `Clear‑RecycleBin` command deletes all items without prompting
<#!>   for confirmation【138572527972950†L31-L57】.  Alternatively, you
<#!>   can enumerate the `$Recycle.Bin` folder and remove items with
<#!>   `Remove‑Item`【762764994538650†L114-L124】.
<#!> – Temporary files under `C:\Windows\Temp`, `C:\Windows\Prefetch`
<#!>   and each user’s `AppData\Local\Temp` folder can be removed using
<#!>   `Get‑ChildItem` and `Remove‑Item` with the `‑Recurse` and
<#!>   `‑Force` parameters【762764994538650†L132-L154】.
<#!> – The Disk Cleanup tool (`cleanmgr`) removes unused files such as
<#!>   temporary files, downloaded Internet files and Recycle Bin
<#!>   contents; running `cleanmgr /sagerun:1` launches the utility
<#!>   with previously saved options【762764994538650†L161-L179】.

<#
    .Description
    This script cleans up a Windows computer by:
      1. Emptying the Recycle Bin.
      2. Deleting files in system temporary directories.
      3. Deleting temporary files in each user’s local app data.
      4. Running the built‑in Disk Cleanup utility (`cleanmgr`).

    IMPORTANT: Before using `cleanmgr /sagerun:1` you must run
    `cleanmgr /sageset:1` once manually to select the cleanup
    categories you want the Disk Cleanup utility to clear.  This
    manual step creates the “1” configuration used by `sagerun:1`.

    .Notes
    Author:  ChatGPT (auto‑generated)
    Date:    2025‑09‑16
    Version: 1.0
#>

param()

# region Functions

# Write a message with a timestamp
function Write‑Log {
    param(
        [string] $Message,
        [ConsoleColor] $Color = [ConsoleColor]::White
    )
    $timestamp = (Get‑Date).ToString("yyyy‑MM‑dd HH:mm:ss")
    Write‑Host "[$timestamp] $Message" -ForegroundColor $Color
}

# Attempt to delete contents of a folder
function Clear‑Folder {
    param(
        [string] $Path
    )
    if (Test‑Path $Path) {
        try {
            # Recursively enumerate items and remove them
            Get‑ChildItem ‑LiteralPath $Path ‑Recurse ‑Force ‑ErrorAction SilentlyContinue |
                Remove‑Item ‑Recurse ‑Force ‑ErrorAction SilentlyContinue
            Write‑Log "Cleared $Path" -Color Green
        } catch {
            Write‑Log "Failed to clear $Path: $_" -Color Yellow
        }
    } else {
        Write‑Log "$Path does not exist, skipping." -Color DarkYellow
    }
}

# endregion

# Ensure the script is running with administrative rights
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write‑Log "ERROR: This script must be run as Administrator." -Color Red
    Write‑Log "Right‑click the script and choose 'Run with PowerShell' as Administrator." -Color Red
    exit 1
}

Write‑Log "Starting system cleanup…" -Color Cyan

# 1. Empty the Recycle Bin
try {
    # Use Clear‑RecycleBin if available (PowerShell 5.1+)
    Clear‑RecycleBin ‑Force ‑ErrorAction SilentlyContinue
    Write‑Log "Recycle Bin cleared." -Color Green
} catch {
    # Fallback: manually delete items in Recycle Bin folders
    $recyclePaths = Get‑ChildItem "C:\$Recycle.Bin" ‑Directory ‑ErrorAction SilentlyContinue | Select‑Object ‑ExpandProperty FullName
    foreach ($path in $recyclePaths) {
        Clear‑Folder $path
    }
}

# 2. Delete system temporary files
$systemTempDirs = @(
    "C:\\Windows\\Temp",
    "C:\\Windows\\Prefetch"
)
foreach ($dir in $systemTempDirs) {
    Clear‑Folder $dir
}

# 3. Delete temporary files for each user
try {
    $userProfiles = Get‑ChildItem "C:\\Users" ‑Directory ‑ErrorAction SilentlyContinue
    foreach ($profile in $userProfiles) {
        $tempPath = Join‑Path $profile.FullName "AppData\\Local\\Temp"
        Clear‑Folder $tempPath
    }
} catch {
    Write‑Log "Failed to enumerate user profiles: $_" -Color Yellow
}

# 4. Run Disk Cleanup (cleanmgr) with saved settings #1
try {
    # The user must have run 'cleanmgr /sageset:1' beforehand to define what is cleaned.
    Write‑Log "Running Disk Cleanup with saved configuration (#1)…" -Color Cyan
    Start‑Process "cleanmgr.exe" "/sagerun:1" -Wait
    Write‑Log "Disk Cleanup completed." -Color Green
} catch {
    Write‑Log "Failed to run Disk Cleanup: $_" -Color Yellow
}

Write‑Log "System cleanup finished." -Color Cyan
