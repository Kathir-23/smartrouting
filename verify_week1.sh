#!/bin/bash
# Save as: verify_week1.sh

echo "🔍 WEEK 1 VERIFICATION SCRIPT"
echo "=============================="

echo "✅ Python version:"
python --version

echo "✅ PostgreSQL version:"
psql --version

echo "✅ Git status:"
git status

echo "✅ Alembic version:"
cd backend && alembic --version && cd ..

echo "✅ Alembic history:"
cd backend && alembic history && cd ..

echo "✅ Database tables:"
psql -U postgres smartrouting -c "\dt"

echo "✅ User count:"
psql -U postgres smartrouting -c "SELECT COUNT(*) FROM users;"

echo "✅ Vehicle count:"
psql -U postgres smartrouting -c "SELECT COUNT(*) FROM vehicles;"

echo "✅ Incident count:"
psql -U postgres smartrouting -c "SELECT COUNT(*) FROM incidents;"

echo ""
echo "✅ WEEK 1 VERIFICATION COMPLETE!"
