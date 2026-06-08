import sys
import logging
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
logger = logging.getLogger(__name__)

mcp = FastMCP("SMS Server", host="0.0.0.0", port=8000)

# Approved contacts list (single source of truth)
APPROVED_CONTACTS = [
    {"name": "Kwame", "phone": "0248174302"},
    {"name": "Ama", "phone": "0244567890"},
    {"name": "Kofi", "phone": "0201234567"},
]


@mcp.tool()
async def get_contacts() -> str:
    """Get the list of approved contacts we can send SMS to."""
    try:
        logger.debug("Fetching contacts list...")
        logger.info("Contacts fetched successfully!")
        return str(APPROVED_CONTACTS)
    except Exception as err:
        logger.error(f"Failed to fetch contacts: {err}")
        return "Sorry, could not fetch contacts."


@mcp.tool()
async def send_sms(phone_number: str, message: str) -> str:
    """Send an SMS to an approved contact only."""
    try:
        # Check if phone number is approved
        approved_numbers = [c["phone"] for c in APPROVED_CONTACTS]

        if phone_number not in approved_numbers:
            logger.warning(f"Rejected SMS to unapproved number: {phone_number}")
            return f"Sorry, {phone_number} is not in the approved contacts list. SMS not sent."

        # If approved, send the SMS
        logger.debug(f"Sending SMS to approved contact {phone_number}...")
        result = f"SMS sent to {phone_number}: {message}"
        logger.info("SMS sent successfully!")
        return result

    except Exception as err:
        logger.error(f"SMS failed: {err}")
        return "Sorry, SMS could not be sent."


@mcp.resource("contacts://list")
async def contacts_resource() -> str:
    """A list of approved contacts we can send SMS to."""
    logger.debug("Contacts resource requested...")
    return str(APPROVED_CONTACTS)


@mcp.prompt()
async def send_sms_prompt(phone_number: str, message: str) -> str:
    """Template for sending an SMS. Use this when user wants to send a message."""
    return f"Please send an SMS to {phone_number} with this message: {message}"


if __name__ == "__main__":
    logger.info("Starting SMS MCP Server on HTTP...")
    mcp.run(transport="streamable-http")




