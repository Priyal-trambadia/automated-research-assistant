import streamlit as st
from research_engine import research_question


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🔎 ResearchAI")
    st.caption("Intelligent Web Research Assistant")

    st.divider()

    # ABOUT
    st.subheader("🤖 About")

    st.write(
        """
        ResearchAI uses AI to decide whether web research
        is required and generates a clear answer with sources.
        """
    )

    st.divider()

    # FEATURES
    st.subheader("✨ Features")

    st.write("🤖 AI-powered search decision")
    st.write("🔎 DuckDuckGo web search")
    st.write("🧠 Gemini AI analysis")
    st.write("📚 Source URLs")
    st.write("📝 Research answers")
    st.write("📜 Research history")

    st.divider()

    # HISTORY
    st.subheader("📜 Research History")

    if st.session_state.history:

        for item in reversed(st.session_state.history[-5:]):

            question_text = item["question"]

            if len(question_text) > 45:
                question_text = question_text[:45] + "..."

            st.caption(f"🔎 {question_text}")

    else:

        st.caption("No research history yet.")

    # CLEAR HISTORY
    if st.session_state.history:

        st.divider()

        if st.button(
            "🗑️ Clear History",
            use_container_width=True
        ):

            st.session_state.history = []
            st.rerun()


# =========================================================
# MAIN HEADER
# =========================================================

st.title("🔎 ResearchAI")

st.subheader(
    "Intelligent Web Research Assistant"
)

st.write(
    "Ask a question and let ResearchAI decide whether "
    "web research is needed."
)


# =========================================================
# INFORMATION BOX
# =========================================================

st.info(
    "💡 Tip: Ask questions like "
    "'What are the latest developments in Generative AI?' "
    "or 'What is Python?'"
)


# =========================================================
# QUESTION INPUT
# =========================================================

st.subheader("💬 What would you like to research?")

question = st.text_area(
    "Enter your question",
    placeholder=(
        "Example: What are the latest developments "
        "in Generative AI?"
    ),
    height=120,
    label_visibility="collapsed"
)


# =========================================================
# RESEARCH BUTTON
# =========================================================

research_button = st.button(
    "🔎 Start Research",
    use_container_width=True,
    type="primary"
)


# =========================================================
# RESEARCH PROCESS
# =========================================================

if research_button:

    # -----------------------------------------------------
    # Check empty question
    # -----------------------------------------------------

    if not question.strip():

        st.warning(
            "⚠️ Please enter a question first."
        )

    else:

        # -------------------------------------------------
        # Run ResearchAI
        # -------------------------------------------------

        with st.spinner(
            "🤖 ResearchAI is analyzing your question..."
        ):

            try:

                result = research_question(
                    question
                )

                # -----------------------------------------
                # Get result information
                # -----------------------------------------

                decision = result["decision"]
                answer = result["answer"]
                sources = result["sources"]

                # -----------------------------------------
                # Save history
                # -----------------------------------------

                st.session_state.history.append(
                    {
                        "question": question,
                        "decision": decision
                    }
                )

                # -----------------------------------------
                # Agent Decision
                # -----------------------------------------

                st.divider()

                st.subheader("🤖 Agent Decision")

                if decision == "SEARCH":

                    st.success(
                        "🔎 Web research used"
                    )

                else:

                    st.success(
                        "🤖 Direct AI answer"
                    )

                # -----------------------------------------
                # Answer
                # -----------------------------------------

                st.divider()

                st.subheader("📝 Research Answer")

                st.write(answer)

                # -----------------------------------------
                # Sources
                # -----------------------------------------

                st.divider()

                st.subheader("📚 Sources")

                if sources:

                    st.write(
                        f"ResearchAI found {len(sources)} web sources."
                    )

                    for i, source in enumerate(
                        sources,
                        start=1
                    ):

                        title = source.get(
                            "title",
                            "Unknown Source"
                        )

                        url = source.get(
                            "href",
                            ""
                        )

                        description = source.get(
                            "body",
                            ""
                        )

                        # Source card using Streamlit
                        with st.expander(
                            f"📄 Source {i}: {title}"
                        ):

                            if description:

                                st.write(
                                    description
                                )

                            if url:

                                st.markdown(
                                    f"[🔗 Open Source]({url})"
                                )

                else:

                    st.info(
                        "ℹ️ No web sources were needed "
                        "for this question."
                    )

            # -------------------------------------------------
            # ERROR HANDLING
            # -------------------------------------------------

            except Exception as e:

                error_message = str(e)

                if (
                    "429" in error_message
                    or "quota" in error_message.lower()
                ):

                    st.error(
                        """
                        ⏳ Gemini API quota is temporarily exhausted.

                        Please wait until your Gemini API quota resets,
                        then try again.
                        """
                    )

                else:

                    st.error(
                        "❌ Something went wrong."
                    )

                    st.code(
                        error_message
                    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🔎 ResearchAI • AI-Powered Web Research Assistant"
)

