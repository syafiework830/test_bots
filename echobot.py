from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.core.teams import TeamsInfo
from botbuilder.schema import ChannelAccount
from botbuilder.schema.teams import TeamsChannelAccount
from typing import List

class EchoBot(ActivityHandler):
   class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        return await turn_context.send_activity(
            MessageFactory.text(f"Echo: {turn_context.activity.text}")
        )
