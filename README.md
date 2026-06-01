# EcoNomics Bot

EcoNomics Bot is an agentic decision-support system designed to assist in evaluation for environmental and economic aspects. **Note: This project does not function as an actual decision maker; instead, it serves a supportive role in the process by evaluating issues from multiple perspectives.**

The system leverages specialized AI agents to analyze data, compile reports, and provide insights directly through a Telegram interface.

## Core Features

- **Multi-Perspective Evaluation**: Processes queries and urban issues through two primary lenses:
    - **Utilitarian Perspective**: Focuses on the "greatest good for the greatest number."
    - **Environmental (Green) Perspective**: Prioritizes ecological health and sustainability.
    - **Automatic Synthesis**: Every query concludes with a final summary and conclusion provided by the **Summarizer Agent**.
- **Environmental & Climate Monitoring**: Compiles up-to-date data including:
    - **Air Quality Reports**: Real-time monitoring of AQI, PM2.5, and PM10 via the WAQI API.
    - **Climate News**: Automated curation of recent local news regarding sustainability and climate change.
- **Dynamic Reporting**: Compares current environmental snapshots with previous data to identify trends and shifts in city status.

## Telegram Interaction

The primary way to interact with the system is through its Telegram bot. Below are the available commands and interaction methods:

| Method / Command | Description |
| :--- | :--- |
| **Any text query** | Send any question or urban issue to receive a comparative analysis from both the Utilitarian and Green agents, followed by an automatic summary and conclusion. |
| **`report`** | Generates a comprehensive summary of current air quality metrics, deltas from previous reports, and relevant climate news. |
| **`change city`** | Update the city location for reports and searches. Once triggered, only the name of the city needs to be entered (e.g., Berlin). |
| **`help`** | Displays available commands and usage information. |

## Why Telegram?

Telegram was chosen as the primary interface for several key reasons:

- **Accessibility**: Users can interact with the AI agents from any device (mobile, desktop, or web) without needing to install custom applications.
- **Real-time Interaction**: The bot provides immediate feedback and push notifications, which is crucial for monitoring environmental changes and urban reports.
- **Native UI Components**: Features like slash commands and formatted Markdown allow for a clean, structured user experience without a complex custom frontend.
- **Rapid Prototyping**: Utilizing Telegram's robust API allows the project to focus on core agentic logic and multi-perspective decision support while maintaining a premium interface.

## System Architecture

Our multi-agent flowchart is here to visualize the decision-making process and communication flow between specialized agents:

<img width="1920" height="1080" alt="Agents_Flowchart" src="https://github.com/user-attachments/assets/b4675d44-c4b0-4a2e-bd76-5fdfc9a155a2" />

## Project Structure

- `main.py`: Entry point that boots the Telegram bot and manages process lifecycle.
- `agents/`: Contains the logic for specialized AI agents (Green, Utilitarian, Reporter, Summarizer).
- `orchestrators/`: Manages workflows between agents, including comparison pipelines and report generation.
- `services/`: External integrations for Telegram, WAQI (Air Quality), and DuckDuckGo Search.
- `config.py`: Centralized configuration and environment variable management.

## Setup & Installation

### Prerequisites

- Python 3.10+
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- An OpenAI API Key
- A WAQI API Token (from [aqicn.org](https://aqicn.org/api/))

### Configuration

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the following variables:
   ```env
   TELEGRAM_BOT_TOKEN=your_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   OPENAI_API_KEY=your_openai_key_here
   AIR_QUALITY_API_KEY=your_waqi_token_here
   
   # Optional
   OPENAI_MODEL=gpt-4o-mini
   AIR_QUALITY_LOCATION=würzburg
   ```

## Running the Project

To start the bot, run:
```bash
python main.py
```

The system includes a conflict-prevention mechanism that will automatically terminate any existing local instances and force-claim the Telegram polling session to ensure only one bot is active at a time.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
