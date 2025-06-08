# KODE
In this repository there the task what I found in LinkedIn post for job opprtunity
Membership Management Addon
Overview
The Membership Management custom addon enhances the functionality of your Odoo server by introducing advanced partner management features. This addon adds new user groups for controlling partner visibility and a custom field to track membership renewals.
Installation

Install the membership_management custom addon on your Odoo server.
Navigate to the Apps module.
Search for the app using the technical name membership_management.
Install the app.

Features
New User Groups
The addon introduces two new user groups under Users & Companies > Groups:

View Approved Partners Only [Regular Users]  

Restricts visibility in the Contacts module and partner selection fields (e.g., in Sales, Invoices, Purchases, and other views) to partners with the Approved state only.


View All Members [Manager]  

Grants access to all partners in the Contacts module and partner selection fields, regardless of their state (Draft, Approved, or Blacklisted).  
Allows managers to modify the state of contacts directly from the Contacts view.



New Field: Last Renewal Date

A new field, Last Renewal Date, is added to the Contact form view.  
This field automatically stores the date and time of the latest confirmed sales quotation created using the Renewal quotation template.  
Purpose: Tracks the most recent membership renewal date for each contact based on confirmed sales orders.

Usage

Assign the appropriate user group (View Approved Partners Only or View All Members) to users based on their roles.
Ensure the Renewal quotation template is configured correctly in the Sales module to enable tracking of the Last Renewal Date for contacts.

