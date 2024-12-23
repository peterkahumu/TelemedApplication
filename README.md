# Welcome to Telemed Application

Telemed is an application that aims to enable patients get access to healthcare despite their geographical differences with Doctors. The application aims to track realtime vitals of the patients, and enable them share them with their loved ones, medical personell or any other relevant parties.

Below is a brief introduction/explanation of the features in the system:
***
## 1. Apps Present

The application has the following applications:
1. ***Authentication:*** Handles user authentication tasks, including:
    - Registration: Enables the user to set up their personal details and roles (Patient, Doctor or admin.)
        - Each user can have only one profile at a time.
        - Logic: *All Doctors can be patients (thus they have access to all activities that can be done by a patent) but not all patients are Doctors.*
        - An email is sent to the provided email to verify the account. The user cannot login to the account if their email is not verified.
    - Activation of the created account.
    - Login: Using their email or password.
    - Reset Password: Allow the users to request for an email to reset their password.
    - Set Password: Allow the user to set a new password using the link sent to them via their email.
    - Log out a user.
2. ***Core***: Handle the user profile. Enables the user to:
    - Serves the landing page (index.html) and the Dashboard (home.html, after the user has logged in.)
    - View their own profile
    - View the profile of another user
    - Update their own profile
    - Update or delete their own profile images.
    - Change the password.
3. ***Appointments***: Handles all matter regarding appointments.
    - Enables the user to book appointments.

4.***Patients***: Allows the patients to view the appointments they've made.