st.caption(
    "Built with Python • Streamlit • Gemini • DuckDuckGo"
)
















# import streamlit as st

# from research_engine import research_question


# # ==========================================
# # PAGE CONFIG
# # ==========================================

# st.set_page_config(
#     page_title="ResearchAI",
#     page_icon="🔎",
#     layout="wide"
# )


# # ==========================================
# # CUSTOM CSS
# # ==========================================

# st.markdown("""
# <style>

# .main-title {
#     font-size: 42px;
#     font-weight: 700;
#     text-align: center;
#     margin-bottom: 5px;
# }

# .subtitle {
#     text-align: center;
#     font-size: 18px;
#     margin-bottom: 30px;
# }

# .source-card {
#     padding: 15px;
#     border-radius: 10px;
#     border: 1px solid #ddd;
#     margin-bottom: 10px;
# }

# </style>
# """, unsafe_allow_html=True)


# # ==========================================
# # HEADER
# # ==========================================

# st.markdown(
#     '<div class="main-title">🔎 ResearchAI</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     '<div class="subtitle">'
#     'Intelligent Web Research Assistant'
#     '</div>',
#     unsafe_allow_html=True
# )


# # ==========================================
# # DESCRIPTION
# # ==========================================

# st.info(
#     "Ask a question and let the AI decide "
#     "whether web research is needed."
# )


# # ==========================================
# # QUESTION INPUT
# # ==========================================

# question = st.text_area(
#     "💬 What would you like to research?",
#     placeholder=(
#         "Example: What are the latest developments "
#         "in Generative AI?"
#     ),
#     height=100
# )


# # ==========================================
# # RESEARCH BUTTON
# # ==========================================

# if st.button(
#     "🔎 Start Research",
#     use_container_width=True
# ):

#     if not question.strip():

#         st.warning(
#             "⚠️ Please enter a question."
#         )

#     else:

#         # Loading indicator
#         with st.spinner(
#             "🤖 AI is researching your question..."
#         ):

#             try:

#                 result = research_question(
#                     question
#                 )

#                 # ------------------------------
#                 # DECISION
#                 # ------------------------------

#                 decision = result["decision"]

#                 if decision == "SEARCH":

#                     st.success(
#                         "🔎 Web research was used."
#                     )

#                 else:

#                     st.success(
#                         "🤖 Answer generated directly."
#                     )


#                 # ------------------------------
#                 # ANSWER
#                 # ------------------------------

#                 st.markdown(
#                     "## 📝 Research Answer"
#                 )

#                 st.markdown(
#                     result["answer"]
#                 )


#                 # ------------------------------
#                 # SOURCES
#                 # ------------------------------

#                 sources = result["sources"]

#                 if sources:

#                     st.markdown(
#                         "## 📚 Sources"
#                     )

#                     for i, source in enumerate(
#                         sources,
#                         start=1
#                     ):

#                         title = source.get(
#                             "title",
#                             "Unknown source"
#                         )

#                         url = source.get(
#                             "href",
#                             "#"
#                         )

#                         st.markdown(
#                             f"""
#                             **{i}. {title}**

#                             🔗 [Open Source]({url})
#                             """
#                         )

#                         st.divider()


#             except Exception as e:

#                 st.error(
#                     f"❌ Something went wrong: {e}"
#                 )

















# import streamlit as st

# st.set_page_config(
#     page_title="ResearchAI",
#     page_icon="🔎",
#     layout="wide"
# )

# st.title("🔎 ResearchAI")
# st.subheader("Intelligent Web Research Assistant")

# st.write(
#     "Ask a question and let the AI decide whether web research is needed."
# )

# question = st.text_input(
#     "What would you like to research?",
#     placeholder="Example: What are the latest developments in Generative AI?"
# )

# if st.button("🔎 Research"):

#     if question.strip():

#         st.info("🤖 Researching your question...")

#         st.write("Your question:")
#         st.write(question)

#     else:

#         st.warning("Please enter a question.")