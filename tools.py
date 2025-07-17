import os
from livekit.agents import function_tool, Agent, RunContext
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()


@function_tool()
async def lookup_weather(
    context: RunContext,
    location: str,
) -> dict[str, str]:
    """Look up weather information for a given location.
    
    Args:
        location: The location to look up weather information for.
    """

    return {"weather": "sunny", "temperature_f": 70}

@function_tool
def send_slack_message(message):
    """Send a message to a Slack channel. use for sending lead info if the lead looks intrested in the product send a message with the lead details like name ,organisation,place,size etc."""
    client = WebClient(token=os.getenv("SLACK_TOKEN"))
    print("Sending message to Slack channel...")
    print("Message: ", message)
    try:
        response = client.chat_postMessage(
            channel="C096VJADZSL",
            text=message
        )
        print("Message sent: ", response["ts"])
    except SlackApiError as e:
        print("Error sending message: ", e.response["error"])


@function_tool
def send_slack_message(
    name: str,
    organisation: str,
    place: str,
    size: str,
    interest_level: str = "interested",
    summary: str = "Lead details",
):
    """
    Send a message to a Slack channel if the lead looks interested in the product
    
    Args:
        name: Name of the lead.
        organisation: Organisation the lead is from.
        place: Location of the lead.
        size: Size of the organisation.
        interest_level: Level of interest (default is "interested").
        summary: A brief summary of the lead's information.
    """

    slack_token = os.getenv("SLACK_TOKEN")
    if not slack_token:
        print("Error: SLACK_TOKEN environment variable is not set.")
        return

    client = WebClient(token=slack_token)
    channel_id = os.getenv("SLACK_CHANNEL_ID", "C096VJADZSL")  # fallback to hardcoded ID

    message = (
        f"*New Lead Alert!*\n"
        f"👤 *Name:* {name}\n"
        f"🏢 *Organisation:* {organisation}\n"
        f"📍 *Location:* {place}\n"
        f"📐 *Size:* {size}\n"
        f"⭐ *Interest Level:* {interest_level}\n"
        f"📝 *Summary:* {summary}\n"
    )

    print("Sending message to Slack channel...")

    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        print("Message sent: ", response["ts"])
    except SlackApiError as e:
        print("Error sending message: ", e.response["error"])
