# Admin Guide - Dynamic FAQ, Guidelines & Awards

## Admin Access

### Admin Login
- **URL**: http://127.0.0.1:8000/admin/
- **Username**: Your superuser username
- **Password**: Your superuser password

---

## FAQ Management

### FAQ Categories
- **List**: http://127.0.0.1:8000/admin/conference/faqcategory/
- **Add New**: http://127.0.0.1:8000/admin/conference/faqcategory/add/

Fields:
- Name (required)
- Slug (auto-generated from name)
- Description
- Icon (choose from 10 options)
- Display Order (for sorting)
- Is Active (show/hide category)

### FAQ Questions
- **List**: http://127.0.0.1:8000/admin/conference/faq/
- **Add New**: http://127.0.0.1:8000/admin/conference/faq/add/

Fields:
- Category (select from dropdown)
- Question (required)
- Answer (rich text)
- Priority (High/Medium/Low)
- Is Published (show/hide)
- Is Featured (highlight on page)
- Display Order
- Tags (comma-separated)
- Keywords (for search)
- AI Enhanced (checkbox)
- AI Response (optional)

### AI Conversations
- **List**: http://127.0.0.1:8000/admin/conference/aiconversation/
- View AI chatbot interactions and analytics

---

## Guidelines Management

### Guideline Categories
- **List**: http://127.0.0.1:8000/admin/conference/guidelinecategory/
- **Add New**: http://127.0.0.1:8000/admin/conference/guidelinecategory/add/

Fields:
- Title (required)
- Slug (auto-generated)
- Description
- Icon (choose from 10 options: file, book, list, clipboard, etc.)
- Color (hex code like #667eea)
- Display Order
- Is Active

### Guidelines
- **List**: http://127.0.0.1:8000/admin/conference/guideline/
- **Add New**: http://127.0.0.1:8000/admin/conference/guideline/add/

Fields:
- Category (select from dropdown)
- Title (required)
- Slug (auto-generated)
- Short Description
- Content (rich HTML text)
- Content Type (Text, Checklist, Steps, Tips, Requirements)
- Additional Info
- Downloadable File (optional PDF/DOC)
- External Link (optional URL)
- Video URL (optional YouTube/Vimeo)
- Is Important (badge)
- Is Published (show/hide)
- Is Featured (highlight on page)
- Display Order

**Inline Checklist Items**: Add checklist items directly in the guideline form

---

## Awards Management

### Award Categories
- **List**: http://127.0.0.1:8000/admin/conference/awardcategory/
- **Add New**: http://127.0.0.1:8000/admin/conference/awardcategory/add/

Fields:
- Name (required)
- Slug (auto-generated)
- Category Type (Paper, Presentation, Poster, Student, Research, Innovation, Service, Special)
- Description
- Icon (choose from icons)
- Color (hex code)
- Prize Details
- Eligibility Criteria
- Display Order
- Is Active
- Show on Homepage

### Awards
- **List**: http://127.0.0.1:8000/admin/conference/award/
- **Add New**: http://127.0.0.1:8000/admin/conference/award/add/

Fields:
- Category (select from dropdown)
- Title (required)
- Slug (auto-generated)
- Description
- Winner Name
- Winner Affiliation
- Winner Photo (upload)
- Winner Bio
- Winning Work Title
- Winning Work Description
- Prize Amount
- Sponsored By
- Nomination Start/End Dates
- Announcement Date
- Status (Upcoming, Open, Closed, Announced)
- Is Featured
- Year
- Display Order

**Inline Award Criteria**: Add evaluation criteria with percentage weights

### Past Winners
- **List**: http://127.0.0.1:8000/admin/conference/pastwinner/
- **Add New**: http://127.0.0.1:8000/admin/conference/pastwinner/add/

Fields:
- Award Name
- Year
- Winner Information
- Work Details
- Display Order
- Is Featured

---

## Quick Start Guide

### 1. Create FAQ Categories
1. Go to http://127.0.0.1:8000/admin/conference/faqcategory/add/
2. Create categories like:
   - General Information
   - Registration & Fees
   - Paper Submission
   - Travel & Accommodation

### 2. Add FAQs
1. Go to http://127.0.0.1:8000/admin/conference/faq/add/
2. Select a category
3. Enter question and answer
4. Set priority to High for important questions
5. Check "Is Published" and optionally "Is Featured"
6. Save

### 3. Create Guideline Categories
1. Go to http://127.0.0.1:8000/admin/conference/guidelinecategory/add/
2. Create categories like:
   - Paper Format
   - Submission Process
   - Presentation Guidelines
   - Camera Ready Instructions

### 4. Add Guidelines
1. Go to http://127.0.0.1:8000/admin/conference/guideline/add/
2. Select category and content type
3. For "Checklist" type, add checklist items at the bottom
4. Upload PDFs, add links, or embed videos
5. Mark important guidelines with "Is Important" flag

### 5. Create Award Categories
1. Go to http://127.0.0.1:8000/admin/conference/awardcategory/add/
2. Create categories like:
   - Best Paper Award
   - Best Presentation
   - Young Researcher Award

### 6. Add Awards
1. Go to http://127.0.0.1:8000/admin/conference/award/add/
2. Fill in award details and timeline
3. Set status to "Open" for active nominations
4. Add winner details once announced
5. Set status to "Announced" and upload winner photo

---

## Frontend Pages

- **FAQ Page**: http://127.0.0.1:8000/faq/
  - AI Chatbot integration
  - Category filtering
  - Search functionality
  - Helpful voting

- **Guidelines Page**: http://127.0.0.1:8000/guidelines/
  - Category filtering
  - Search functionality
  - Featured guidelines section
  - Download PDFs, watch videos, visit external links

- **Awards Page**: http://127.0.0.1:8000/awards/
  - Coming soon (template needs to be created)

- **Admin Dashboard**: http://127.0.0.1:8000/admin/dashboard/
  - Statistics overview
  - Quick access links
  - Management sections

---

## Tips & Best Practices

### FAQ
- Use clear, concise questions
- Provide comprehensive answers
- Tag FAQs for better search
- Mark important FAQs as "Featured"
- Set appropriate priority levels

### Guidelines
- Use content types appropriately:
  - **Text**: General information
  - **Checklist**: Step-by-step requirements
  - **Steps**: Sequential instructions
  - **Tips**: Helpful suggestions
  - **Requirements**: Mandatory criteria
- Upload downloadable PDFs for detailed guides
- Add videos for complex processes
- Use "Is Important" for critical guidelines

### Awards
- Keep nomination timelines accurate
- Update status as nominations progress:
  - **Upcoming**: Not yet open
  - **Open**: Accepting nominations
  - **Closed**: Past deadline
  - **Announced**: Winner declared
- Add past winners for credibility
- Include evaluation criteria for transparency

---

## Troubleshooting

### Can't access admin?
- Make sure server is running: `python manage.py runserver`
- Verify you're logged in as a superuser
- Check URL is correct: http://127.0.0.1:8000/admin/

### Changes not showing?
- Make sure "Is Published" / "Is Active" is checked
- Check display order settings
- Clear browser cache (Ctrl+F5)

### Slugs not auto-generating?
- Slugs are auto-generated from title/name
- Save the form once to generate
- You can manually edit if needed

---

## Database Models Created

Migration 0028 created these tables:
- conference_faqcategory
- conference_faq
- conference_aiconversation
- conference_guidelinecategory
- conference_guideline
- conference_guidelinechecklist
- conference_awardcategory
- conference_award
- conference_awardcriteria
- conference_pastwinner

All models are fully migrated and ready to use!
