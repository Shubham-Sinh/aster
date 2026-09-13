from typing import Literal

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

from tools.historical_tool import history_tool
from tools.parc import weather_tool
from Agent_file.ml_agent1 import ml_model

from weather_rag.rag_pipeline.rag_pipeline import build_pipeline


# =========================================================
# 1. OLLAMA MODEL
# =========================================================

llm = ChatOllama(
    model="llama3.2:3b",
    base_url="http://127.0.0.1:11434",
    temperature=0.5
)


# =========================================================
# 2. AVAILABLE TOOLS
# =========================================================

tools = [
    history_tool,
    weather_tool,
    ml_model
]


# =========================================================
# 3. ROUTER
# =========================================================

def router(question: str) -> str:
    """
    Decide whether the question should be answered using
    RAG government documents or weather/ML tools.
    """

    question_lower = question.lower().strip()

    # =====================================================
    # 1. STRONG RAG / GOVERNMENT INTENT
    # =====================================================

    rag_keywords = [
        "government",
        "govt",
        "guideline",
        "guidelines",
        "crop damage",
        "crop damaged",
        "crop loss",
        "crop losses",
        "insurance",
        "insurance claim",
        "wbcis",
        "rwbcis",
        "nais",
        "weather data",
        "aws",
        "automatic weather station",
        "scheme",
        "compensation",
        "claim",
        "farmer compensation",
        "agriculture guideline",
        "agricultural guideline",
        "government scheme",
        "government rule",
        "government rules",
        "official guideline",
        "official guidelines",
        "farmer guideline",
        "farmer guidelines",
        "crop insurance",
        "damage assessment",
        "loss assessment",
        "weather station"
    ]

    # =====================================================
    # 2. STRONG FARMER / AGRICULTURE INTENT
    # =====================================================

    farmer_keywords = [
        "farmer",
        "farmers",
        "kisan",
        "kisan ke liye",
        "kheti",
        "fasal",
        "crop",
        "farming",
        "agriculture",
        "agricultural",
        "agri"
    ]

    # =====================================================
    # 3. WEATHER / ML TOOL INTENT
    # =====================================================

    tool_keywords = [
        "current weather",
        "weather now",
        "temperature",
        "humidity",
        "rainfall",
        "rain prediction",
        "rain prediction",
        "forecast",
        "weather forecast",
        "flood",
        "flood risk",
        "flood prediction",
        "wind speed",
        "pressure",
        "historical weather",
        "past weather",
        "previous weather"
    ]

    # =====================================================
    # PRIORITY 1: GOVERNMENT / GUIDELINE QUESTIONS
    # =====================================================

    for keyword in rag_keywords:
        if keyword in question_lower:
            return "RAG"

    # =====================================================
    # PRIORITY 2: FARMER / AGRICULTURE QUESTIONS
    # =====================================================

    for keyword in farmer_keywords:
        if keyword in question_lower:
            return "RAG"

    # =====================================================
    # PRIORITY 3: WEATHER / ML QUESTIONS
    # =====================================================

    for keyword in tool_keywords:
        if keyword in question_lower:
            return "TOOL"

    # =====================================================
    # DEFAULT
    # =====================================================

    return "RAG"


# =========================================================
# 4. RAG ANSWER
# =========================================================

def rag_answer(question: str) -> str:
    """
    Search government guideline PDFs and generate an answer.
    """

    try:
        documents = build_pipeline(question)

        if not documents:
            return "I could not find relevant information in the government guideline documents."

        context = "\n\n".join(
            [
                doc.page_content
                for doc in documents
            ]
        )

        prompt = f"""
You are WeatherGPT, an AI assistant designed to help Indian farmers.

Answer the user's question using ONLY the information
provided in the retrieved government documents.

If the answer is not available in the documents,
clearly say that the information was not found.

Do not invent government rules, compensation amounts,
eligibility criteria or deadlines.

Explain the answer in simple language.

User Question:
{question}

Government Document Context:
{context}
"""

        response = llm.invoke(
            [
                HumanMessage(content=prompt)
            ]
        )

        return response.content

    except Exception as e:
        return f"RAG processing error: {str(e)}"


# =========================================================
# 5. TOOL ANSWER
# =========================================================

