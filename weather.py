import httpx
from mcp.server.fastmcp import FastMCP
import asyncio

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"import httpx
from mcp.server.fastmcp import FastMCP
import asyncio
import logging

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def make_nws_request(url: str) -> dict:
    """Helper function to make a request to the NWS API with a timeout."""
    try:
        async with httpx.AsyncClient() as client:
            # Add a timeout of 10 seconds for the API request
            response = await client.get(url, timeout=10, headers={"User-Agent": USER_AGENT})
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"Error during request to {url}: {e}")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred while accessing {url}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return None

def format_alert(feature: dict) -> str:
    """Format the weather alert data."""
    return f"Alert: {feature['properties']['headline']}\nDescription: {feature['properties']['description']}"

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state."""
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    logger.info(f"Fetching weather alerts for state: {state}")
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location."""
    logger.info(f"Fetching weather forecast for coordinates: {latitude}, {longitude}")
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

if __name__ == "__main__":
    # Initialize and run the server
    logger.info("Starting FastMCP server...")
    mcp.run(transport='stdio')
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict:
    """Helper function to make a request to the NWS API with a timeout."""
    try:
        async with httpx.AsyncClient() as client:
            # Add a timeout of 10 seconds for the API request
            response = await client.get(url, timeout=10)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
    except httpx.RequestError as e:
        print(f"Error during request to {url}: {e}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred while accessing {url}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def format_alert(feature: dict) -> str:
    """Format the weather alert data."""
    return f"Alert: {feature['properties']['headline']}\nDescription: {feature['properties']['description']}"

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state."""
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    print(f"Fetching weather alerts for state: {state}")
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location."""
    print(f"Fetching weather forecast for coordinates: {latitude}, {longitude}")
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

if __name__ == "__main__":
    # Initialize and run the server
    print("Starting FastMCP server...")
    mcp.run(transport='stdio')
