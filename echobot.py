from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.core.teams import TeamsInfo
from botbuilder.schema import ChannelAccount

class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def _show_members(self, turn_context: TurnContext):
        try:
            user_id = turn_context.activity.from_property.id
            print(f"Attempting to retrieve details for user ID: {user_id}")
            member = await TeamsInfo.get_member(turn_context, user_id)
            await turn_context.send_activity(f"Member details: {member}")
        except Exception as e:
            await turn_context.send_activity(f"Error retrieving member details: {str(e)}")
            print(f"Error retrieving member details: {str(e)}")

    async def _show_all_members(self, turn_context: TurnContext):
        try:
            team_id = turn_context.activity.conversation.id
            members = await TeamsInfo.get_team_members(turn_context, team_id)
            member_names = [member.name for member in members]
            await turn_context.send_activity(f"Team members: {', '.join(member_names)}")
        except Exception as e:
            await turn_context.send_activity(f"Error retrieving team members: {str(e)}")
            print(f"Error retrieving team members: {str(e)}")

    async def on_message_activity(self, turn_context: TurnContext):
        # Call _show_members and await its completion
        await  self._show_all_members(turn_context)
        
        return await turn_context.send_activity(
            MessageFactory.text(f"The Bot: {turn_context.activity.text}")
        )
