
import json
import time
import traceback

import streamlit as st

from google import genai
from google.genai import types

from sources import (
    SOURCES,
    validate_indicator,
    normalize_indicator,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ThreatLens",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# CONSTANTS
# ============================================================

GEMINI_MODEL = "gemini-3.7-flash"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(value: str) -> str:
    """
    Removes leading/trailing whitespace and ensures
    the value contains only ASCII characters.
    """

    return value.strip()


def validate_api_key_ascii(
    api_key: str,
    key_name: str
) -> str:

    cleaned = clean_text(api_key)

    if not cleaned:
        raise ValueError(
            f"{key_name} API key is required."
        )

    try:
        cleaned.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError(
            f"{key_name} API key contains an invalid "
            f"non-ASCII character. Please paste the actual "
            f"API key, not a masked value such as •••••."
        )

    return cleaned


def safe_json(value) -> str:

    try:
        return json.dumps(
            value,
            indent=2,
            ensure_ascii=True,
            default=str
        )
    except Exception:
        return str(value)


# ============================================================
# GEMINI PROMPT
# ============================================================

def build_gemini_prompt(
    indicator: str,
    indicator_type: str,
    knowledge_level: str,
    source_results: dict
) -> str:

    source_text = safe_json(
        source_results
    )

    if knowledge_level == "Beginner":

        instructions = """
You are explaining a cybersecurity indicator to a beginner.

Use very simple language.

Explain:
1. Whether the indicator appears safe, suspicious, or malicious.
2. The most important evidence from VirusTotal and WHOIS.
3. What the evidence means in simple words.
4. What the user should do next.

Avoid unnecessary cybersecurity jargon.
"""

    elif knowledge_level == "Intermediate":

        instructions = """
You are explaining a cybersecurity indicator to an
intermediate-level cybersecurity learner.

Explain:
1. The overall security assessment.
2. Important VirusTotal findings.
3. Important WHOIS findings.
4. Relevant indicators of compromise or risk.
5. Recommended next actions.

Use appropriate cybersecurity terminology,
but explain important terms briefly.
"""

    else:

        instructions = """
You are explaining a cybersecurity indicator to an
expert cybersecurity professional.

Provide:
1. A concise verdict.
2. Evidence-based analysis.
3. VirusTotal detection statistics and reputation.
4. WHOIS registration information when available.
5. Risk indicators and limitations.
6. Recommended defensive actions.

Do not invent evidence.
Clearly distinguish observed evidence from inference.
"""

    prompt = f"""
You are ThreatLens, a cybersecurity threat-analysis assistant.

Indicator:
{indicator}

Indicator type:
{indicator_type}

User knowledge level:
{knowledge_level}

{instructions}

IMPORTANT RULES:

- Only use the supplied source results.
- Do not invent VirusTotal detections.
- Do not invent WHOIS information.
- If a source failed, say that it failed.
- If a source has no data, say that data was unavailable.
- Do not claim certainty when the evidence is inconclusive.
- A missing WHOIS record does NOT automatically mean malicious.
- A clean VirusTotal result does NOT guarantee an indicator is safe.

SOURCE RESULTS:

{source_text}

Return ONLY valid JSON matching this structure:

{{
    "verdict": "Safe",
    "confidence": "Low",
    "summary": "Short explanation",
    "key_findings": [
        "Finding 1",
        "Finding 2",
        "Finding 3"
    ],
    "recommended_actions": [
        "Action 1",
        "Action 2"
    ]
}}

The verdict must be exactly one of:

Safe
Suspicious
Malicious
Inconclusive

The confidence must be exactly one of:

Low
Medium
High
"""

    return prompt


# ============================================================
# GEMINI API CALL
# ============================================================

def call_gemini(
    api_key: str,
    prompt: str
) -> dict:

    key = validate_api_key_ascii(
        api_key,
        "Gemini"
    )

    if not prompt.strip():
        raise ValueError(
            "Gemini prompt is empty."
        )

    # Ensure prompt can be safely encoded.
    try:
        prompt.encode("utf-8")
    except UnicodeEncodeError:
        raise ValueError(
            "The Gemini prompt contains invalid Unicode."
        )

    try:

        client = genai.Client(
            api_key=key
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "object",
                    "properties": {
                        "verdict": {
                            "type": "string",
                            "enum": [
                                "Safe",
                                "Suspicious",
                                "Malicious",
                                "Inconclusive"
                            ]
                        },
                        "confidence": {
                            "type": "string",
                            "enum": [
                                "Low",
                                "Medium",
                                "High"
                            ]
                        },
                        "summary": {
                            "type": "string"
                        },
                        "key_findings": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "recommended_actions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": [
                        "verdict",
                        "confidence",
                        "summary",
                        "key_findings",
                        "recommended_actions"
                    ]
                }
            )
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return json.loads(
            response.text
        )

    except Exception as exc:

        # Log the complete traceback to the Streamlit server logs.
        # Do not write to a Colab-specific /content/ path.
        print("Gemini error:")
        print(traceback.format_exc())

        error_text = str(exc)

        # Retry temporary Google server availability errors.
        if "503" in error_text or "UNAVAILABLE" in error_text:

            time.sleep(3)

            try:

                client = genai.Client(
                    api_key=key
                )

                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema={
                            "type": "object",
                            "properties": {
                                "verdict": {
                                    "type": "string",
                                    "enum": [
                                        "Safe",
                                        "Suspicious",
                                        "Malicious",
                                        "Inconclusive"
                                    ]
                                },
                                "confidence": {
                                    "type": "string",
                                    "enum": [
                                        "Low",
                                        "Medium",
                                        "High"
                                    ]
                                },
                                "summary": {
                                    "type": "string"
                                },
                                "key_findings": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "recommended_actions": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                }
                            },
                            "required": [
                                "verdict",
                                "confidence",
                                "summary",
                                "key_findings",
                                "recommended_actions"
                            ]
                        }
                    )
                )

                if not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return json.loads(
                    response.text
                )

            except Exception:
                print("Gemini retry error:")
                print(traceback.format_exc())
                raise

        raise


