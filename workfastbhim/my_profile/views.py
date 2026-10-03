from django.shortcuts import render
from gallery.models import GalleryImage, Comment
from django import forms
from django.shortcuts import redirect

def my_profile_dashboard(request):
    return render(request, 'my_profile_dashboard.html')

def about_page(request):
    return render(request, 'about_page.html')

def my_gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'my_gallery.html', {'images': images})

def add_image_comment(request, image_id):
    image = GalleryImage.objects.filter(id=image_id).first()
    #comments = Comment.objects.filter(image=image)
    class CommentForm(forms.ModelForm):
        class Meta:
            model = Comment
            fields = ['author', 'text']

    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.image = image
            new_comment.save()
            form = CommentForm()
    return redirect('my_profile:my_gallery')
    #return render(request, 'gallery.html', {'image': image, 'comments': comments, 'form': form})










