"""
Hangman — Streamlit UI. Run:  streamlit run app.py
"""

from __future__ import annotations

import random

import streamlit as st

WORDS = [
    "python",
    "computer",
    "keyboard",
    "monitor",
    "program",
    "variable",
    "function",
    "string",
    "number",
    "puzzle",
    "garden",
    "planet",
    "rocket",
    "ocean",
    "tiger",
    "eagle",
    "castle",
    "bridge",
    "window",
    "shadow",
]

MAX_WRONG_GUESSES = 6


def init_session():
    """Set up game state in session_state."""
    if "word" not in st.session_state:
        st.session_state.word = random.choice(WORDS)
    if "guessed_letters" not in st.session_state:
        st.session_state.guessed_letters = set()
    if "wrong_letters" not in st.session_state:
        st.session_state.wrong_letters = set()
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "won" not in st.session_state:
        st.session_state.won = False


def new_game():
    """Start a fresh round."""
    st.session_state.word = random.choice(WORDS)
    st.session_state.guessed_letters = set()
    st.session_state.wrong_letters = set()
    st.session_state.game_over = False
    st.session_state.won = False


def word_display(word: str, guessed: set) -> str:
    """Letters or blanks, spaced for readability."""
    parts = []
    for ch in word:
        parts.append(ch.upper() if ch in guessed else "—")
    return "  ".join(parts)


def all_letters_guessed(word: str, guessed: set) -> bool:
    return all(c in guessed for c in word)


def apply_guess(raw: str) -> str | None:
    """
    Process one guess. Returns None if OK, or an error message string.
    """
    if st.session_state.game_over:
        return "Game is over — use **Restart** to play again."

    guess = raw.strip().lower()
    if len(guess) != 1:
        return "Enter **exactly one** letter."
    if not guess.isalpha():
        return "Only **A–Z** letters count."

    if guess in st.session_state.guessed_letters:
        return f"You already tried **{guess.upper()}**."

    st.session_state.guessed_letters.add(guess)

    if guess in st.session_state.word:
        if all_letters_guessed(st.session_state.word, st.session_state.guessed_letters):
            st.session_state.game_over = True
            st.session_state.won = True
    else:
        st.session_state.wrong_letters.add(guess)
        remaining = MAX_WRONG_GUESSES - len(st.session_state.wrong_letters)
        if remaining <= 0:
            st.session_state.game_over = True
            st.session_state.won = False

    return None


