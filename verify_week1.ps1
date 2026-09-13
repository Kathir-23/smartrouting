Write-Host "🔍 WEEK 1 VERIFICATION SCRIPT"
Write-Host "=============================="

Write-Host "`n✅ Python version:"
.\backend\venv\Scripts\python.exe --version

Write-Host "`n✅ PostgreSQL version:"
psql --version

Write-Host "`n✅ Git status:"
git status -s

Write-Host "`n✅ Alembic version:"
Push-Location backend
.\venv\Scripts\alembic.exe --version
Pop-Location

Write-Host "`n✅ Alembic history:"
Push-Location backend
.\venv\Scripts\alembic.exe history
Pop-Location

$env:PGPASSWORD = 'password123'
Write-Host "`n✅ Database tables:"
psql -U postgres -d smartrouting -c "\dt"

Write-Host "`n✅ User count:"
psql -U postgres -d smartrouting -c "SELECT COUNT(*) FROM users;"

Write-Host "`n✅ Vehicle count:"
psql -U postgres -d smartrouting -c "SELECT COUNT(*) FROM vehicles;"

Write-Host "`n✅ Incident count:"
psql -U postgres -d smartrouting -c "SELECT COUNT(*) FROM incidents;"

Write-Host "`n✅ WEEK 1 VERIFICATION COMPLETE!"
