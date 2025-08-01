# HackRX API v2 Test Runner (PowerShell)
# Usage: .\test_runner.ps1

param(
    [string]$TestType = "",
    [string]$Server = "http://localhost:8000",
    [int]$Repeats = 1,
    [switch]$Verbose,
    [string]$ApiKey = ""
)

Write-Host "🚀 HackRX API v2 Test Runner" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Gray

if (-not $TestType) {
    Write-Host ""
    Write-Host "Available test types:" -ForegroundColor Yellow
    Write-Host "  simple      - Quick API test" -ForegroundColor White
    Write-Host "  load        - Comprehensive load test" -ForegroundColor White
    Write-Host "  repeat      - Run multiple times" -ForegroundColor White
    Write-Host "  stress      - Stress test with 10 repeats" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Green
    Write-Host "  .\test_runner.ps1 -TestType simple" -ForegroundColor Gray
    Write-Host "  .\test_runner.ps1 -TestType load -Verbose" -ForegroundColor Gray
    Write-Host "  .\test_runner.ps1 -TestType repeat -Repeats 5" -ForegroundColor Gray
    Write-Host "  .\test_runner.ps1 -TestType load -Server http://prod-server.com" -ForegroundColor Gray
    exit
}

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not detected." -ForegroundColor Yellow
    Write-Host "💡 Activating .venv..." -ForegroundColor Blue
    
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        & ".venv\Scripts\Activate.ps1"
    } else {
        Write-Host "❌ .venv not found. Please create virtual environment first." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Configuration:" -ForegroundColor Blue
Write-Host "  Server: $Server" -ForegroundColor White
Write-Host "  Repeats: $Repeats" -ForegroundColor White
Write-Host "  Verbose: $($Verbose.IsPresent)" -ForegroundColor White
Write-Host "  API Key: $($ApiKey ? 'Provided' : 'Not provided')" -ForegroundColor White
Write-Host ""

switch ($TestType.ToLower()) {
    "simple" {
        Write-Host "🏃 Running simple test..." -ForegroundColor Green
        python Test\simple_test.py
    }
    
    "load" {
        Write-Host "🏋️  Running load test..." -ForegroundColor Green
        $args = @("Test\load_test.py", "--server", $Server)
        if ($Verbose) { $args += "--verbose" }
        if ($ApiKey) { $args += "--api-key", $ApiKey }
        if ($Repeats -gt 1) { $args += "--repeat", $Repeats }
        
        python @args
    }
    
    "repeat" {
        if ($Repeats -le 1) { $Repeats = 3 }
        Write-Host "🔄 Running repeat test ($Repeats times)..." -ForegroundColor Green
        
        $args = @("Test\load_test.py", "--server", $Server, "--repeat", $Repeats)
        if ($Verbose) { $args += "--verbose" }
        if ($ApiKey) { $args += "--api-key", $ApiKey }
        
        python @args
    }
    
    "stress" {
        Write-Host "💪 Running stress test (10 repeats)..." -ForegroundColor Green
        
        $args = @("Test\load_test.py", "--server", $Server, "--repeat", "10", "--timeout", "600")
        if ($Verbose) { $args += "--verbose" }
        if ($ApiKey) { $args += "--api-key", $ApiKey }
        
        python @args
    }
    
    default {
        Write-Host "❌ Unknown test type: $TestType" -ForegroundColor Red
        Write-Host "💡 Use: simple, load, repeat, or stress" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Test completed!" -ForegroundColor Green
