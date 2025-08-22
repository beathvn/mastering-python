# ruff: noqa: I001

# system imports
import logging
import os

logging.basicConfig(
    format="[{levelname}] {name}: {message}",
    style="{",
)

LOGGER_NAME = "loggingTest"
from azure.monitor.opentelemetry import configure_azure_monitor

# 3rd party imports
import streamlit as st

if st.session_state.get("first_run") is None:
    configure_azure_monitor(
        logger_name=LOGGER_NAME,
        connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"],
        enable_live_metrics=True,
        disable_offline_storage=True,
        logging_formatter=logging.Formatter("[%(levelname)s] %(name)s: %(message)s"),
    )
    st.session_state["first_run"] = True

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)

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
