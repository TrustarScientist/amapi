This API serves as the computing foundation for the client's system, managing user roles, assets, and transactions.

🚀 Key Features
Role-Based Access Control (RBAC): Differentiates between Admin (Owner/Manager) and Buyer user roles.

Item Management: CRUD operations for digital assets (e.g., social media accounts). Write access (Create/Update/Delete) is restricted to the Admin role.

User Management: Buyers can manage their own profile; Admins can manage all users.

Wallet System: Includes a wallet_balance for each Buyer to facilitate purchases.

Secure Authentication: Uses JWT (JSON Web Tokens) via djangorestframework-simplejwt.

⚙️ Local Setup and Installation
Prerequisites
Python 3.11+

PostgreSQL

Virtual Environment tool (venv recommended)

Setup Steps
Clone the Repository:

Bash

git clone [YOUR_REPO_URL]
cd amapi
Install Dependencies:

Bash

# Setup and activate virtual environment

python -m venv .venv
source .venv/bin/activate

# Install Python dependencies

pip install -r requirements.txt
Configure Environment Variables: Create a .env file and define the following: SECRET_KEY, and all necessary PostgreSQL variables (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT).

Database Initialization:

Bash

# Apply migrations

python manage.py makemigrations
python manage.py migrate
Create Initial Roles and Admin: The system requires the Admin and Buyer roles to exist.

Create Roles: Run in the Django shell to ensure Admin and Buyer are in the database.

Bash

python manage.py shell

# >>> from users.models import Role

# >>> Role.objects.get_or_create(name='Admin')

# >>> Role.objects.get_or_create(name='Buyer')

# >>> exit()

Create Superuser: Run python manage.py createsuperuser. After creation, log into the Django Admin (/admin/) and manually set the user's Role to Admin.

Run the Server:

Bash

python manage.py runserver
The API will be available at http://127.0.0.1:8000/.

🌐 API Endpoints Specification
The base path for all API routes is /api/v1/.

1. Authentication
   Path Method Purpose Notes
   /auth/register/ POST Creates a new user. Default role is Buyer.
   /auth/token/ POST Login. Returns access, refresh, and the user_info object (includes id, role, is_admin, wallet_balance).
   /auth/token/refresh/ POST Renew the access token. Requires refresh token.

Export to Sheets

2. Item & Category Management
   Path Method Role Restriction Purpose
   /items/ GET All List all available items for sale.
   /items/ POST Admin Only Create a new item listing.
   /items/{pk}/ PUT/PATCH Admin Only Update an existing item.
   /items/{pk}/ DELETE Admin Only Delete an item listing.
   /categories/ GET All List all defined item categories.

Export to Sheets

3. User & Profile Management
   Path Method Role Restriction Purpose
   /users/ GET Admin Only List all users in the system.
   /users/{pk}/ GET All Retrieve a specific user's details.
   /users/{pk}/ PUT/PATCH Owner or Admin Update a user profile. Buyers can only update their own account.
   /users/{pk}/ DELETE Owner or Admin Delete a user account. Buyers can only delete their own account.

Export to Sheets

4. Wallet and Transactions
   These endpoints are used by Buyers to manage funds and complete purchases.

Path Method Role Restriction Purpose Request Body Example
/wallet/topup/ POST Buyer Only Top-Up Wallet: Adds funds to the user's wallet_balance (simulating a successful payment). {"amount": 50.00}
/purchase/item/ POST Buyer Only Purchase: Executes the transaction (checks funds, debits wallet, marks item as sold). {"item_id": 42}
