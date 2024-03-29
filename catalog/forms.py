from django import forms
from django.utils import timezone
#from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe

User = get_user_model()

from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

class RegisterForm(UserCreationForm):

  email = forms.EmailField()

  class Meta:
	  model = User
	  fields = ["username", "email", "password1", "password2"]



class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':'40','class': 'form-control'}))
    sender = forms.EmailField(widget=forms.TextInput(attrs={'size':'40','class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    copy = forms.BooleanField(required=False)

class LoginForm(forms.Form):

	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Login'
		self.fields['password'].label = 'Parol'

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		if not User.objects.filter(username=username).exists():
			raise forms.ValidationError('Bu adda istifadəçi artıq mövcuddur!')
		user = User.objects.get(username=username)
		if user and not user.check_password(password):
			raise forms.ValidationError('Parol yalnisdir!')

class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password_check = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'password_check',
			'first_name',
			'last_name',
			'email',
			#'phone',
			#'brity'
		]

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'İstifadəçi adı'
		self.fields['password'].label = 'Şifrə'
		self.fields['password'].help_text = 'Şifrə daxil edin'
		self.fields['password_check'].label = 'Şifrəni təkrar edin'
		self.fields['first_name'].label = 'Ad'
		self.fields['last_name'].label = 'Soyad'
		self.fields['email'].label = 'Email adresiniz'
		

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']
		email = self.cleaned_data['email']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('Bu adda istifadəçi artıq mövcuddur!')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Bu email adres ilə istifadəçi artıq mövcuddur!')
		if password != password_check:
			raise forms.ValidationError('Təkrar şifrə düzgün daxil edilməyib. Yenidən yoxla!')







class OrderForm(forms.Form):

	name = forms.CharField()
	last_name = forms.CharField(required=False)
	phone = forms.CharField()
	buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "Özünüz yaxınlaşacaqsınız?"),("delivery", "Çatdırılma")]))
	date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
	address = forms.CharField(required=False)
	comments = forms.CharField(widget=forms.Textarea, required=False)


	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = 'Ad'
		self.fields['last_name'].label = 'Soyad'
		self.fields['phone'].label = 'Əlaqə nömrəsi'
		self.fields['phone'].help_text = 'Xahiş edirik işlək nömrə qeyd edin.'
		self.fields['buying_type'].label = 'Məhsulu necə əldə edəcəksiniz?'
		self.fields['address'].label = 'Çatdırılma ünvanı'
		self.fields['address'].help_text = '*Şəhəri mütləq qeyd edin!'
		self.fields['comments'].label = 'Sifarişlə bağlı qeyd'
		self.fields['date'].label = 'Çatdırılma tarixi'
		self.fields['date'].help_text = 'Sifariş təstiq olunduqdan sonra 30 dəqiqə ərzində sizinlə əlaqə saxlanılacaq!'

class ClickForms(forms.ModelForm):
	class Meta:
		model = Click
		fields = ['product','phone','name','note',]


class LoginsForm(forms.Form):
  email = forms.EmailField(
    label='Email',
    widget=forms.EmailInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "Email"
      }
    )
  )
  password = forms.CharField(
    widget=forms.PasswordInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "password"
      }
    )
  )

  def __init__(self, request, *args, **kwargs):
    self.request = request
    super(LoginsForm, self).__init__(*args, **kwargs)

  def clean(self):
    request = self.request
    data = self.cleaned_data
    email  = data.get("email")
    password  = data.get("password")
    qs = User.objects.filter(email=email)
    if qs.exists():
      not_active = qs.filter(is_active=False)
      if not_active.exists():
        link = reverse("accounts:resend-activation")
        reconfirm_msg = """Go to <a href='{resend_link}'>
        resend confirmation email</a>.""".format(resend_link=link)
        confirm_email = EmailActivation.objects.filter(email=email)
        is_confirmable = confirm_email.confirmable().exists()
        if is_confirmable:
          msg1 = "Please check your email to confirm your account or " + reconfirm_msg.lower()
          raise forms.ValidationError(mark_safe(msg1))
        email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
        if email_confirm_exists:
          msg2 = "Email not confirmed. " + reconfirm_msg
          raise forms.ValidationError(mark_safe(msg2))
        if not is_confirmable and not email_confirm_exists:
          raise forms.ValidationError("This user is inactive.")
    user = authenticate(request, username=email, password=password)
    if user is None:
      raise forms.ValidationError("Invalid credentials")
    login(request, user)
    self.user = user
    return data


class RegisterForm(forms.ModelForm):
  email = forms.EmailField(
    label='Email',
    widget=forms.EmailInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "Email"
      }
    )
  )
  full_name = forms.CharField(
    label='Full Name',
    widget=forms.TextInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "Full Name"
      }
    )
  )
  password1 = forms.CharField(
    label='Password',
    widget=forms.PasswordInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "password"
      }
    )
  )
  password2 = forms.CharField(
    label='Password confirmation',
    widget=forms.PasswordInput(
      attrs={
        "class": "form-control mb-4",
        "placeholder": "Password confirmation"
      }
    )
  )

  class Meta:
    model = User
    fields = ('email', 'full_name', )

  def clean_password2(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError("Passwords don't match")
    return password2

  def save(self, commit=True):
    user = super(RegisterForm, self).save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    user.is_active = False
    if commit:
      user.save()
    return user


class HistoryForms(forms.ModelForm):
  class Meta:
    model = HistoryProducts
    fields = ['user', 'product',]

class ProductComment(forms.ModelForm):
  class Meta:
    model = Comment
    fields = '__all__'