def inject_styles():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

            html, body, [class*="css"] {
                font-family: 'Outfit', sans-serif;
            }

            .stApp {
                background: radial-gradient(1200px 800px at 10% -10%, #1a1f35 0%, transparent 55%),
                            radial-gradient(900px 600px at 100% 0%, #2d1b4e 0%, transparent 50%),
                            linear-gradient(165deg, #0a0c10 0%, #12151c 45%, #0d1018 100%);
                color: #e8ecf4;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #141824 0%, #0f1219 100%) !important;
                border-right: 1px solid rgba(124, 92, 255, 0.25);
            }

            [data-testid="stSidebar"] .block-container {
                padding-top: 2rem;
            }

            [data-testid="stHeader"] {
                background: rgba(10, 12, 16, 0.85);
                backdrop-filter: blur(8px);
            }

            h1 {
                font-weight: 700 !important;
                letter-spacing: -0.02em;
                background: linear-gradient(120deg, #c4b5fd 0%, #7c3aed 40%, #22d3ee 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .hangman-card {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(124, 92, 255, 0.2);
                border-radius: 16px;
                padding: 1.5rem 1.75rem;
                margin-bottom: 1rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
            }

            .word-line {
                font-family: 'JetBrains Mono', monospace;
                font-size: clamp(1.6rem, 5vw, 2.4rem);
                font-weight: 700;
                letter-spacing: 0.12em;
                color: #f1f5f9;
                text-align: center;
                padding: 0.5rem 0;
            }

            .metric-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                background: rgba(34, 211, 238, 0.12);
                border: 1px solid rgba(34, 211, 238, 0.35);
                color: #67e8f9;
                padding: 0.35rem 0.85rem;
                border-radius: 999px;
                font-weight: 600;
                font-size: 0.95rem;
            }

            div[data-testid="stFormSubmitButton"] button {
                background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important;
                color: white !important;
                border: none !important;
                font-weight: 600 !important;
                border-radius: 10px !important;
                padding: 0.5rem 1.25rem !important;
                box-shadow: 0 4px 20px rgba(124, 58, 237, 0.45);
            }

            div[data-testid="stFormSubmitButton"] button:hover {
                box-shadow: 0 6px 28px rgba(124, 58, 237, 0.55);
            }

            .stTextInput input {
                border-radius: 10px !important;
                border: 1px solid rgba(148, 163, 184, 0.25) !important;
                background: rgba(15, 18, 25, 0.8) !important;
                color: #f8fafc !important;
            }

            .stAlert {
                border-radius: 12px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="Hangman",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_styles()
    init_session()

    with st.sidebar:
        st.markdown("### 🎯 Hangman")
        st.caption("Guess the word before you run out of tries.")
        st.divider()
        st.markdown(
            """
**How to play**
1. Type **one letter** and submit.
2. Correct letters appear in the word.
3. Wrong letters cost a try — you have **6** total.

Good luck!
            """
        )
        st.divider()
        if st.button("🔄 Restart game", use_container_width=True, type="primary"):
            new_game()
            st.rerun()

    st.markdown("# Hangman")
    st.caption("Dark mode · letter by letter")

    word = st.session_state.word
    guessed = st.session_state.guessed_letters
    wrong = st.session_state.wrong_letters
    remaining = max(0, MAX_WRONG_GUESSES - len(wrong))
    correct_only = sorted(guessed - wrong)

    col_main, col_side = st.columns([2.2, 1])

    with col_main:
        st.markdown('<div class="hangman-card">', unsafe_allow_html=True)
        st.markdown(
            f'<p class="word-line">{word_display(word, guessed)}</p>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<p style="text-align:center;margin-top:0.5rem;">'
            f'<span class="metric-pill">❤️ Remaining tries: {remaining}</span></p>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**✅ Correct guesses**")
            st.write(", ".join(c.upper() for c in correct_only) if correct_only else "_None yet_")
        with c2:
            st.markdown("**❌ Wrong guesses**")
            st.write(", ".join(c.upper() for c in sorted(wrong)) if wrong else "_None yet_")

        if st.session_state.game_over:
            st.divider()
            if st.session_state.won:
                st.success(f"🎉 **You won!** The word was **{word.upper()}**.")
            else:
                st.error(f"💀 **Game over.** The word was **{word.upper()}**.")
        else:
            st.divider()
            with st.form("guess_form", clear_on_submit=True):
                guess_input = st.text_input(
                    "Your guess",
                    placeholder="e.g. A",
                    max_chars=5,
                    label_visibility="collapsed",
                )
                submitted = st.form_submit_button("Submit letter")

            if submitted:
                err = apply_guess(guess_input or "")
                if err:
                    st.warning(err)
                else:
                    st.rerun()

    with col_side:
        st.markdown(
            """
<div class="hangman-card" style="margin-top:0;">
<p style="margin:0 0 0.75rem 0;font-weight:600;color:#c4b5fd;">Quick stats</p>
<p style="margin:0.25rem 0;color:#94a3b8;font-size:0.9rem;">Letters in word</p>
<p style="margin:0;font-size:1.75rem;font-weight:700;color:#22d3ee;">"""
            + str(len(set(word)))
            + """</p>
<p style="margin:1rem 0 0.25rem 0;color:#94a3b8;font-size:0.9rem;">Unique guesses</p>
<p style="margin:0;font-size:1.75rem;font-weight:700;color:#a78bfa;">"""
            + str(len(guessed))
            + """</p>
</div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Streamlit · dark theme")


if __name__ == "__main__":
    main()
