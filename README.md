# Discord Recipe Planner Bot

A simple Discord bot built with Python that helps users with recipe planning. The bot can perform various tasks and respond to commands related to recipes in a Discord server.

## Features

- Responds to user commands
- Integrates with external recipe APIs
- Can handle multiple commands and functionalities for recipe planning

## Installation

### Prerequisites
Ensure you have Python 3.12 or the version specified in the Makefile installed on your system.

### Clone and Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/jakebarry/discord-bot.git
   ```

2. Navigate to the project directory:
   ```bash
   cd discord-bot
   ```

### Using the Makefile

The Makefile automates the process of setting up the virtual environment, installing dependencies, and ensuring code formatting. Follow these steps to streamline the setup:

3. **Create a virtual environment and install dependencies:**
   Run the following command to automatically create a virtual environment and install the required dependencies:
   ```bash
   make install
   ```

4. **Activate the virtual environment (optional):**
   The Makefile uses the virtual environment directly, but if you want to manually activate it:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

### Code Formatting
To ensure the code adheres to the formatting standards set by `ruff`, run:
```bash
make format
```

### Running the Bot
To run the Discord Recipe Planner bot:
```bash
make run
```

### Cleaning the Environment
To remove the virtual environment and clean up the project directory:
```bash
make clean
```

## Technologies Used

- Python 3.12
- Discord.py
- Beautiful Soup
- Requests
- Dotenv
- PyMongo
- Validators
- TLDextract
- Ruff (for formatting)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions for improvements.

## Author

Jake Barry - [GitHub Profile](https://github.com/jakebarry)
