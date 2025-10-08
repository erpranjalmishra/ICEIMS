# Registration Fees Table Management

## Overview
The Registration Fees Table feature allows administrators to manage the registration fees displayed on the registration page through the Django admin panel.

## Features

### Admin Panel Management
- **Location**: `/admin/conference/registrationfeestable/`
- **Full CRUD**: Create, Read, Update, Delete fees table rows
- **Bulk Actions**: Activate, Deactivate, Highlight, Unhighlight rows
- **Reordering**: Use `display_order` field to control row sequence

### Fields

#### Participant Information
- **Participant Type**: Select from predefined types (Indian/Foreign, Author/Student/Attendee)
- **Display Name**: Custom name shown in the table
- **Notes**: Optional additional information (e.g., "Valid student ID required")

#### Fees (Text Fields)
- **Early Bird IEEE**: Early bird rate for IEEE members (e.g., `₹6000` or `$200`)
- **Early Bird Non-IEEE**: Early bird rate for non-IEEE members
- **Regular IEEE**: Regular rate for IEEE members
- **Regular Non-IEEE**: Regular rate for non-IEEE members

#### Display Settings
- **Is Active**: Show/hide this row in the fees table
- **Is Highlighted**: Apply yellow background to emphasize this row
- **Display Order**: Numeric value for sorting (lower numbers appear first)

## How to Use

### 1. Add New Fee Row
1. Go to `/admin/conference/registrationfeestable/`
2. Click "Add Registration Fees Table Row"
3. Fill in all fields:
   - Select participant type
   - Enter display name
   - Enter fees (include currency symbol: ₹ or $)
   - Set display order
   - Check "Is active" to show immediately
4. Click "Save"

### 2. Edit Existing Row
1. Click on the row name in the admin list
2. Update any fields
3. Click "Save"

### 3. Reorder Rows
- Set `display_order` field to change sequence
- Lower numbers appear first
- Example: 1, 2, 3, 4... or 10, 20, 30, 40...

### 4. Highlight Important Rows
- Check `is_highlighted` to add yellow background
- Good for student rates or special offers

### 5. Bulk Actions
- Select multiple rows using checkboxes
- Choose action from dropdown:
  - "Activate selected rows"
  - "Deactivate selected rows"
  - "Highlight selected rows"
  - "Remove highlight from selected rows"
- Click "Go"

## Populate Sample Data

Run this command to create sample fees data:

```bash
python manage.py populate_fees_table
```

This creates 10 sample rows with realistic fees for:
- Indian Authors (Academia/Industry)
- Indian Student Authors
- Indian Attendees
- Foreign Authors
- Foreign Student Authors
- And more...

## Template Integration

The fees table automatically displays on the registration page at `/registration/`.

### Features:
- Responsive Bootstrap table
- Highlighted rows (yellow background)
- Notes display under category names
- Fallback to old category-based table if fees_table_rows is empty

### Table Structure:
```
| Category          | Early Bird        | Regular           |
|                   | IEEE | Non-IEEE   | IEEE | Non-IEEE   |
|-------------------|------|------------|------|------------|
| Row 1             | ₹6000| ₹7000      | ₹7000| ₹8000      |
| Row 2 (highlight) | ₹4500| ₹5500      | ₹5500| ₹6500      |
```

## Tips

### Currency Formatting
- **Indian Rupees**: Use `₹` symbol (₹6000, ₹7500)
- **US Dollars**: Use `$` symbol ($200, $250)
- **Other**: Any text works (€150, £100, etc.)

### Display Order Best Practices
- Use increments of 10: 10, 20, 30, 40...
- This allows easy insertion between rows later
- Example: Insert new row with order 15 between 10 and 20

### Notes Field
- Keep notes concise
- Use for important conditions
- Examples:
  - "Valid student ID required"
  - "Maximum 2 papers per author"
  - "Includes conference kit"

### Highlighting
- Highlight student rates to attract students
- Highlight early bird to encourage early registration
- Don't highlight too many rows (loses impact)

## Admin Screenshots Locations

To access:
1. **Main List**: `/admin/conference/registrationfeestable/`
2. **Add New**: `/admin/conference/registrationfeestable/add/`
3. **Edit Row**: `/admin/conference/registrationfeestable/{id}/change/`

## Database Model

**Model**: `RegistrationFeesTable`
**Table**: `conference_registrationfeestable`

Fields:
- `id` (Auto)
- `participant_type` (CharField, 100)
- `display_name` (CharField, 200)
- `early_bird_ieee` (CharField, 50)
- `early_bird_non_ieee` (CharField, 50)
- `regular_ieee` (CharField, 50)
- `regular_non_ieee` (CharField, 50)
- `is_active` (BooleanField)
- `display_order` (IntegerField)
- `is_highlighted` (BooleanField)
- `notes` (CharField, 500)
- `created_at` (DateTimeField)
- `updated_at` (DateTimeField)

## Migration

Migration file: `conference/migrations/0048_registrationfeestable.py`

To apply:
```bash
python manage.py migrate
```

## Related Files

- **Model**: `conference/models.py` (RegistrationFeesTable)
- **Admin**: `conference/admin.py` (RegistrationFeesTableAdmin)
- **View**: `conference/views.py` (registration function)
- **Template**: `templates/registration.html`
- **Command**: `conference/management/commands/populate_fees_table.py`

## Support

For issues or questions, contact the development team.
