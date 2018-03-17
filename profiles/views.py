from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.shortcuts import Http404
User = get_user_model()


class ProfileDetailView(DetailView):
    queryset = User.objects.filter(is_active=True)
    template_name = 'profiles/profile_detail.html'

    def get_object(self):
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username)
