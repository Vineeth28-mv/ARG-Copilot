"""
LLM Interface using OpenAI API

Centralized module for calling OpenAI models.
"""

import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Default model
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


def call_llm(
    system_prompt: str,
    user_prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 4000
) -> str:
    """
    Call OpenAI API with system and user prompts.
    
    Args:
        system_prompt: System-level instructions
        user_prompt: User query or task description
        model: Model name (default: gpt-4o)
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens in response
        
    Returns:
        Response text from LLM
        
    Raises:
        Exception if API call fails
    """
    if model is None:
        model = DEFAULT_MODEL
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        raise


def call_llm_with_history(
    system_prompt: str,
    messages: list,
    model: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 4000
) -> str:
    """
    Call OpenAI API with message history (for multi-turn conversations).
    
    Args:
        system_prompt: System-level instructions
        messages: List of dicts with 'role' and 'content' keys
        model: Model name (default: gpt-4o)
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens in response
        
    Returns:
        Response text from LLM
    """
    if model is None:
        model = DEFAULT_MODEL
    
    try:
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        
        response = client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        raise


def estimate_tokens(text: str) -> int:
    """
    Rough estimate of token count (1 token ≈ 4 characters).
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    return len(text) // 4

