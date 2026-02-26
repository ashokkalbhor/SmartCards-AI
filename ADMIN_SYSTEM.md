# Admin System Documentation

## Overview

The SmartCards AI platform now includes a comprehensive admin system with user roles, moderator approval workflow, and edit suggestions for card data. This system ensures data quality and community governance.

## 🔐 Admin Configuration

### Admin Email Setup
The admin system is configured with your email address:
- **Admin Email**: `ashokkalbhor@gmail.com`
- **Location**: `backend/app/core/config.py` in `ADMIN_EMAILS` list

### Role Hierarchy
1. **Normal User** - Can view cards, submit suggestions, request moderator status
2. **Moderator** - Can review and approve edit suggestions
3. **Admin** - Can manage users, approve moderators, full system access

## 🗄️ Database Schema

### New Tables Created

#### `user_roles`
- `id` - Primary key
- `user_id` - Foreign key to users table
- `role_type` - "user", "moderator", "admin"
- `approved_by` - Who approved this role
- `approved_at` - When role was approved
- `status` - "active", "inactive", "pending"

#### `moderator_requests`
- `id` - Primary key
- `user_id` - User requesting moderator status
- `request_reason` - Why they want to be a moderator
- `user_activity_summary` - JSON with activity data
- `status` - "pending", "approved", "rejected"
- `reviewed_by` - Admin who reviewed the request
- `reviewed_at` - When request was reviewed

#### `edit_suggestions`
- `id` - Primary key
- `user_id` - User who submitted suggestion
- `card_master_id` - Card being edited
- `field_type` - "spending_category" or "merchant_reward"
- `field_name` - Name of the field being changed
- `old_value` - Current value
- `new_value` - Proposed new value
- `status` - "pending", "approved", "rejected"
- `suggestion_reason` - Why this change is suggested
- `reviewed_by` - Moderator/admin who reviewed
- `review_notes` - Notes from reviewer

#### `audit_logs`
- `id` - Primary key
- `user_id` - User who performed action (null for system)
- `action_type` - Type of action performed
- `table_name` - Table affected
- `record_id` - ID of affected record
- `old_values` - Previous values (JSON)
- `new_values` - New values (JSON)
- `change_summary` - Human-readable summary

## 🔧 Backend API Endpoints

### Admin Endpoints (`/api/v1/admin/`)

#### Get Admin Info
```http
GET /api/v1/admin/admin-info
```
Returns admin configuration and current user's admin status.

#### Get All Users
```http
GET /api/v1/admin/users?skip=0&limit=100&search=email&role_filter=moderator
```
Returns all users with their role information.

#### Get Moderator Requests
```http
GET /api/v1/admin/moderator-requests?status_filter=pending
```
Returns all moderator requests.

#### Review Moderator Request
```http
PUT /api/v1/admin/moderator-requests/{request_id}
{
  "status": "approved" | "rejected"
}
```
Approve or reject a moderator request.

#### Get Edit Suggestions
```http
GET /api/v1/admin/edit-suggestions?status_filter=pending&field_type=spending_category
```
Returns all edit suggestions.

#### Review Edit Suggestion
```http
PUT /api/v1/admin/edit-suggestions/{suggestion_id}
{
  "status": "approved" | "rejected",
  "review_notes": "Optional notes"
}
```
Approve or reject an edit suggestion.

#### Get Admin Stats
```http
GET /api/v1/admin/stats
```
Returns dashboard statistics for admin.

### Moderator Endpoints (`/api/v1/moderator/`)

#### Get Moderator Info
```http
GET /api/v1/moderator/moderator-info
```
Returns moderator status and permissions.

#### Get Pending Suggestions
```http
GET /api/v1/moderator/edit-suggestions?status_filter=pending
```
Returns edit suggestions for review.

#### Review Suggestion
```http
PUT /api/v1/moderator/edit-suggestions/{suggestion_id}
{
  "status": "approved" | "rejected",
  "review_notes": "Optional notes"
}
```
Review and approve/reject edit suggestions.

#### Get Moderator Stats
```http
GET /api/v1/moderator/stats
```
Returns moderator dashboard statistics.

### User Role Endpoints (`/api/v1/user-roles/`)

#### Request Moderator Status
```http
POST /api/v1/user-roles/request-moderator
{
  "request_reason": "I want to help improve card data quality"
}
```
Submit a request to become a moderator.

