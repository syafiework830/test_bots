from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.core.teams import TeamsInfo
from botbuilder.schema import ChannelAccount
from msal import ConfidentialClientApplication
import requests

class EchoBot(ActivityHandler):
    def __init__(self):
        self.client_id = "4de31d44-c36c-4c94-9357-56c12acc1810"
        self.client_secret = "Vni8Q~~bqEijtbvTYBJNsM9WJu3vhfxYCKR37a-t"
        TENANT_ID = "155fd083-bd9d-49e1-8d00-2cc96af8a37b"
        self.authority = f'https://login.microsoftonline.com/{TENANT_ID}'
        self.scope = ["https://graph.microsoft.com/.default"]

        # Initialize attributes to None
        self.name = None
        self.email = None
        self.office = None

    async def msal_app(self, turn_context: TurnContext):
        msal_app = ConfidentialClientApplication(
            client_credential=self.client_secret,
            client_id=self.client_id,
            authority=self.authority
        )

        result = msal_app.acquire_token_silent(
            scopes=self.scope,
            account=None
        )

        if not result:
            result = msal_app.acquire_token_for_client(
                scopes=self.scope
            )
        
        if "access_token" in result:
            access_token = result["access_token"]
        else:
            raise Exception("No Access Token Found")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.get(
            url="https://graph.microsoft.com/v1.0/users",
            headers=headers
        )

        user_info = response.json()
        self.name = user_info["value"][0]["givenName"]
        self.email = user_info["value"][0]["mail"]
        self.office = user_info["value"][0]["officeLocation"]

        await turn_context.send_activity(f"User Info: Name: {self.name}, Office: {self.office}, Email: {self.email}")

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

    async def on_message_activity(self, turn_context: TurnContext):
        user_name = turn_context.activity.from_property.name
        await turn_context.send_activity(f"Welcome - {user_name}")

        # Call _show_member_details and await its completion
        await self._show_member_details(turn_context)

        return await turn_context.send_activity(
            MessageFactory.text(f"The Bot: {turn_context.activity.text}")
        )

    async def _show_member_details(self, turn_context: TurnContext):
        try:
            user_id = turn_context.activity.from_property.id
            print(f"Attempting to retrieve details for user ID: {user_id}")
            member = await TeamsInfo.get_member(turn_context, user_id)
            member_details = f"Name: {member.name}, Email: {member.email if member.email else 'No email available'}"
            
            # Fetch additional details using msal_app
            await self.msal_app(turn_context)
            additional_details = f"Name: {self.name}, Email: {self.email}, Office: {self.office}"
            
            await turn_context.send_activity(f"Member details: {member_details}\nAdditional details: {additional_details}")
        except Exception as e:
            # Check if attributes exist before using them in the error message
            name = self.name if self.name else "N/A"
            office = self.office if self.office else "N/A"
            email = self.email if self.email else "N/A"

            await turn_context.send_activity(f"Error retrieving member details: {str(e)}\n\nName: {name}, Office: {office}, Email: {email}")
            print(f"Error retrieving member details: {str(e)}")

    async def _show_all_members(self, turn_context: TurnContext):
        try:
            team_id = turn_context.activity.conversation.id
            members = await TeamsInfo.get_team_members(turn_context, team_id)
            print(members)
            member_names = [member.name if member.name else "Unnamed Member" for member in members]
            await turn_context.send_activity(f"Team members: {', '.join(member_names)}")
        except Exception as e:
            await turn_context.send_activity(f"Error retrieving team members: {str(e)}")
            print(f"Error retrieving team members: {str(e)}")