# ============================================================
# DISPLAY HELPERS
# ============================================================

def display_verdict(verdict: str):

    if verdict == "Safe":

        st.success(
            "🟢 SAFE"
        )

    elif verdict == "Suspicious":

        st.warning(
            "🟡 SUSPICIOUS"
        )

    elif verdict == "Malicious":

        st.error(
            "🔴 MALICIOUS"
        )

    else:

        st.info(
            "🔵 INCONCLUSIVE"
        )


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ ThreatLens")

st.subheader(
    "Cybersecurity Indicator Analysis"
)

st.write(
    "Analyze an IP address, domain, or URL using "
    "VirusTotal, WHOIS, and Gemini AI."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("API Configuration")

    st.caption(
        "API keys are entered at runtime and are not "
        "hardcoded into the application."
    )

    virustotal_api_key = st.text_input(
        "VirusTotal API Key",
        type="password"
    )

    gemini_api_key = st.text_input(
        "Gemini API Key",
        type="password"
    )

    st.divider()

    st.caption(
        f"Gemini model: {GEMINI_MODEL}"
    )


# ============================================================
# MAIN INPUTS
# ============================================================

col1, col2 = st.columns(
    [1, 2]
)

with col1:

    indicator_type = st.selectbox(
        "Indicator Type",
        [
            "IP Address",
            "Domain",
            "URL"
        ]
    )

with col2:

    indicator = st.text_input(
        "Indicator",
        placeholder=(
            "Example: 8.8.8.8, example.com, "
            "https://example.com"
        )
    )


knowledge_level = st.selectbox(
    "Knowledge Level",
    [
        "Beginner",
        "Intermediate",
        "Expert"
    ]
)


analyze_button = st.button(
    "🔍 Analyze Indicator",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS PIPELINE
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # BASIC CHECK
    # --------------------------------------------------------

    if not indicator.strip():

        st.error(
            "Please enter an indicator."
        )

        st.stop()

    # --------------------------------------------------------
    # API KEY CHECK
    # --------------------------------------------------------

    if not virustotal_api_key.strip():

        st.error(
            "Please enter your VirusTotal API key."
        )

        st.stop()

    if not gemini_api_key.strip():

        st.error(
            "Please enter your Gemini API key."
        )

        st.stop()

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    valid, validation_message = validate_indicator(
        indicator,
        indicator_type
    )

    if not valid:

        st.error(
            validation_message
        )

        st.stop()

    normalized_indicator = normalize_indicator(
        indicator,
        indicator_type
    )

    st.success(
        "Indicator validated."
    )

    # --------------------------------------------------------
    # SOURCE COLLECTION
    # --------------------------------------------------------

    st.info(
        "Collecting VirusTotal and WHOIS results..."
    )

    source_results = {}

    progress = st.progress(
        0
    )

    source_items = list(
        SOURCES.items()
    )

    total_sources = len(
        source_items
    )

    for index, (source_name, source_function) in enumerate(
        source_items,
        start=1
    ):

        try:

            result = source_function(
                indicator,
                indicator_type,
                virustotal_api_key
            )

            source_results[
                source_name
            ] = result

        except Exception as exc:

            source_results[
                source_name
            ] = {
                "source": source_name,
                "status": "error",
                "message": str(exc)
            }

        progress.progress(
            index / total_sources
        )

    progress.empty()

    # --------------------------------------------------------
    # SOURCE RESULTS
    # --------------------------------------------------------

    st.subheader(
        "Source Results"
    )

    source_columns = st.columns(
        len(source_results)
    )

    for column, (source_name, result) in zip(
        source_columns,
        source_results.items()
    ):

        with column:

            st.markdown(
                f"### {source_name}"
            )

            status = result.get(
                "status",
                "unknown"
            )

            if status == "success":

                st.success(
                    "Data collected"
                )

            elif status == "not_found":

                st.warning(
                    "No data found"
                )

            elif status == "not_applicable":

                st.info(
                    "Not applicable"
                )

            else:

                st.error(
                    "Source error"
                )

            with st.expander(
                "View raw result"
            ):

                st.json(
                    result
                )

    # --------------------------------------------------------
    # GEMINI ANALYSIS
    # --------------------------------------------------------

    st.subheader(
        "AI Security Analysis"
    )

    st.info(
        f"Building {knowledge_level} Gemini analysis..."
    )

    prompt = build_gemini_prompt(
        normalized_indicator,
        indicator_type,
        knowledge_level,
        source_results
    )

    st.info(
        "Gemini 3.7 Flash is analyzing..."
    )

    try:

        analysis = call_gemini(
            gemini_api_key,
            prompt
        )

    except Exception as exc:

        st.error(
            f"Gemini analysis failed: {exc}"
        )

        st.caption(
            "Gemini encountered an error. "
            "Please check the Streamlit app logs for details."
        )

        st.stop()

    # --------------------------------------------------------
    # VERDICT
    # --------------------------------------------------------

    verdict = analysis.get(
        "verdict",
        "Inconclusive"
    )

    confidence = analysis.get(
        "confidence",
        "Low"
    )

    display_verdict(
        verdict
    )

    st.markdown(
        f"**Confidence:** {confidence}"
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    st.markdown(
        "### AI Insight"
    )

    st.write(
        analysis.get(
            "summary",
            "No summary was returned."
        )
    )

    # --------------------------------------------------------
    # KEY FINDINGS
    # --------------------------------------------------------

    findings = analysis.get(
        "key_findings",
        []
    )

    if findings:

        st.markdown(
            "### Key Findings"
        )

        for finding in findings:

            st.markdown(
                f"- {finding}"
            )

    # --------------------------------------------------------
    # RECOMMENDED ACTIONS
    # --------------------------------------------------------

    actions = analysis.get(
        "recommended_actions",
        []
    )

    if actions:

        st.markdown(
            "### Recommended Actions"
        )

        for action in actions:

            st.markdown(
                f"- {action}"
            )

    # --------------------------------------------------------
    # RAW AI RESPONSE
    # --------------------------------------------------------

    with st.expander(
        "View AI JSON Response"
    ):

        st.json(
            analysis
        )

    st.divider()

    st.caption(
        "ThreatLens provides an automated assessment based "
        "on the available VirusTotal and WHOIS evidence. "
        "It should not be treated as a definitive security guarantee."
    )
