@echo off
echo Starting Data Breach Analysis Tool...
echo.

echo 1. Installing dependencies...
npm run install-all

echo.
echo 2. Starting all services...
echo - Backend (Node.js): http://localhost:5000
echo - Frontend (React): http://localhost:3000
echo - ML Service (Python): http://localhost:5001
echo.

npm run dev 