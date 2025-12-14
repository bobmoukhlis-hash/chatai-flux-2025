#!/usr/bin/env bash
echo "🔧 Aggiorno pip e setuptools..."
pip install --upgrade pip setuptools wheel

echo "📦 Installo i pacchetti richiesti..."
pip install -r requirements.txt || exit 1

echo "✅ Build completata!"
