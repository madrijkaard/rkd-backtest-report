#!/bin/bash
set -e

# Check if the script is sourced
(return 0 2>/dev/null) || {
    echo "⚠️  This script must be executed using 'source venv.sh [-u]' to work correctly."
    exit 1
}

# Verificar se o argumento -u foi passado
UPDATE_REQS=false
for arg in "$@"; do
    if [ "$arg" == "-u" ]; then
        UPDATE_REQS=true
        break
    fi
done

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    py -m venv venv
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Instalar dependências apenas se a flag -u for passada
if $UPDATE_REQS; then
    if [ -f "requirements.txt" ]; then
        echo "📄 requirements.txt found. Installing dependencies..."
        pip install --upgrade pip

        mapfile -t packages < requirements.txt
        total=${#packages[@]}
        count=0

        for pkg in "${packages[@]}"; do
            count=$((count + 1))
            percent=$((count * 100 / total))
            filled=$((percent / 5))  # 20-block progress bar
            empty=$((20 - filled))
            bar=$(printf "%0.s█" $(seq 1 $filled))
            bar+=$(printf "%0.s " $(seq 1 $empty))
            echo -ne "\r🔄 [$bar] $count/$total: $pkg"
            pip install "$pkg" 2>/dev/null | grep -v "Requirement already satisfied" || true
        done

        echo -e "\n✅ Dependency installation complete!"
    else
        echo "⚠️  No requirements.txt found. Skipping dependency installation."
    fi
else
    echo "ℹ️  Skipping dependency installation. Use 'source venv.sh -u' to install requirements."
fi

# Run the main script
echo "🚀 Running executor.py..."
python executor.py
