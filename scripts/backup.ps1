# BlazeKV Automated Backup Script
# Run this script daily or weekly to backup your data.db and repository

param(
    [string]$BackupPath = "$env:USERPROFILE\BlazeKV_Backups",
    [int]$RetentionDays = 30,
    [switch]$Force
)

# Configuration
$ProjectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$DataFile = Join-Path $ProjectRoot "data.db"
$LogFile = Join-Path $BackupPath "backup.log"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    Write-Host $logEntry
    Add-Content -Path $LogFile -Value $logEntry
}

# Create backup directory if it doesn't exist
if (-not (Test-Path $BackupPath)) {
    New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null
    Write-Log "Created backup directory: $BackupPath"
}

# Check if data.db exists
if (-not (Test-Path $DataFile)) {
    Write-Log "WARNING: data.db not found at $DataFile" "WARN"
    if (-not $Force) {
        Write-Log "Backup skipped. Use -Force to proceed anyway." "ERROR"
        exit 1
    }
}

try {
    # Create timestamped backup
    $timestamp = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'
    $backupFile = Join-Path $BackupPath "data_$timestamp.db"
    
    if (Test-Path $DataFile) {
        Copy-Item -Path $DataFile -Destination $backupFile -Force
        Write-Log "Backup created: $backupFile" "SUCCESS"
    } else {
        Write-Log "Created empty backup marker at $backupFile"
        New-Item -Path $backupFile -ItemType File -Force | Out-Null
    }
    
    # Get backup file size
    $backupSize = (Get-Item $backupFile).Length
    Write-Log "Backup size: $backupSize bytes"
    
    # Clean up old backups
    $oldBackups = Get-ChildItem -Path $BackupPath -Filter "data_*.db" -File | 
        Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-$RetentionDays) }
    
    if ($oldBackups) {
        Write-Log "Removing $(($oldBackups | Measure-Object).Count) backup(s) older than $RetentionDays days"
        $oldBackups | Remove-Item -Force
    }
    
    # List current backups
    $currentBackups = Get-ChildItem -Path $BackupPath -Filter "data_*.db" -File | 
        Sort-Object -Property LastWriteTime -Descending
    Write-Log "Current backups: $(($currentBackups | Measure-Object).Count)"
    
    Write-Log "Backup completed successfully" "SUCCESS"
    exit 0
    
} catch {
    Write-Log "Backup failed: $_" "ERROR"
    exit 1
}
