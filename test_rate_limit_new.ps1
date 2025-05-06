# Replace with your actual JWT token
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2NTI4MDI3LCJpYXQiOjE3NDY1MjQ0MjcsImp0aSI6IjJhYjA4ZTdjZjI4MDQ3OTFiZWExYmYxNDY3ZmFlNzQ4IiwidXNlcl9pZCI6MX0.P5Z4lzuGWr4XhLG3kMUBoMv6Q_hA2eFONoyDuZa7oe8"

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

Write-Host "Testing rate limit response..."
Write-Host "Making 101 requests to trigger rate limit..."

for ($i = 1; $i -le 101; $i++) {
    Write-Host "`nMaking request $i..."
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/api/user-profiles/" -Headers $headers -Method Get
        
        Write-Host "Status Code: $($response.StatusCode)"
        Write-Host "Response: $($response.Content)"
    }
    catch {
        Write-Host "`nRate limit hit!"
        Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)"
        Write-Host "Response: $($_.ErrorDetails.Message)"
        break
    }
    
    # Small delay to make output readable
    Start-Sleep -Milliseconds 100
} 