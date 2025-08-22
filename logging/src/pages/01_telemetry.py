import logging

import streamlit as st

logger = logging.getLogger("loggingTest.Telemetry")
logger.setLevel(logging.INFO)

st.markdown("# Telemetry Logging")

if st.session_state.get("first_run") is None:
    st.switch_page("main.py")

if st.button("DEBUG Click me"):
    st.write("Button clicked!")
    logger.debug("Debug button clicked")


if st.button("INFO Click me"):
    st.write("Button clicked!")
    logger.info(
        "InfoUpload",
        extra={
            "user_id": "user_id_111",
            "file_count": 8,
            "success": True,
            "duration": 0.5,
        },
    )


if st.button("WARNING Click me"):
    st.write("Button clicked!")
    logger.warning(
        "WarningUpload",
        extra={
            "user_id": "user_id_1234",
            "file_count": 10,
            "success": True,
            "duration": 1.3,
        },
    )

if st.button("ERROR Click me"):
    st.write("Button clicked!")
    logger.error(
        "ErrorUpload",
        extra={
            "user_id": "user_id_1234",
            "file_count": 3,
            "success": False,
            "duration": 2.3,
        },
    )

if st.button("CRITICAL Click me"):
    st.write("Button clicked!")
    logger.critical(
        "CriticalUpload",
        extra={
            "user_id": "user_id_1234",
            "file_count": 3,
            "success": False,
            "duration": 2.3,
        },
    )

if st.button("Exception Click me"):
    try:
        raise ValueError("This is a test exception")
    except ValueError as e:
        logger.exception(f"Exception occurred: {e}")
        st.write("An exception has been logged.")
