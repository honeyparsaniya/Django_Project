from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        min_length=3,
        label="Username",
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "username",
                "class": "login-input",
                "placeholder": "Enter your username",
                "autocomplete": "username",
            }
        )
    )

    contact_number = forms.CharField(
        max_length=15,
        min_length=10,
        label="Contact Number",
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "contact",
                "class": "login-input",
                "placeholder": "Enter your contact number",
                "type": "tel",
                "autocomplete": "tel",
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if not username:
            raise forms.ValidationError("Username is required.")

        return username

    def clean_contact_number(self):
        contact_number = self.cleaned_data["contact_number"].strip()

        if not contact_number.isdigit():
            raise forms.ValidationError(
                "Contact number must contain only numbers."
            )

        if len(contact_number) != 10:
            raise forms.ValidationError(
                "Contact number must be exactly 10 digits."
            )

        return contact_number


class OTPForm(forms.Form):

    otp = forms.CharField(
        max_length=6,
        min_length=6,
        label="Enter OTP",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "otp-input",
                "placeholder": "Enter 6-digit OTP",
                "maxlength": "6",
                "autocomplete": "one-time-code",
            }
        )
    )

    def clean_otp(self):
        otp = self.cleaned_data["otp"].strip()

        if not otp.isdigit():
            raise forms.ValidationError(
                "OTP must contain only numbers."
            )

        if len(otp) != 6:
            raise forms.ValidationError(
                "OTP must be exactly 6 digits."
            )

        return otp

# =========================================================
# PROFILE UPDATE FORM
# =========================================================

class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "contact_number",
            "role",
            "read_terms_and_conditions",
            "image",
        ]

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email",
                }
            ),

            "contact_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "read_terms_and_conditions": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        # Get current logged-in user
        user = kwargs.get("instance")

        super().__init__(*args, **kwargs)

        if user:

            # -------------------------------------------------
            # Username
            # -------------------------------------------------

            if user.username:
                self.fields["username"].disabled = True


            # -------------------------------------------------
            # Contact Number
            # -------------------------------------------------

            if user.contact_number:
                self.fields["contact_number"].disabled = True


            # -------------------------------------------------
            # Role
            # -------------------------------------------------

            # User should NOT be able to change role
            self.fields["role"].disabled = True


            # -------------------------------------------------
            # Email
            # -------------------------------------------------

            if user.email:
                self.fields["email"].disabled = True


            # -------------------------------------------------
            # Profile Image
            # -------------------------------------------------

            if user.image:
                self.fields["image"].disabled = True


            # -------------------------------------------------
            # Terms & Conditions
            # -------------------------------------------------

            if user.read_terms_and_conditions:
                self.fields[
                    "read_terms_and_conditions"
                ].disabled = True