def tool_answer(question: str) -> str:
    """
    Answer weather/flood related questions.
    """

    question_lower = question.lower()

    try:

        # -------------------------------------------------
        # FLOOD
        # -------------------------------------------------

        if "flood" in question_lower:

            # Try to find a city name from common Indian cities.
            cities = [
                "delhi",
                "mumbai",
                "patna",
                "sitamarhi",
                "sitamari",
                "kolkata",
                "lucknow",
                "jaipur",
                "chennai",
                "hyderabad",
                "bengaluru",
                "bangalore",
                "pune",
                "ahmedabad",
                "varanasi",
                "muzaffarpur",
                "gaya"
            ]

            city = None

            for item in cities:
                if item in question_lower:
                    city = item
                    break

            if city is None:
                return (
                    "Please mention the city for which you want "
                    "the flood prediction."
                )

            location = weather_tool.invoke(city)

            if isinstance(location, str):
                return location

            result = ml_model.invoke(
                {
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "day": 1
                }
            )

            return str(result)


        # -------------------------------------------------
        # CURRENT WEATHER
        # -------------------------------------------------

        if (
            "current weather" in question_lower
            or "weather now" in question_lower
            or "temperature" in question_lower
        ):

            cities = [
                "delhi",
                "mumbai",
                "patna",
                "sitamarhi",
                "kolkata",
                "lucknow",
                "jaipur",
                "chennai",
                "hyderabad",
                "bengaluru",
                "bangalore",
                "pune",
                "ahmedabad",
                "varanasi",
                "muzaffarpur",
                "gaya"
            ]

            city = None

            for item in cities:
                if item in question_lower:
                    city = item
                    break

            if city is None:
                return (
                    "Please mention the city for which you want "
                    "the current weather."
                )

            result = weather_tool.invoke(city)

            return str(result)


        # -------------------------------------------------
        # HISTORICAL WEATHER
        # -------------------------------------------------

        if (
            "historical" in question_lower
            or "past weather" in question_lower
            or "previous weather" in question_lower
        ):

            cities = [
                "delhi",
                "mumbai",
                "patna",
                "sitamarhi",
                "kolkata",
                "lucknow",
                "jaipur",
                "chennai",
                "hyderabad",
                "bengaluru",
                "bangalore",
                "pune",
                "ahmedabad",
                "varanasi",
                "muzaffarpur",
                "gaya"
            ]

            city = None

            for item in cities:
                if item in question_lower:
                    city = item
                    break

            if city is None:
                return (
                    "Please mention the city for which you want "
                    "historical weather."
                )

            location = weather_tool.invoke(city)

            if isinstance(location, str):
                return location

            result = history_tool.invoke(
                {
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "days": 7
                }
            )

            return str(result)


        # -------------------------------------------------
        # GENERAL WEATHER QUESTION
        # -------------------------------------------------

        prompt = f"""
You are WeatherGPT.

The user asked:

{question}

Give a short, useful answer for an Indian farmer.

If exact live weather information is required but
no city/location was provided, ask the user to provide
their city.

Do not invent live weather data.
"""

        response = llm.invoke(
            [
                HumanMessage(content=prompt)
            ]
        )

        return response.content

    except Exception as e:
        return f"Weather tool error: {str(e)}"


# =========================================================
# 6. MAIN WEATHERGPT FUNCTION
# =========================================================

def ask_weather_gpt(question: str) -> str:
    """
    Main function used by FastAPI / React.
    """

    if not question or not question.strip():
        return "Please enter a question."

    question = question.strip()

    route = router(question)

    print(f"Question: {question}")
    print(f"Selected route: {route}")

    if route == "RAG":
        return rag_answer(question)

    return tool_answer(question)


# =========================================================
# 7. OPTIONAL LANGGRAPH-STYLE APP COMPATIBILITY
# =========================================================

class WeatherGPTApp:

    def invoke(self, data):

        messages = data.get("messages", [])

        if not messages:
            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": "Please provide a question."
                    }
                ]
            }

        last_message = messages[-1]

        if isinstance(last_message, tuple):
            question = last_message[1]

        elif isinstance(last_message, HumanMessage):
            question = last_message.content

        elif isinstance(last_message, dict):
            question = last_message.get("content", "")

        else:
            question = str(last_message)

        answer = ask_weather_gpt(question)

        return {
            "messages": [
                {
                    "role": "human",
                    "content": question
                },
                {
                    "role": "assistant",
                    "content": answer
                }
            ],
            "answer": answer
        }


# FastAPI can import this as `app`
app = WeatherGPTApp()


# =========================================================
# IMPORTANT
# =========================================================
#
# There is NO:
#
# input("Ask Question: ")
#
# here.
#
# FastAPI will call ask_weather_gpt()
# =========================================================