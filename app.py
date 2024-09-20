import os
from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity, ActivityTypes

# Set the bot credentials
app_id = os.getenv("MicrosoftAppId", "")
app_password = os.getenv("MicrosoftAppPassword", "")
settings = BotFrameworkAdapterSettings(app_id, app_password)
adapter = BotFrameworkAdapter(settings)

# Simple Echo Bot
async def on_message_activity(turn_context: TurnContext):
    if turn_context.activity.type == ActivityTypes.message:
        await turn_context.send_activity(f"You said: {turn_context.activity.text}")

# Handle incoming requests
async def messages(request: web.Request) -> web.Response:
    # Process the incoming activity
    body = await request.json()
    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    # Handle activity type
    if activity.type == ActivityTypes.message:
        await adapter.process_activity(activity, auth_header, on_message_activity)

    return web.Response(status=200)

# Main entry point
app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=os.getenv("PORT", 3978))
