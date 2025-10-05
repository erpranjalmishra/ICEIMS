# Hierarchy Levels Management Guide

## Overview
The Hierarchy Levels system allows you to create custom categories for organizing your committee members on the conference website.

## Features

### ✨ Fully Customizable
- **Add unlimited levels**: You're not limited to 8 levels - add as many as you need
- **Custom names**: Change "Level 1" to "Chief Patron", "Advisory Board", or any name you prefer
- **Flexible ordering**: Control the display order by assigning level numbers

### 📋 How to Use

#### Adding a New Hierarchy Level
1. Go to **Admin Panel** → **Conference** → **Hierarchy Levels**
2. Click **"Add Hierarchy Level"** button
3. Fill in the details:
   - **Level Number**: Choose a unique number (e.g., 9, 10, 15, 20, etc.)
     - Lower numbers appear first on the website
     - Use gaps (like 10, 20, 30) to allow future insertions
   - **Level Name**: Give it a meaningful name
     - Examples: "Advisory Board", "International Committee", "Student Volunteers"
   - **Description**: Optional - explain the role of this level
   - **Is Active**: Keep checked to display on the website
4. Click **Save**

#### Editing Existing Levels
1. Go to **Hierarchy Levels** list
2. Click directly on the **level name** to edit it inline
3. Or click the level number to open the full edit form
4. Changes appear immediately on the website

#### Assigning Members to Levels
1. Go to **Committee Members**
2. When adding/editing a member, select the **Hierarchy Level** from the dropdown
3. All active levels will be available in the dropdown
4. Members will be automatically grouped by their level on the website

#### Deleting Levels
- You can only delete levels that have **no members assigned**
- If you try to delete a level with members, you'll get an error
- Solution: First reassign all members to a different level, then delete

### 💡 Best Practices

#### Level Numbering Strategy
- **Use gaps**: Number levels as 10, 20, 30 instead of 1, 2, 3
  - This allows you to insert new levels between existing ones later
  - Example: If you have levels 10 and 20, you can add level 15 later

#### Common Level Examples
```
Level 1  → Chief Patron
Level 2  → Patrons
Level 3  → Honorary Chairs
Level 4  → Conference Chairs
Level 5  → Program Committee
Level 6  → Organizing Committee
Level 7  → Technical Committee
Level 8  → Advisory Board
Level 9  → International Committee
Level 10 → Publicity Committee
Level 15 → Student Volunteers
```

#### Organizing Tips
1. **Top positions first**: Use lower numbers (1-5) for leadership positions
2. **Supporting roles middle**: Use middle numbers (6-15) for committee roles
3. **Volunteers/Support last**: Use higher numbers (16+) for support staff

### 🔧 Technical Details

#### How It Works
- Each hierarchy level is stored in the database with a unique number
- Committee members are assigned to levels via the `hierarchy_level` field
- The website automatically groups members by their level
- Levels are displayed in ascending order (1, 2, 3, etc.)

#### Display Behavior
- **Level Header**: Shows the custom name (e.g., "Chief Patron" instead of "Level 1")
- **Member Cards**: Display under their respective level sections
- **Inactive Levels**: Hidden from the public website but still in the database

### ❓ FAQ

**Q: Can I have more than 8 levels?**
A: Yes! Add as many as you need. There's no limit.

**Q: What happens if I change a level name?**
A: The change appears immediately on the website for all members in that level.

**Q: Can I reorder levels?**
A: Yes, by changing the level numbers. Lower numbers appear first.

**Q: What if I want to temporarily hide a level?**
A: Uncheck "Is Active" instead of deleting it. This hides it from the website.

**Q: Can I skip numbers (like 1, 3, 5)?**
A: Yes! You don't need consecutive numbers. Use any unique numbers you prefer.

**Q: What's the best way to insert a new level between existing ones?**
A: If you numbered with gaps (10, 20, 30), just use a number in between (e.g., 15).
   If you used consecutive numbers (1, 2, 3), you'll need to renumber existing levels.

### 🚀 Quick Start Examples

#### Example 1: Adding an Advisory Board
```
Level Number: 9
Level Name: Advisory Board
Description: Distinguished advisors to the conference
Is Active: ✓
```

#### Example 2: Adding International Committee
```
Level Number: 10
Level Name: International Committee
Description: Representatives from international institutions
Is Active: ✓
```

#### Example 3: Adding Student Volunteers
```
Level Number: 20
Level Name: Student Volunteers
Description: Student support team
Is Active: ✓
```

## Support
If you need help or have questions, please contact the technical team.

---
*Last Updated: October 2025*
