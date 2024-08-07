### Installation
```bash
$ pip install django-contact-message
```

#### `settings.py`
```python
INSTALLED_APPS+=['django_contact_message']
```

#### `migrate`
```bash
$ python manage.py migrate
```

### Features
+   `Message` model
+   admin

### Models
model|table|columns/fields
-|-|-
`Message`|`django_contact_message`|`id`,`user`,`email`,`subject`,`message`,`created_at`

### Examples
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django_contact_message.models import Message

class View(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        Message(
            user=request.user,
            subject=request.POST['subject'],
            email=request.POST['email'],
            message=request.POST['message'],
        ).save()
```

