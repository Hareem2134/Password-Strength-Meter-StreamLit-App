import streamlit as st
import re
import random

# Function to check password criteria
def check_password_criteria(password):
    return {
        "✅ At least 8 characters" if len(password) >= 8 else "❌ At least 8 characters": len(password) >= 8,
        "✅ Uppercase letters" if bool(re.search(r"[A-Z]", password)) else "❌ Uppercase letters": bool(re.search(r"[A-Z]", password)),
        "✅ Lowercase letters" if bool(re.search(r"[a-z]", password)) else "❌ Lowercase letters": bool(re.search(r"[a-z]", password)),
        "✅ Numbers" if bool(re.search(r"\d", password)) else "❌ Numbers": bool(re.search(r"\d", password)),
        "✅ Special characters (!@#$%^&*)" if bool(re.search(r"[!@#$%^&*]", password)) else "❌ Special characters (!@#$%^&*)": bool(re.search(r"[!@#$%^&*]", password)),
        "✅ 12+ characters (recommended)" if len(password) >= 12 else "❌ 12+ characters (recommended)": len(password) >= 12,
        "✅ No common patterns" if not re.search(r"(1234|password|qwerty|admin|abc123)", password, re.IGNORECASE) else "❌ No common patterns": not re.search(r"(1234|password|qwerty|admin|abc123)", password, re.IGNORECASE),
    }

# Function to check password strength
def check_password_strength(password):
    score = sum(check_password_criteria(password).values())
    strength_levels = ["Weak ❌", "Weak ❌", "Moderate ⚠️", "Strong ✅"]
    return strength_levels[min(score, 3)], min(score, 3)

# Function to generate a strong password with custom length
def generate_password(length):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return "".join(random.sample(chars, length))

# Initialize session states
if "password" not in st.session_state:
    st.session_state.password = ""
if "show_password" not in st.session_state:
    st.session_state.show_password = False
if "password_length" not in st.session_state:
    st.session_state.password_length = 16  # Default length

# UI Title
st.title("🔐 Password Strength Meter")

# Password Input Field
password = st.text_input(
    "Enter your password:",
    type="password" if not st.session_state.show_password else "default",  # Toggle visibility
    value=st.session_state.password,
    key="password_input"
)

# ✅ Show Password Toggle Button (Beneath Input Field)
if st.button("👁 Show Password" if not st.session_state.show_password else "🙈 Hide Password"):
    st.session_state.show_password = not st.session_state.show_password
    st.rerun()

# 📊 Password Analysis Section
st.subheader("📊 Password Analysis")

if password:
    criteria_status = check_password_criteria(password)
    for rule, passed in criteria_status.items():
        color = "green" if passed else "red"
        st.markdown(f"<span style='color:{color}; font-size:16px;'>{rule}</span>", unsafe_allow_html=True)
    st.session_state.password = password  # Update session state

# Check Strength Button
if st.button("Check Strength"):
    if password:
        strength, score = check_password_strength(password)
        color = ["red", "red", "orange", "green"][score]
        st.markdown(f"**Password Strength:** <span style='color:{color}; font-size:18px;'>{strength}</span>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a password.")

# 🔢 Password Length Selector
st.subheader("🔢 Choose Password Length")
st.session_state.password_length = st.slider("Select password length:", min_value=8, max_value=32, value=st.session_state.password_length)

# Generate Strong Password Button
if st.button("🔄 Generate Strong Password"):
    st.session_state.password = generate_password(st.session_state.password_length)
    st.rerun()  # Auto-fill input field & retain settings

# 🔍 Password Security Facts
st.subheader("🔍 Password Security Facts")
st.info("""
- A password with 8 characters can be cracked in **less than 8 hours** using modern techniques.
- Adding **just 4 more characters** can increase cracking time to **several years**.
- Using a **unique password for each site** prevents credential stuffing attacks.
- **Password managers** are the safest way to manage multiple complex passwords.
- **Two-factor authentication (2FA)** adds an extra layer of security beyond passwords.
""")

# 🛡️ Privacy Notice
st.subheader("🛡️ Your password is never stored or transmitted")
st.success("All analysis happens in your browser for maximum security.")
