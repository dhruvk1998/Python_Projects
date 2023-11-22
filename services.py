import requests
import json

class LeadMapper:
    @staticmethod
    def map(constants, body):
        """Maps the given body to a list of leads using the given constants."""
        leads = []
        for constant in constants:
            lead = {}
            lead["Schema"] = constant.get("Schema")
            lead["Value"] = LeadMapper.get_value(body, constant.get("Mapping Key"))
            leads.append(lead)
        return leads

    @staticmethod
    def get_value(body, keys):
        """Gets the value of the given key from the given body."""
        value = body
        for key in keys:
            value = value.get(key)
            if value is None:
                break
        return value

class ActivityMapper:
    @staticmethod
    def map(event_code, lead_id, constants, body):
        """Maps the given body to an activity using the given constants."""
        activity = {}
        activity["RelatedProspectId"] = lead_id
        activity["ActivityEvent"] = event_code
        fields = []
        for constant in constants:
            field = {}
            field["SchemaName"] = constant.get("Schema")
            field["Value"] = LeadMapper.get_value(body, constant.get("Mapping Key"))
            fields.append(field)
        activity["Fields"] = fields
        return activity

class Services:
    def __init__(self):
        self.https = requests

    def activity_handler(self, event_code, body, constants):
        """Creates an activity for the given body using the given constants."""
        lead_presence = None
        if event_code == 230:
            response = self.https.get("https://api.example.com/activities/search", params={"order_id": body["order_id"]})
            activities = json.loads(response.content)
            if activities["List"]:
                lead_presence = self.https.get("https://api.example.com/leads/search", params={"email": activities["List"][0]["mx_Custom_65"]})
                lead_presence = json.loads(lead_presence.content)
                if lead_presence:
                    activity = ActivityMapper.map(event_code, lead_presence[0]["ProspectID"], constants, body)
                    response = self.https.post("https://api.example.com/activities", json=activity)
                    created_activity = json.loads(response.content)
                    return created_activity
        else:
            if "email" in body:
                lead_presence = self.https.get("https://api.example.com/leads/search", params={"email": body["email"]})
                lead_presence = json.loads(lead_presence.content)
            else:
                raise Exception("No email in the data")

            if lead_presence:
                activity = ActivityMapper.map(event_code, lead_presence[0]["ProspectID"], constants, body)
                response = self.https.post("https://api.example.com/activities", json=activity)
                created_activity = json.loads(response.content)
                return created_activity
            else:
                raise Exception("No lead found with the given email")

    def services(self, body, query_string):
        """Routes the given body to the appropriate service based on the query string."""
        if query_string["type"] == "CustomerCreation":
            leads = LeadMapper.map(customerMap, body)
            leads.append(
                {
                    "Schema": "Source",
                    "Value": "Ozokart",
                }
            )
            response = self.https.post("https://api.example.com/leads", json=leads)
            captured_lead = json.loads(response.content)
            return {"CapturedLeadResponse": captured_lead}
        elif query_string["type"] == "CheckoutCreation":
            return self.activity_handler(225, body, checkoutCreation)
        elif query_string["type"] == "CartCreation":
            return self.activity_handler(223, body, cartCreation)
        elif query_string["type"] == "CartUpdation":
            return self.activity_hand
