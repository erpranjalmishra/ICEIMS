# Role-Based Access Control (RBAC) System - ICEIMS 2026

## Overview
The admin dashboard now implements role-based access control to restrict access based on user permissions.

## Permission System

### Admin Roles
Defined in `conference/models.py` - `AdminRole` model:

1. **Super Administrator** - Full access to everything
2. **Content Administrator** - Manage tracks, attractions, maintenance
3. **Blog Administrator** - Manage blog posts, comments, categories
4. **Event Administrator** - Manage general events
5. **Schedule Administrator** - Manage conference schedule
6. **Speaker Administrator** - Manage speakers
7. **Committee Administrator** - Manage committee members
8. **Notice Administrator** - Manage notices and announcements
9. **Timeline Administrator** - Manage timeline and status updates
10. **User Administrator** - Manage users and permissions
11. **Read Only Administrator** - View-only access

### Permissions

Each role can have the following permissions:

- `can_access_dashboard` - Access to admin dashboard
- `can_manage_users` - Create, edit, delete users
- `can_manage_content` - Manage tracks, attractions, general content
- `can_manage_blog` - Manage blog posts, comments, categories
- `can_manage_events` - Manage events
- `can_manage_schedule` - Manage conference schedule
- `can_manage_speakers` - Manage speakers
- `can_manage_committee` - Manage committee members
- `can_manage_notices` - Manage notices and announcements
- `can_manage_timeline` - Manage timeline and status updates
- `can_export_data` - Export data
- `can_view_logs` - View activity logs

## Implementation

### 1. Template-Level Access Control

**Dashboard (`templates/admin/dashboard.html`)**:
- Each management section is wrapped with permission checks
- Only displays sections the user has access to

Example:
```django
{% if user.is_superuser or user.profile.has_permission('can_manage_blog') %}
<div class="management-section">
    <h5>Blog Management</h5>
    <!-- Blog management links -->
</div>
{% endif %}
```

**Navigation Menu (`templates/base.html`)**:
- Dropdown menu items filtered by permissions
- Only shows links to sections user can access

### 2. View-Level Access Control

**Permission Check Functions** (`conference/views.py`):
```python
def has_blog_permission(user):
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile:
        return user.profile.has_permission('can_manage_blog')
    return False
```

**View Decorators**:
```python
@login_required
@user_passes_test(has_blog_permission)
def blog_list(request):
    # View code
```

### 3. Model-Level Permission Checks

**UserProfile Model**:
```python
def has_permission(self, permission):
    if self.user.is_superuser:
        return True
    if not self.admin_role or not self.admin_role.is_active:
        return False
    return getattr(self.admin_role, permission, False)
```

## How to Assign Permissions

### Option 1: Create Admin User with Role
1. Go to Admin Dashboard → User Management
2. Click "Create User"
3. Fill in user details
4. Select an Admin Role from dropdown
5. Check "Admin User" - allows access to custom admin dashboard
6. Check "Staff Status" - required for Django admin panel access
7. Save

### Option 2: Edit Existing User
1. Go to Admin Dashboard → User Management
2. Click "Edit" on the user
3. Change Admin Role as needed
4. Update permissions checkboxes if superuser

### Option 3: Fix Staff Status (For Login Issues)
1. Go to Admin Dashboard → User Management
2. Click "Fix Staff Status" button (yellow warning button)
3. Review users without staff status
4. Click "Grant Staff Status" to fix

## Staff Status Issue Resolution

**Problem**: Users created without "Staff Status" checkbox cannot login to Django admin panel

**Solution**:
1. **For New Users**: The "Staff Status" checkbox is now checked by default in user creation form
2. **For Existing Users**: Use the "Fix Staff Status" utility in User Management
3. **Manual Fix**: Edit user and check the "Staff Status" checkbox

## Permission Matrix

| Role | Blog | Notice | Timeline | Schedule | Speaker | Committee | Content | Users |
|------|------|--------|----------|----------|---------|-----------|---------|-------|
| Super Admin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Blog Admin | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Notice Admin | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Timeline Admin | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Schedule Admin | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Speaker Admin | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Committee Admin | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Content Admin | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| User Admin | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Read Only | View | View | View | View | View | View | View | ❌ |

## Testing Permissions

1. Create a test user with "Blog Admin" role
2. Login as that user
3. Verify:
   - ✅ Can see Blog Management section
   - ✅ Can access blog list, create, edit
   - ❌ Cannot see Notice Management
   - ❌ Cannot see Timeline Management
   - ❌ Cannot see User Management
   - ❌ Getting 403/redirect when trying to access unauthorized URLs directly

## Security Notes

1. **Superusers bypass all permission checks** - Be careful who has superuser access
2. **Staff status required for Django admin** - Without it, users cannot login to `/admin/`
3. **Admin user status required for custom dashboard** - Without it, users cannot access `/admin-panel/`
4. **URL-level protection** - Views check permissions even if user knows the URL
5. **Template-level hiding** - Menu items hidden for unauthorized users

## Troubleshooting

### User cannot login to Django admin
- Check if `is_staff = True`
- Use "Fix Staff Status" utility
- Edit user manually and check "Staff Status"

### User sees all menu items despite limited role
- Check if user has `is_superuser = True`
- Check if user has a UserProfile assigned
- Check if user has an active Admin Role assigned

### User gets 403 error on authorized pages
- Check if Admin Role is active (`is_active = True`)
- Check if specific permission is checked for that role
- Check if user's profile is linked to the role

## Future Enhancements

1. Add granular permissions (view vs. edit vs. delete)
2. Add permission groups for easier management
3. Add audit trail for permission changes
4. Add permission inheritance
5. Add custom permission creation
