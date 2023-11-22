import datetime
import requests

# Define the working hours
start_time = datetime.time(9, 0)  # 9:00 AM
end_time = datetime.time(18, 0)  # 6:00 PM

# Function to check if the current time is within working hours
def within_working_hours():
    current_time = datetime.datetime.now().time()
    return start_time <= current_time <= end_time

# Function to distribute the lead
def distribute_lead(lead, user):
    
    # Replace the following values with your CRM system's API credentials
    CRM_API_URL = "ls.SETTINGS.LS_ACCESS_KEY"
    CRM_API_URL = "ls.SETTINGS.LS_SECRET_KEY"
    CRM_API_TOKEN = "YOUR_CRM_API_TOKEN"
    
    def bulk_update_lead_owner(lead_ids, user_id):
            request = requests.post(
                CRM_API_URL + "/bulk/update",
                headers={"Authorization": "Bearer " + CRM_API_TOKEN},
                json={"lead_ids": lead_ids, "owner_id": user_id},
            )
    
            # Check the response status code to see if the leads were updated successfully.
            if request.status_code == 200:
                print("Leads updated successfully.")
            else:
                print("Error updating leads: " + request.content)
    if __name__ == "__main__":
        # Create a list of lead IDs.
        lead_ids = ["1234567890", "9876543210"]

        # Specify the user ID of the user to assign the leads to.
        user_id = 1234567890

        # Bulk update the lead owner of the leads.
        bulk_update_lead_owner(lead_ids, user_id)
   

# Function to handle lead redistribution
def handle_lead_redistribution(lead, user):
    current_time = datetime.datetime.now().time()
    
    # Check if the current time is within working hours
    if within_working_hours():
        time_limit = datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(hours=6)
        
        # Check if the time limit for updating the lead has passed
        if current_time >= time_limit.time():
            distribute_lead(lead, user)
        else:
            print("Waiting for 6 hours before redistributing the lead...")
    else:
        print("Outside of working hours. Lead redistribution will be handled when the working hours resume.")

# Example usage
lead_id = "ABC123"
assigned_user = "John Doe"

# Simulate lead entry into the system
print(f"New lead {lead_id} entered the system and was assigned to {assigned_user}.")

# Handle lead redistribution
handle_lead_redistribution(lead_id, assigned_user)
