# 🤖 Job Updates Telegram Chatbot

Welcome to my first Telegram Chatbot project! The chatbot's primary purpose is to simplify the job hunting process by monitoring job listings on **Smartsheet** and **Remitly** websites. Specifically, it's designed to exclude certain roles such as "Senior", "Software Engineer II", "Engineer III", "Manager", and "Principal", aligning with a customer's specific request.

## 🎯 Key Features

- Monitors job postings from Smartsheet and Remitly in real-time.
- Excludes specific job roles: "Senior", "Software Engineer II", "Engineer III", "Manager", and "Principal".
- Sends instant alerts with job details and a direct link to the job listing when a new job is posted.

## 💻 Requirements

- Python 3.8+
- Telegram API token

## 🔧 Dependencies

- aiogram
- asyncio
- dotenv

## 🚀 Setup and Installation

1. Ensure that you have Python 3.8 or higher installed on your machine.

2. Install the necessary dependencies using pip:
    ```
    pip install aiogram asyncio python-dotenv
    ```

3. Clone the repository:
    ```
    git clone https://github.com/yourusername/JobUpdatesChatbot.git
    ```

4. Navigate into the project directory:
    ```
    cd JobUpdatesChatbot
    ```

5. Set up your environment variables:
    ```
    cp .env.example .env
    ```
   Open the `.env` file and replace `YOUR_TELEGRAM_BOT_TOKEN` with your actual Telegram bot token.

6. Run the bot:
    ```
    python main.py
    ```

## 📚 Usage

Once the bot is running, it will start monitoring the Smartsheet and Remitly websites for job postings. If a new job is posted, the bot will send an alert with the job details.

## 📜 Commands

- `/start` - Start the chatbot and begin monitoring job updates.
- `/send_image` - The bot sends a motivational image.
- `/getdata` - Choose a company (Smartsheet or Remitly) and get a list of all currently posted jobs.
