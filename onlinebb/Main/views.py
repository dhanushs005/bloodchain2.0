from django.shortcuts import render
from django.http import JsonResponse
from .forms import UserForm, EmergencyForm, ReportForm
from pymongo import MongoClient

# MongoDB connection setup
MONGO_URI = "mongodb+srv://Dhanush:2k22ca005@userdetails.mavp0oq.mongodb.net/?retryWrites=true&w=majority" # Update with your MongoDB URI
DB_NAME = "Users"  # Replace with your database name
USER_COLLECTION = "User"  # Replace with your user collection name
EMERGENCY_COLLECTION = "emergency"  # Replace with your emergency collection name
REPORTS_COLLECTION = "reports"  # The reports collection
# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Home view
def home(request):
    form = UserForm()
    return render(request, 'Main/home.html', {'UserForm': form})
def report(request):
    form3 = ReportForm()
    return render(request, 'Main/report.html',{'ReportForm':form3})
# Emergency view
def emerg(request):
    form2 = EmergencyForm()
    return render(request, 'Main/emergency.html', {'EmergencyForm': form2})

# View donors and emergency data
def view_donors(request):
    blood_group = request.GET.get('blood_group', '').strip()
    district = request.GET.get('district', '').strip()

    # Build MongoDB query based on search parameters
    query = {}
    if blood_group:
        query['blood_group'] = blood_group
    if district:
        query['district'] = district

    # Fetch matching donors and emergency cases
    donors = list(db[USER_COLLECTION].find(query, {"_id": 0}))
    emergency = list(db[EMERGENCY_COLLECTION].find({}, {"_id": 0}))  # Fetch all emergency cases

    context = {
        'donors': donors,
        'emergency': emergency,
    }
    return render(request, 'Main/donors.html', context)

# Save user details
def save_user_details(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            mobile = cleaned_data['mobile']  # Mobile number field from the form

            # Check if the mobile number already exists in the database
            existing_user = db[USER_COLLECTION].find_one({"mobile": mobile})

            if existing_user:
                # If the mobile number exists, return an error
                return JsonResponse({"status": "error", "message": "Mobile number already exists!"})
            else:
                # If the mobile number is unique, save the data
                new_entry = {
                    "name": cleaned_data['name'],
                    "mobile": mobile,
                    "blood_group": cleaned_data['bg'],
                    "gender": cleaned_data['gender'],
                    "district": cleaned_data['dists'],
                    "last_donated_date": str(cleaned_data['last_date'])
                }
                try:
                    # Insert into MongoDB
                    db[USER_COLLECTION].insert_one(new_entry)
                    return JsonResponse({"status": "success", "message": "User details saved successfully!"})
                except Exception as e:
                    return JsonResponse({"status": "error", "message": f"Error saving data: {str(e)}"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid form data!", "errors": form.errors})

    return render(request, 'form.html', {'form': UserForm()})
# Save emergency details
def emergency_details(request):
    if request.method == 'POST':
        form = EmergencyForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            new_entry = {
                "pname": cleaned_data['pname'],
                "pmobile": cleaned_data['pmobile'],
                "bg_needed": cleaned_data['bg_needed'],
                "pgender": cleaned_data['pgender'],
                "units_needed": cleaned_data['units_needed'],
                "hospital_name": cleaned_data['hospital_name'],
                "pdists": cleaned_data['pdists'],
                "urgency_level": cleaned_data['urgency_level']
            }
            try:
                # Insert into MongoDB
                db[EMERGENCY_COLLECTION].insert_one(new_entry)
                return JsonResponse({"status": "success", "message": "Emergency details saved successfully!"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": f"Error saving data: {str(e)}"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid form data!", "errors": form.errors})
    return render(request, 'form.html', {'form': EmergencyForm()})

def updateReport(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            cleaned_data = form.cleaned_data
            mobile = cleaned_data['rmobile']  # Mobile field
            report_type = cleaned_data['report_type']  # Report type field
            description = cleaned_data['description']  # Description field

            new_entry = {
                "mobile": mobile,
                "report_type": report_type,
                "description": description,
            }

            try:
                # Insert into MongoDB
                db[REPORTS_COLLECTION].insert_one(new_entry)
                return JsonResponse({"status": "success", "message": "Report saved successfully!"})
            except Exception as e:
                return JsonResponse({"status": "error", "message": f"Error saving data: {str(e)}"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid form data!", "errors": form.errors})

    # For GET requests, render the ReportForm
    form = ReportForm()
    return render(request, 'form.html', {'form': form})

# def view_reports(request):
#     blood_group = request.GET.get('blood_group', '').strip()
#     district = request.GET.get('district', '').strip()
#
#     # Build MongoDB query based on search parameters
#     query = {}
#     if blood_group:
#         query['blood_group'] = blood_group
#     if district:
#         query['district'] = district
#
#     # Fetch matching donors and emergency cases
#     donors = list(db[USER_COLLECTION].find(query, {"_id": 0}))
#     emergency = list(db[EMERGENCY_COLLECTION].find({}, {"_id": 0}))  # Fetch all emergency cases
#
#     context = {
#         'donors': donors,
#         'emergency': emergency,
#     }
#     return render(request, 'Main/donors.html', context)
