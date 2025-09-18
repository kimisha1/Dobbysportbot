import json
import asyncio
from typing import Optional
import time
import requests
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# ========================
# CONFIG
# ========================
TELEGRAM_BOT_TOKEN = ""  # <-- put your Telegram bot token here
FIREWORKS_API_KEY = ""   # <-- put your Fireworks API key here
FIREWORKS_URL = "https://api.fireworks.ai/inference/v1/chat/completions"
FIREWORKS_MODEL = "accounts/sentientfoundation/models/dobby-unhinged-llama-3-3-70b-new"

GLOBAL_MAX_CONCURRENT_REQUESTS = 5
_ai_call_semaphore = asyncio.Semaphore(GLOBAL_MAX_CONCURRENT_REQUESTS)


# ========================
# FIREWORKS CALL
# ========================
def call_fireworks_sports_programmer(user_text: str) -> str:
    """Call Fireworks AI to answer as a sports programmer and return the result or raise."""
    if not FIREWORKS_API_KEY or "<FIREWORKS_API_KEY>" in FIREWORKS_API_KEY:
        raise RuntimeError("FIREWORKS_API_KEY is not set in code")

    system_instruction = (
        "You are an experienced Sports Programmer. "
        "Your job is to combine knowledge of software engineering (Python, JavaScript, SQL, algorithms, "
        "data analysis) with the world of sports (football, basketball, volleyball, athletics, "
        "performance analytics, match statistics).\n"
        "- Always give clear, accurate, and useful answers.\n"
        "- Provide code snippets, pseudo-code, or step-by-step explanations when appropriate.\n"
        "- If real-time sports data is needed and you cannot access it, suggest practical ways to fetch it (APIs, scripts).\n"
        "- Do not make up fake data; be explicit about limitations.\n"
        "- Tone: friendly, professional, and concise."
    )

    payload = {
        "model": FIREWORKS_MODEL,
        "max_tokens": 1024,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_text},
        ],
        "stream": False,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
    }

    response = requests.post(FIREWORKS_URL, headers=headers, data=json.dumps(payload), timeout=(10, 120))
    if response.status_code != 200:
        error_msg = f"Fireworks API error: {response.status_code}"
        try:
            error_detail = response.text
            error_msg += f" - {error_detail}"
        except:
            pass
        raise RuntimeError(error_msg)

    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("Fireworks API returned no choices")

    message = choices[0].get("message") or {}
    content = message.get("content")
    if not content:
        raise RuntimeError("Fireworks API returned empty content")
    return content.strip()


def _call_fireworks_with_retry(user_text: str, attempts: int = 3, base_delay_seconds: float = 1.0) -> str:
    """Call the Fireworks API with simple exponential backoff retries."""
    last_error: Optional[Exception] = None
    for attempt_index in range(attempts):
        try:
            return call_fireworks_sports_programmer(user_text)
        except requests.exceptions.Timeout as exc:
            last_error = RuntimeError(f"Request timeout (attempt {attempt_index + 1}/{attempts}): {exc}")
        except requests.exceptions.ConnectionError as exc:
            last_error = RuntimeError(f"Connection error (attempt {attempt_index + 1}/{attempts}): {exc}")
        except Exception as exc:  # broad to bubble up to user if all attempts fail
            last_error = exc
        
        if attempt_index < attempts - 1:
            delay = base_delay_seconds * (2 ** attempt_index)
            print(f"Retrying in {delay} seconds... (attempt {attempt_index + 1}/{attempts})")
            time.sleep(delay)
    
    if last_error:
        raise last_error
    raise RuntimeError("Unknown error while calling Fireworks API")


# ========================
# TELEGRAM HANDLERS
# ========================
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! I am a Sports Programmer bot. Ask me anything about coding, sports analytics, or both."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "I am a Sports Programmer. Ask me about:\n"
            "- Writing scripts to fetch football/basketball stats\n"
            "- Building predictive models for match outcomes\n"
            "- Debugging Python, SQL, or JS code\n"
            "- Sports analytics (e.g., xG, performance metrics)\n\n"
            "Examples:\n"
            "- 'Write Python code to fetch Champions League results from an API and save to CSV'\n"
            "- 'How do I compute expected goals (xG) from match events?'\n"
            "- 'Give me a regression model for predicting win/loss'\n"
            "- 'Fix this pandas error in my script'\n\n"
            "Commands: /start , /help"
        ),
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    if not user_text:
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    wait_msg = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Thinking as a Sports Programmer..."
    )
    try:
        async with _ai_call_semaphore:
            reply_text = await asyncio.to_thread(_call_fireworks_with_retry, user_text)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=reply_text,
            )
    except Exception as exc:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Error: {exc}",
        )
    finally:
        try:
            await wait_msg.delete()
        except Exception:
            pass


# ========================
# MAIN ENTRY
# ========================
def main() -> None:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()