# setup.sh

# Function to find the most recent Python version
find_latest_python() {
    local latest_python
    latest_python=$(compgen -c python | grep -E '^python[0-9]+\.[0-9]+$' | sort -V | tail -n 1)
    echo $latest_python
}

# Get the most recent Python version
PYTHON_VERSION=$(find_latest_python)

if [ -z "$PYTHON_VERSION" ]; then
    echo "No suitable Python version found. Please install Python 3.6 or higher."
    exit 1
fi

# Create a virtual environment with the specified Python version
$PYTHON_VERSION -m venv battleship

# Activate the virtual environment
source battleship/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Virtual environment setup complete and dependencies installed!"