# sytem imports
import logging

# 3rd party imports
import streamlit as st

logging.basicConfig(
    format="{levelname} - {message}",
    style="{",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.ERROR)

if st.button("DEBUG Click me"):
    st.write("Button clicked!")
    logger.debug("Debug button clicked")


if st.button("INFO Click me"):
    st.write("Button clicked!")
    logger.info("Info button clicked")


if st.button("WARNING Click me"):
    st.write("Button clicked!")
    logger.warning("Warning button clicked")

if st.button("ERROR Click me"):
    st.write("Button clicked!")
    logger.error("Error button clicked")

if st.button("CRITICAL Click me"):
    st.write("Button clicked!")
    logger.critical("Critical button clicked")

if st.button("Exception Click me"):
    try:
        raise ValueError("This is a test exception")
    except ValueError as e:
        logger.exception("Exception occurred: %s", e)
        st.write("An exception has been logged.")
