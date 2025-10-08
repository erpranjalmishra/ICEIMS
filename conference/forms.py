from django import forms
from .models import ConferenceRegistration, RegistrationCategory


class ConferenceRegistrationForm(forms.ModelForm):
    """Form for conference registration"""
    
    # Add terms acceptance
    accept_terms = forms.BooleanField(
        required=True,
        label='I accept the terms and conditions'
    )
    
    class Meta:
        model = ConferenceRegistration
        fields = [
            'category', 'title', 'first_name', 'last_name', 'email', 'phone',
            'alternate_phone', 'organization', 'designation', 'department',
            'country', 'state', 'city', 'address', 'postal_code',
            'is_ieee_member', 'ieee_membership_id',
            'is_student', 'student_id', 'student_id_document',
            'has_paper', 'paper_id', 'paper_title', 'additional_pages',
            'payment_method', 'transaction_id', 'payment_receipt',
            'payment_notes', 'special_requirements', 'accommodation_required'
        ]
        
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'title': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXXXXXXX',
                'required': True
            }),
            'alternate_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional alternate phone'
            }),
            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'University/Company name',
                'required': True
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Professor/Student/Engineer etc.',
                'required': True
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Department name'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country',
                'required': True
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Complete address'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal/ZIP code'
            }),
            'is_ieee_member': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'ieeeCheck'
            }),
            'ieee_membership_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'IEEE Membership Number',
                'id': 'ieeeMembershipId'
            }),
            'is_student': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'studentCheck'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Student ID Number',
                'id': 'studentId'
            }),
            'student_id_document': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png',
                'id': 'studentIdDoc'
            }),
            'has_paper': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'paperCheck'
            }),
            'paper_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Paper ID from submission system',
                'id': 'paperId'
            }),
            'paper_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full title of your paper',
                'id': 'paperTitle'
            }),
            'additional_pages': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 4,
                'value': 0,
                'id': 'additionalPages'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Transaction/Reference ID'
            }),
            'payment_receipt': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'payment_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Any additional payment information'
            }),
            'special_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dietary restrictions, accessibility needs, etc.'
            }),
            'accommodation_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Only show active categories
        self.fields['category'].queryset = RegistrationCategory.objects.filter(is_active=True)
        
        # Make certain fields not required initially
        self.fields['ieee_membership_id'].required = False
        self.fields['student_id'].required = False
        self.fields['student_id_document'].required = False
        self.fields['paper_id'].required = False
        self.fields['paper_title'].required = False
        self.fields['payment_method'].required = False
        self.fields['transaction_id'].required = False
        self.fields['payment_receipt'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate IEEE membership
        if cleaned_data.get('is_ieee_member') and not cleaned_data.get('ieee_membership_id'):
            self.add_error('ieee_membership_id', 'IEEE Membership ID is required for IEEE members.')
        
        # Validate student information
        if cleaned_data.get('is_student'):
            if not cleaned_data.get('student_id'):
                self.add_error('student_id', 'Student ID is required for student registration.')
            if not cleaned_data.get('student_id_document'):
                self.add_error('student_id_document', 'Student ID document is required for verification.')
        
        # Validate paper information
        if cleaned_data.get('has_paper'):
            if not cleaned_data.get('paper_id'):
                self.add_error('paper_id', 'Paper ID is required if you are submitting a paper.')
            if not cleaned_data.get('paper_title'):
                self.add_error('paper_title', 'Paper title is required if you are submitting a paper.')
        
        # Validate additional pages
        additional_pages = cleaned_data.get('additional_pages', 0)
        if additional_pages < 0:
            self.add_error('additional_pages', 'Additional pages cannot be negative.')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Calculate payment amount
        instance.payment_amount = instance.calculate_total_amount()
        instance.currency = instance.category.currency
        
        # Set initial status
        if not instance.pk:
            instance.status = 'pending'
        
        if commit:
            instance.save()
        
        return instance
