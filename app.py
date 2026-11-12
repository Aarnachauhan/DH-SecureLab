import streamlit as st
import plotly.graph_objects as go

from simulation.normal_exchange import run_normal_exchange
from simulation.mitm_attack import run_mitm_attack
from simulation.authenticated_exchange import run_authenticated_exchange
from simulation.secure_mitm import run_secure_mitm

from crypto.encryption import encrypt_message, decrypt_message


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="DH SecureLab",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background: #0b1120;
        color: #e5e7eb;
    }

    /* ===== TOP HEADER ===== */

    header[data-testid="stHeader"] {
        display: flex !important;
        background: #0b1120 !important;
        border-bottom: 1px solid #263449 !important;
    }

    header[data-testid="stHeader"] * {
        color: #f8fafc !important;
    }

    /* Keep the sidebar toggle visible */
    header[data-testid="stHeader"] button {
        color: #f8fafc !important;
        background: transparent !important;
    }

    /* ===== SIDEBAR ===== */

    [data-testid="stSidebar"] {
        background: #111827 !important;
    }

    [data-testid="stSidebar"] * {
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] li {
        color: #F8FAFC !important;
        opacity: 1 !important;
    }

    /* Navigation radio buttons */
    [data-testid="stSidebar"] [data-testid="stRadio"] label,
    [data-testid="stSidebar"] [data-testid="stRadio"] p {
        color: #F1F5F9 !important;
        opacity: 1 !important;
    }

    /* Navigation hover */
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        color: #a5b4fc !important;
    }

    /* Sidebar captions */
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #CBD5E1 !important;
        opacity: 1 !important;
    }

    /* Selected navigation option */
    [data-testid="stSidebar"] [data-testid="stRadio"] input:checked + div {
        border-color: #818CF8 !important;
    }

    /* ===== TEXT SELECTION ===== */

    ::selection {
        background: #6366f1 !important;
        color: #ffffff !important;
    }

    /* ===== HIDE DEPLOY BUTTON ONLY ===== */

    [data-testid="stAppDeployButton"] {
        display: none !important;
    }

    /* Remove top decoration */
    [data-testid="stDecoration"] {
        display: none !important;
    }

    /* Remove unnecessary top padding */
    .block-container {
        padding-top: 2rem !important;
    }

    .hero {
        padding: 28px;
        border-radius: 16px;
        background: linear-gradient(120deg, #172554, #312e81);
        margin-bottom: 25px;
        border: 1px solid #3730a3;
    }

    .hero h1 {
        color: white;
        font-size: 36px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #c7d2fe;
        font-size: 16px;
    }

    .section-title {
        color: #a5b4fc;
        font-size: 23px;
        font-weight: 700;
        margin-top: 15px;
    }

    /* ===== METRIC BOXES FIX ===== */
    div[data-testid="stMetric"] {
        background: #172033;
        border: 1px solid #263449;
        padding: 16px;
        border-radius: 12px;
    }

    div[data-testid="stMetric"] [data-testid="stMetricLabel"] p {
        color: #94a3b8 !important; /* Light slate for labels */
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #f8fafc !important; /* Bright white/slate for values */
    }

    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }

    .info-box {
        background: #172033;
        padding: 16px;
        border-radius: 10px;
        border-left: 4px solid #818cf8;
        margin: 10px 0;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# REUSABLE FUNCTIONS
# --------------------------------------------------

def show_hero(title, description):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_flow(nodes, colors, descriptions):
    """Display a simple Alice-Bob-Eve communication diagram."""

    positions = list(range(len(nodes)))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=positions,
        y=[0] * len(nodes),
        mode="markers+text",
        marker=dict(
            size=65,
            color=colors,
            line=dict(color="#c7d2fe", width=2)
        ),
        text=nodes,
        textposition="middle center",
        textfont=dict(color="white", size=13),
        hovertext=descriptions,
        hoverinfo="text"
    ))

    for i in range(len(nodes) - 1):
        fig.add_annotation(
            x=i + 1,
            y=0,
            ax=i + 0.18,
            ay=0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=3,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor="#a5b4fc"
        )

    fig.update_layout(
        height=230,
        margin=dict(l=20, r=20, t=25, b=20),
        xaxis=dict(visible=False, range=[-0.5, len(nodes) - 0.5]),
        yaxis=dict(visible=False, range=[-0.7, 0.7]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


def show_result(label, value):
    st.metric(label, value)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.markdown("# 🔐 DH SecureLab")
st.sidebar.caption("Interactive Cryptography Simulator")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Normal DH Exchange",
        "MITM Attack",
        "Authenticated Exchange",
        "AES-GCM Messaging",
        "Encrypted MITM Attack"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### Project Modules")
st.sidebar.caption("Diffie–Hellman")
st.sidebar.caption("RSA Digital Signatures")
st.sidebar.caption("HKDF Key Derivation")
st.sidebar.caption("AES-256-GCM Encryption")

st.sidebar.divider()
st.sidebar.caption("Educational cryptography project")


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if page == "Overview":

    show_hero(
        "DH SecureLab",
        "An Interactive Diffie–Hellman Key Exchange and "
        "Man-in-the-Middle Attack Simulator"
    )

    st.markdown("## Welcome to SecureLab")

    st.write(
        "Explore how two parties establish a shared secret, "
        "how an attacker can intercept an unauthenticated exchange, "
        "and how digital signatures help prevent impersonation."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        show_result("Cryptographic techniques", "4")

    with col2:
        show_result("Attack simulations", "2")

    with col3:
        show_result("Encryption algorithm", "AES-GCM")

    st.markdown("### Explore the modules")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔑 Diffie–Hellman")
        st.write("Understand public keys and shared-secret generation.")

        st.markdown("#### 🛡️ RSA Authentication")
        st.write("Verify public keys using digital signatures.")

        st.markdown("#### 🔒 AES-GCM")
        st.write("Encrypt and decrypt messages using authenticated encryption.")

    with col2:
        st.markdown("#### ⚠️ MITM Attack")
        st.write("See how Eve intercepts and replaces public keys.")

        st.markdown("#### ✅ Secure Exchange")
        st.write("Observe how authentication rejects an impersonation attempt.")

    st.warning(
        "Educational demonstration only. The current Diffie–Hellman "
        "implementation uses small toy parameters and is not suitable "
        "for real-world security."
    )


# --------------------------------------------------
# NORMAL DH EXCHANGE
# --------------------------------------------------

elif page == "Normal DH Exchange":

    show_hero(
        "Normal Diffie–Hellman Exchange",
        "Alice and Bob establish a common secret without transmitting it."
    )

    if st.button("Run Key Exchange", type="primary"):

        result = run_normal_exchange()

        show_flow(
            ["Alice", "Bob"],
            ["#2563eb", "#059669"],
            ["Generates a public key", "Generates a public key"]
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Alice")
            show_result("Public Key", result["alice_public_key"])
            show_result("Shared Secret", result["alice_secret"])

        with col2:
            st.subheader("Bob")
            show_result("Public Key", result["bob_public_key"])
            show_result("Shared Secret", result["bob_secret"])

        if result["keys_match"]:
            st.success("Success! Alice and Bob generated the same shared secret.")
        else:
            st.error("Shared-secret mismatch.")

    else:
        st.info("Click Run Key Exchange to start the simulation.")


# --------------------------------------------------
# MITM ATTACK
# --------------------------------------------------

elif page == "MITM Attack":

    show_hero(
        "Man-in-the-Middle Attack",
        "See how Eve intercepts public keys and establishes separate secrets."
    )

    st.write(
        "In an unauthenticated Diffie–Hellman exchange, "
        "an attacker can replace the public keys exchanged by Alice and Bob."
    )

    if st.button("Launch MITM Attack", type="primary"):

        result = run_mitm_attack()

        show_flow(
            ["Alice", "Eve", "Bob"],
            ["#2563eb", "#dc2626", "#059669"],
            ["Alice communicates with Eve", "Attacker intercepts both sides",
             "Bob communicates with Eve"]
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            show_result("Alice's Secret", result["alice_secret"])

        with col2:
            show_result("Eve–Alice Secret", result["eve_alice_secret"])

        with col3:
            show_result("Eve–Bob Secret", result["eve_bob_secret"])

        st.error("MITM attack successful!")

        st.write(
            "Eve establishes separate shared secrets with Alice and Bob. "
            "Alice and Bob do not share the same secret."
        )

        st.write(
            "Eve can communicate independently with both parties:",
            result["eve_can_read_alice"] and result["eve_can_read_bob"]
        )

    else:
        st.info("Click Launch MITM Attack to simulate the attack.")


# --------------------------------------------------
# AUTHENTICATED EXCHANGE
# --------------------------------------------------

elif page == "Authenticated Exchange":

    show_hero(
        "Authenticated Key Exchange",
        "RSA digital signatures help Alice and Bob verify public keys."
    )

    st.write(
        "Each participant signs their Diffie–Hellman public key. "
        "The receiving party verifies the signature before accepting the key."
    )

    if st.button("Run Authentication Tests", type="primary"):

        normal = run_authenticated_exchange(attack=False)
        attack = run_authenticated_exchange(attack=True)

        st.markdown("### Normal authenticated exchange")

        col1, col2, col3 = st.columns(3)

        with col1:
            show_result("Alice verifies Bob", str(normal["alice_verified"]))

        with col2:
            show_result("Bob verifies Alice", str(normal["bob_verified"]))

        with col3:
            show_result("Shared secrets match", str(normal["keys_match"]))

        st.success(normal["message"])

        st.divider()

        st.markdown("### MITM attempt with authentication")

        col1, col2 = st.columns(2)

        with col1:
            show_result("Alice verifies Eve's key", str(attack["alice_verified"]))

        with col2:
            show_result("Bob verifies Eve's key", str(attack["bob_verified"]))

        st.error(attack["message"])


# --------------------------------------------------
# AES-GCM MESSAGING
# --------------------------------------------------

elif page == "AES-GCM Messaging":

    show_hero(
        "AES-GCM Secure Messaging",
        "Send an encrypted message using a Diffie–Hellman shared secret."
    )

    message = st.text_area(
        "Enter your message",
        value="Hello Bob! This is Alice.",
        height=100
    )

    if st.button("Encrypt and Send", type="primary"):

        if not message.strip():
            st.warning("Please enter a message.")
        else:
            result = run_normal_exchange()

            encrypted = encrypt_message(
                result["alice_secret"],
                message
            )

            decrypted = decrypt_message(
                result["bob_secret"],
                encrypted
            )

            st.markdown("### Alice's message")
            st.info(message)

            st.markdown("### Encrypted ciphertext")

            st.code(encrypted["ciphertext"].hex(), language="text")

            st.markdown("### Bob's decrypted message")
            st.success(decrypted)

            if decrypted == message:
                st.success("Message encrypted and decrypted successfully!")


# --------------------------------------------------
# ENCRYPTED MITM ATTACK
# --------------------------------------------------

elif page == "Encrypted MITM Attack":

    show_hero(
        "Encrypted MITM Attack",
        "Observe how Eve can read and modify encrypted messages "
        "when key exchange is not authenticated."
    )

    if st.button("Execute Encrypted MITM Attack", type="primary"):

        result = run_secure_mitm()

        show_flow(
            ["Alice", "Eve", "Bob"],
            ["#2563eb", "#dc2626", "#059669"],
            ["Encrypts message", "Decrypts and modifies message",
             "Receives modified message"]
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Alice sends")
            st.info(result["original_message"])

            st.markdown("### Eve intercepts")
            st.warning(result["intercepted_message"])

        with col2:
            st.markdown("### Eve modifies")
            st.error(result["modified_message"])

            st.markdown("### Bob receives")
            st.warning(result["bob_received_message"])

        col1, col2 = st.columns(2)

        with col1:
            show_result("Eve can read", str(result["eve_can_read"]))

        with col2:
            show_result("Eve can modify", str(result["eve_can_modify"]))

        if result["eve_can_read"] and result["eve_can_modify"]:
            st.error("Attack successful! Encryption alone did not stop Eve.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "DH SecureLab | Applied Cryptography Project | "
    "Educational use only"
)