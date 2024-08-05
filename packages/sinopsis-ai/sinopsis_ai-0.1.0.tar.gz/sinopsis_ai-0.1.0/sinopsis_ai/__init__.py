
# Import key classes and functions to make them available directly from the package
from .client import SinopsisAI

__all__ = ['SinopsisAI', '_retrieve_existing_chat_history', 'update_conversation_in_db', 'log_prompt', 'log_response']

