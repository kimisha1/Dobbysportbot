# Sports Programmer Telegram Bot

A specialized Telegram bot (`app.py`) that combines software engineering expertise with sports analytics knowledge. The bot uses Fireworks AI to provide intelligent responses about coding, sports data analysis, and the intersection of technology and sports.

## Features
- **Sports Programming Expertise**: Combines software engineering (Python, JavaScript, SQL, algorithms) with sports knowledge
- **AI-Powered Responses**: Uses Fireworks AI (`dobby-unhinged-llama-3-3-70b-new`) for intelligent, contextual answers
- **Code Generation**: Provides code snippets, pseudo-code, and step-by-step explanations
- **Sports Analytics**: Helps with performance metrics, match statistics, and predictive modeling
- **Concurrent Request Handling**: Global semaphore limits to manage multiple simultaneous requests
- **Enhanced Retry Logic**: Exponential backoff with improved timeout handling (10s connection, 120s read)
- **Robust Error Handling**: Specific handling for timeout and connection errors with detailed logging
- **User-Friendly Interface**: Typing indicators and clear error messages

## Requirements
- Python 3.10+
- Telegram Bot Token
- Fireworks API Key

## Installation
```bash
pip install python-telegram-bot==21.6 requests
```

## Configuration
Update the configuration variables in `app.py`:

```python
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
FIREWORKS_API_KEY = "YOUR_FIREWORKS_API_KEY_HERE"
```

Optional settings:
- `GLOBAL_MAX_CONCURRENT_REQUESTS = 5` (adjust based on your needs)
- `FIREWORKS_MODEL = "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new"`

## Running the Bot
```bash
python app.py
```

Expected output:
```
Bot is running. Press Ctrl+C to stop.
```

## Usage Examples

### Commands
- `/start` - Initialize the bot and get a welcome message
- `/help` - Display available features and example queries

### Sample Queries
The bot can help with various sports programming topics:

**Data Fetching:**
- "Write Python code to fetch Champions League results from an API and save to CSV"
- "How do I scrape football match statistics from a website?"

**Analytics & Modeling:**
- "How do I compute expected goals (xG) from match events?"
- "Give me a regression model for predicting win/loss"
- "Create a Python script to analyze basketball player performance"

**Code Debugging:**
- "Fix this pandas error in my script"
- "Help me optimize this SQL query for sports data"
- "Debug my JavaScript code for real-time score updates"

**Sports Knowledge:**
- "Explain the difference between possession-based and counter-attacking football"
- "What are the key metrics for evaluating basketball defense?"

## How It Works

1. **Message Reception**: Bot receives user messages via Telegram long polling
2. **Processing**: Shows typing indicator and enters semaphore for rate limiting
3. **AI Processing**: Sends query to Fireworks AI with sports programmer context
4. **Response**: Returns formatted answer with code snippets or explanations
5. **Error Handling**: Graceful error messages for API failures or invalid requests

## Bot Personality

The bot is designed as an experienced Sports Programmer who:
- Provides clear, accurate, and useful answers
- Offers practical code solutions and explanations
- Suggests real-world approaches for data fetching and analysis
- Maintains a friendly, professional tone
- Explicitly states limitations when real-time data isn't available

## Troubleshooting

**Common Issues:**

- **Bot not responding**: Check `TELEGRAM_BOT_TOKEN` and ensure bot is started via BotFather
- **API errors**: Verify `FIREWORKS_API_KEY` and account access
- **Timeout errors**: The bot now has improved timeout handling (10s connection, 120s read timeout) with automatic retries
- **Slow responses**: Adjust `GLOBAL_MAX_CONCURRENT_REQUESTS` based on your quota
- **Event loop errors**: Run `python app.py` from a normal shell (not Jupyter/IPython)

**Timeout & Connection Issues:**
- The bot includes enhanced error handling for timeout and connection errors
- Automatic retry with exponential backoff (3 attempts by default)
- Separate connection and read timeouts for better reliability
- Console logging shows retry attempts for debugging

**Rate Limiting:**
- The bot includes built-in rate limiting to prevent API quota exhaustion
- Adjust `GLOBAL_MAX_CONCURRENT_REQUESTS` if you experience issues

## Security Notes

- **Production Deployment**: Move API keys to environment variables or secure configuration
- **Monitoring**: Add logging and monitoring for production use
- **Access Control**: Consider implementing user authentication for sensitive operations

## Customization

You can modify the bot's behavior by editing the `system_instruction` in the `call_fireworks_sports_programmer()` function to:
- Change the bot's expertise area
- Adjust response style and tone
- Add specific domain knowledge
- Modify language or cultural context

## Contributing

Feel free to enhance the bot by:
- Adding new command handlers
- Improving error handling
- Adding more specialized sports programming features
- Implementing data visualization capabilities

