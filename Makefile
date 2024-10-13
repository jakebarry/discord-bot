# Variables
PYTHON_VERSION := python3.12# Specify your Python version
VENV := venv# Virtual environment folder
REQ := requirements.txt# Requirements file

# Create virtual environment
.PHONY: venv
venv:
	test -d venv || $(PYTHON_VERSION) -m venv $(VENV)
	@echo "Virtual environment created successfully"

# Install dependencies
.PHONY: install
install: venv
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r $(REQ)
	@echo "Required packages installed successfully"

# Format code using ruff
.PHONY: format
format:
	$(VENV)/bin/ruff check --fix

# Clean the virtual environment
.PHONY: clean
clean:
	rm -rf $(VENV)

# Run the bot
.PHONY: run
run:
	$(VENV)/bin/python bot.py  # Adjust if the main file is different
