from django.shortcuts import render, get_object_or_404
from .models import GalleryImage, Comment
from django import forms
from django.shortcuts import redirect

def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'gallery.html', {'images': images})


def add_image_comment(request, image_id):
    image = get_object_or_404(GalleryImage, pk=image_id)
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
    return redirect('gallery')
    #return render(request, 'gallery.html', {'image': image, 'comments': comments, 'form': form})
