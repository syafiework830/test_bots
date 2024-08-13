from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.core.teams import TeamsInfo
from botbuilder.schema import ChannelAccount
from botbuilder.schema.teams import TeamsChannelAccount
from typing import List

class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            try:
                # Print TurnContext activity for debugging
                print("TurnContext Activity:", turn_context.activity)
                
                # Ensure you have the correct member_id
                print(f"Processing member ID: {member.id}")
                
                # Get member details
                teams_member = await self.get_member(turn_context, member.id)
                
                if teams_member:
                    await turn_context.send_activity(
                        f"Welcome {teams_member.given_name} {teams_member.surname}! "
                        f"Your email is {teams_member.email} and your UPN is {teams_member.user_principal_name}."
                    )
                else:
                    await turn_context.send_activity(
                        f"Welcome {member.name}! We couldn't retrieve your detailed information."
                    )
            except Exception as e:
                print(f"Error processing member: {e}")
                await turn_context.send_activity(
                    f"Welcome {member.name}! An error occurred while retrieving your information."
                )

    async def get_member(self, turn_context: TurnContext, member_id: str) -> TeamsChannelAccount:
        try:
            # Ensure TurnContext and member_id are valid
            print("TurnContext for get_member:", turn_context)
            print(f"Retrieving member with ID: {member_id}")
            
            # Call TeamsInfo.get_member() to get the member details
            member = await TeamsInfo.get_member(turn_context, member_id)
            return member
        except Exception as e:
            # Log and handle the exception if any error occurs
            print(f"Error retrieving member: {e}")
            return None