#### Get My Moderator Request
```http
GET /api/v1/user-roles/my-moderator-request
```
Check status of your moderator request.

#### Get My Role
```http
GET /api/v1/user-roles/my-role
```
Get current user's role and permissions.

#### Submit Edit Suggestion
```http
POST /api/v1/user-roles/edit-suggestions?card_id=123
{
  "field_type": "spending_category" | "merchant_reward",
  "field_name": "fuel",
  "new_value": "5.0",
  "suggestion_reason": "Updated reward rate"
}
```
Submit an edit suggestion for card data.

#### Get My Suggestions
```http
GET /api/v1/user-roles/my-suggestions?status_filter=pending
```
Get user's own edit suggestions.

#### Get My Suggestions Stats
```http
GET /api/v1/user-roles/my-suggestions/stats
```
Get statistics for user's suggestions.

## 🎯 Core Functions

### Admin Utilities (`backend/app/core/admin.py`)

```python
def is_admin(user: User) -> bool:
    """Check if user is an admin"""
    return user.email in settings.ADMIN_EMAILS

def is_moderator(user: User) -> bool:
    """Check if user is a moderator"""
    return user.role == "moderator" or is_admin(user)

def can_approve_suggestions(user: User) -> bool:
    """Check if user can approve suggestions"""
    return is_moderator(user)

def can_manage_users(user: User) -> bool:
    """Check if user can manage other users"""
    return is_admin(user)
```

## 🔄 Workflow

### Moderator Approval Process
1. User submits moderator request via `/user-roles/request-moderator`
2. System calculates user activity summary
3. Admin reviews request via `/admin/moderator-requests`
4. If approved, user gets moderator role
5. Moderator can now review edit suggestions

### Edit Suggestion Process
1. User submits edit suggestion via `/user-roles/edit-suggestions`
2. System validates card and field exist
3. Moderator reviews suggestion via `/moderator/edit-suggestions`
4. If approved, change is applied to card data
5. Audit log is created for tracking

## 🛡️ Security Features

### Role-Based Access Control
- Admin endpoints require admin email
- Moderator endpoints require moderator role
- User endpoints require authentication

### Audit Logging
- All admin/moderator actions are logged
- Includes old/new values for transparency
- Tracks who performed what action when

### Data Validation
- Field types are validated
- Card existence is verified
- Duplicate suggestions are prevented

## 🚀 Getting Started

### 1. Verify Admin Setup
```bash
cd backend
python3 test_admin_system.py
```

### 2. Test Admin Access
- Login with `ashokkalbhor@gmail.com`
- Access `/api/v1/admin/admin-info`
- Should return admin configuration

### 3. Test Moderator Workflow
- Create a test user
- Submit moderator request
- Login as admin and approve
- Test moderator permissions

## 📊 Monitoring

### Admin Dashboard Stats
- Total users and active users
- Number of moderators
- Pending moderator requests
- Pending edit suggestions
- Recent activity logs

### Moderator Dashboard Stats
- Pending suggestions by type
- Recent reviews performed
- Approval/rejection rates

## 🔧 Configuration

### Adding New Admins
Edit `backend/app/core/config.py`:
```python
ADMIN_EMAILS: List[str] = [
    "ashokkalbhor@gmail.com",
    "newadmin@example.com"  # Add new admin emails
]
```

### Changing Admin Permissions
Modify functions in `backend/app/core/admin.py` to adjust permission logic.

## 🐛 Troubleshooting

### Common Issues

1. **Admin not recognized**
   - Check email in `ADMIN_EMAILS` list
   - Verify user exists in database

2. **Migration failed**
   - Run `python3 -m alembic upgrade head`
   - Check database connection

3. **Endpoints not found**
   - Verify routers are included in `api.py`
   - Check server is running

### Debug Commands
```bash
# Check database tables
sqlite3 smartcards_ai.db ".tables"

# Check admin users
sqlite3 smartcards_ai.db "SELECT * FROM users WHERE email LIKE '%admin%';"

# Check user roles
sqlite3 smartcards_ai.db "SELECT * FROM user_roles;"
```

## 🎉 Success!

The admin system is now fully implemented with:
- ✅ Admin identification via email
- ✅ Moderator approval workflow
- ✅ Edit suggestions for card data
- ✅ Comprehensive audit logging
- ✅ Role-based access control
- ✅ Database migrations applied

You can now manage the platform with full control over who can moderate and what changes are applied to card data! 