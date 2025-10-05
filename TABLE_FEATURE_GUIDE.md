# Guidelines Table Feature - Admin Guide

## Overview
The Guidelines system now supports **Excel and CSV table imports** with automatic parsing and beautiful display on the public page. Admins can upload table files, and they will be automatically converted to interactive web tables.

---

## How to Add Tables to Guidelines

### Step 1: Access Guideline Admin
1. Go to: http://127.0.0.1:8000/admin/conference/guideline/
2. Click "Add Guideline" or edit an existing guideline

### Step 2: Select Content Type
- In the "Basic Information" section, set **Content Type** to **"Table Data"**

### Step 3: Upload Table File
In the "Table Data (Excel/CSV Import)" section:

1. **Table Title** (optional): Enter a descriptive title for your table
   - Example: "Submission Deadlines", "Registration Fees", "Paper Format Requirements"

2. **Table File**: Upload your Excel (.xlsx, .xls) or CSV file
   - Supported formats: `.xlsx`, `.xls`, `.csv`
   - Maximum file size: Based on your server settings (usually 10MB)

3. **Table Has Header**: Check this if the first row contains column names
   - ✅ Checked: First row will be used as table headers
   - ❌ Unchecked: Auto-generate headers as "Column 1", "Column 2", etc.

4. **Table Preview**: After saving, you'll see a preview of your table with:
   - First 5 rows displayed
   - Total row and column count
   - Styled headers with gradient background

### Step 4: Add Additional Content (Optional)
- **Content**: Add text description or introduction for the table
- **Additional Info**: Add notes, warnings, or important information
- **Downloadable File**: Upload the original file for users to download

### Step 5: Display Settings
- ✅ **Is Published**: Make the guideline visible
- ✅ **Is Featured**: Show in featured section
- ✅ **Is Important**: Highlight with special badge

---

## Creating Excel/CSV Files

### Excel File Format (.xlsx, .xls)
```
| Category       | Deadline       | Extension Fee |
|----------------|----------------|---------------|
| Early Bird     | Jan 15, 2026   | $150          |
| Regular        | Feb 28, 2026   | $200          |
| Late           | Mar 31, 2026   | $250          |
```

**Tips for Excel:**
- Keep headers in Row 1
- Use simple, clear column names
- Avoid merged cells
- Remove empty rows/columns
- Use only the first sheet (others are ignored)

### CSV File Format (.csv)
```
Category,Deadline,Extension Fee
Early Bird,Jan 15 2026,$150
Regular,Feb 28 2026,$200
Late,Mar 31 2026,$250
```

**Tips for CSV:**
- Use comma (,) as delimiter
- Put headers in first row
- Enclose text with commas in quotes
- Use consistent formatting

---

## Example Tables for Conference

### 1. Registration Fees Table
**File**: registration_fees.xlsx

| Category        | Early Bird   | Regular | Late    |
|-----------------|--------------|---------|---------|
| Student         | $100         | $150    | $200    |
| Academician     | $200         | $250    | $300    |
| Industry        | $300         | $350    | $400    |
| Virtual         | $50          | $75     | $100    |

### 2. Important Dates Table
**File**: important_dates.xlsx

| Event                  | Date          | Status    |
|------------------------|---------------|-----------|
| Paper Submission Opens | Nov 1, 2025   | Completed |
| Submission Deadline    | Jan 31, 2026  | Open      |
| Notification           | Mar 15, 2026  | Upcoming  |
| Camera Ready           | Apr 15, 2026  | Upcoming  |
| Conference Dates       | May 20-22     | Upcoming  |

### 3. Paper Format Requirements
**File**: paper_format.xlsx

| Element       | Requirement              | Page Limit |
|---------------|--------------------------|------------|
| Font          | Times New Roman 11pt     | -          |
| Margins       | 1 inch all sides         | -          |
| Full Paper    | IEEE format              | 6-8 pages  |
| Short Paper   | IEEE format              | 4-6 pages  |
| Poster        | IEEE format              | 2-4 pages  |

### 4. Track Information
**File**: conference_tracks.xlsx

| Track Name               | Chair                | Topics                |
|--------------------------|----------------------|-----------------------|
| Machine Learning         | Dr. John Smith       | AI, ML, Deep Learning |
| IoT & Embedded Systems   | Dr. Jane Doe         | IoT, Sensors, Edge    |
| Cloud Computing          | Dr. Bob Wilson       | Cloud, Distributed    |
| Cybersecurity            | Dr. Alice Johnson    | Security, Privacy     |

---

## Public Page Display

### How Tables Appear to Users

1. **Table Container**:
   - White background with rounded corners
   - Soft shadow for depth
   - Responsive design (scrollable on mobile)

