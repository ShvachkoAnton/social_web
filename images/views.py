

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ImageForm
@login_required
def image_create(request):
    if request.method=="POST":
        form=ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            new_item=form.save(commit=False)
            new_item.user=request.user
            new_item.save()
            messages.success(request, 'Изображение было успешно добавлено')
            return redirect(new_item.get_absolute_url())
    else:
        form=ImageCreateForm(data=request.GET)
    return render(request,'images/image/create.html', {'section':'images',
        'form':form})

def image_detail(request,id,slug):
    image=get_object_or_404(Image, id=id, slug=slug)
    return render(request,'images/image/detail.html',{'section': 'images',
'image': image} )


"""class ImageDetail(DetailView):
    model=Image
    template_name='images/image/detail.html'
    context_object_name='image'
    def get_queryset(self):
        return Image.objects.filter(id=self.kwargs.get('id'),slug=self.kwargs['slug'])
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        likes_connected=get_object_or_404(Image, id=self.kwargs['id'],slug=self.kwargs['slug'])
        liked=False
        if likes_connected.users_like.filter(id=self.request.user.id).exists():
            liked=True
        data['number_of_likes']=likes_connected._of_likes()
        data['post_is_liked']=liked
        return data"""

    
"""def ImagePostLike(request,id):
    image=get_object_or_404(Image, id=request.POST.get('image_id'))
    if image.users_like.filter(id=request.user.id).exists():
        image.users_like.remove(request.user)
    else:
        image.users_like.add(request.user)
    return HttpResponseRedirect(reverse('images:detail', args=[self.id, self.slug]))"""


@login_required
@require_POST
def image_like(request):
    image_id=request.POST.get('id')
    action=request.POST.get('action')
    if image_id and action:
        try:
            image=Image.objects.get(id=image_id)
            if action=='лайк':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})