2. **Table Header** (if table_title is set):
   - Purple gradient icon
   - Table title in bold
   - Row × Column count

3. **Data Table**:
   - **Header Row**: Purple gradient background with white text
   - **Data Rows**: Alternating gray/white backgrounds
   - **Hover Effect**: Rows highlight and slightly scale on hover
   - **First Column**: Bold and purple colored (acts as row header)

4. **Download Button**: 
   - If table_file is uploaded, users can download the original file
   - Purple gradient button at bottom-right

### Features:
- ✅ Responsive (scrolls horizontally on small screens)
- ✅ Beautiful gradient styling
- ✅ Smooth hover animations
- ✅ Auto-parsed from Excel/CSV
- ✅ Download original file option

---

## Admin Interface Features

### List View:
- **Table Status Column**: Shows "📊 X rows × Y cols" badge if table exists
- Filter by content type to see all table guidelines
- Edit/delete table guidelines

### Edit View:
- **Table Preview**: See first 5 rows of your table
- **Auto-parsing**: Upload triggers automatic parsing
- **Success Message**: "Table parsed successfully: X rows, Y columns"
- **Error Handling**: Clear error messages if file can't be parsed

---

## Troubleshooting

### "Error parsing table file"
**Causes:**
- File is corrupted
- Unsupported file format
- Empty file
- Excel file with complex formulas

**Solutions:**
- Re-save Excel file as .xlsx
- Ensure file has data
- Remove complex formulas, keep only values
- Try converting to CSV

### Table not displaying
**Checks:**
1. Content Type = "Table Data"
2. Table file uploaded successfully
3. "Is Published" is checked
4. table_data field has JSON data (check in preview)

### Headers showing as "Column 1, Column 2"
**Solution:**
- Check "Table Has Header" checkbox
- Ensure first row contains text headers (not empty)
- Re-save the guideline

### Table too wide on mobile
**This is normal behavior:**
- Tables become horizontally scrollable on small screens
- Users can swipe left/right to see all columns
- Consider creating separate mobile-friendly tables for very wide data

---

## Best Practices

### 1. Keep Tables Simple
- ✅ 3-10 columns ideal
- ✅ 5-50 rows recommended
- ❌ Avoid 100+ rows (creates very long tables)
- ❌ Avoid 20+ columns (hard to read)

### 2. Use Clear Headers
- Use descriptive column names
- Keep headers short (1-3 words)
- Use title case: "Registration Fee" not "registration fee"

### 3. Format Data Consistently
- Use same date format throughout
- Use consistent currency symbols
- Align numbers properly in Excel

### 4. Provide Context
- Add description in "Content" field explaining the table
- Use "Additional Info" for important notes
- Mark as "Important" for critical tables

### 5. Offer Downloads
- Always upload the original file in "Downloadable File"
- Users may want to analyze data in Excel
- Provides backup if web display has issues

---

## Example Workflow

1. **Prepare Excel File**:
   ```
   Create registration_fees.xlsx with headers in row 1
   ```

2. **Create Guideline**:
   - Title: "Registration Fees for ICEIMS 2026"
   - Content Type: "Table Data"
   - Short Description: "Conference registration fee structure for different categories"

3. **Upload Table**:
   - Table Title: "Registration Fee Structure"
   - Table File: Upload registration_fees.xlsx
   - Table Has Header: ✅ Checked

4. **Add Context**:
   - Content: "Early bird discounts available until January 31, 2026. All fees in USD."
   - Additional Info: "Group discounts available for 5+ registrations. Contact us for details."

5. **Set Display Options**:
   - Is Published: ✅
   - Is Important: ✅ (if it's critical information)
   - Is Featured: ✅ (to show in featured section)

6. **Save and Preview**:
   - Check table preview in admin
   - Visit public page: http://127.0.0.1:8000/guidelines/
   - Verify table displays correctly

---

## API & JSON Structure

When a table file is uploaded, it's converted to JSON format:

```json
{
    "headers": ["Category", "Early Bird", "Regular", "Late"],
    "rows": [
        ["Student", "$100", "$150", "$200"],
        ["Academician", "$200", "$250", "$300"],
        ["Industry", "$300", "$350", "$400"]
    ],
    "total_rows": 3,
    "total_columns": 4
}
```

This JSON is stored in the `table_data` field and rendered as HTML on the public page.

---

## Support

For issues or questions:
- Check server logs for error details
- Verify file format is .xlsx, .xls, or .csv
- Contact system administrator

---

**Last Updated**: October 6, 2025  
**Feature Version**: 1.0  
**Django Version**: 5.2.6
