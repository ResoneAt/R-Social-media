from django.shortcuts import render, redirect, get_object_or_404
from .models import ImagePostModel, PostModel
from django.views.generic import View
from .forms import CreatePostForm, ImagePostForm
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.utils.text import slugify
from django.contrib import messages


class CreatePostView(View):
    form_class = CreatePostForm
    ImageFormSet = inlineformset_factory(PostModel, ImagePostModel, form=ImagePostForm,
                                         formset=BaseInlineFormSet, extra=1, max_num=10,
                                         validate_max=True, can_delete=True)
    template_name = 'posts/create_post.html'

    def get(self, request):
        form = self.form_class()
        image_formset = self.ImageFormSet()
        return render(request, self.template_name, {'form': form, 'image_formset': image_formset})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        image_formset = self.ImageFormSet(request.POST, request.FILES)

        if form.is_valid() and image_formset.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.slug = slugify(form.cleaned_data['body'][:30])
            post.save()

            for image_form in image_formset.cleaned_data:
                if image_form:
                    image = image_form['image']
                    alt = image_form['alt']
                    ImagePostModel.objects.create(post=post, image=image, alt=alt)
            messages.success(request, 'your post is create successfully', 'success')
            return redirect('accounts:user_profile', request.user.id)

        return render(request, self.template_name, {'form': form, 'image_formset': image_formset})


class EditPostView(View):
    form_class = CreatePostForm
    ImageFormSet = inlineformset_factory(PostModel, ImagePostModel, form=ImagePostForm,
                                         formset=BaseInlineFormSet, extra=1, max_num=10,
                                         validate_max=True, can_delete=True)
    template_name = 'posts/edit_post.html'

    def get(self, request, post_id):
        post = get_object_or_404(PostModel, id=post_id, user=request.user)
        form = self.form_class(instance=post)
        image_formset = self.ImageFormSet(instance=post)
        return render(request, self.template_name, {'form': form, 'image_formset': image_formset})

    def post(self, request, post_id):
        post = get_object_or_404(PostModel, id=post_id, user=request.user)
        form = self.form_class(request.POST, request.FILES, instance=post)
        image_formset = self.ImageFormSet(request.POST, request.FILES, instance=post)

        if form.is_valid() and image_formset.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(form.cleaned_data['body'][:30])
            post.save()

            for image_form in image_formset.cleaned_data:
                if image_form:
                    image = image_form['image']
                    alt = image_form['alt']
                    if 'id' in image_form and image_form['id']:
                        image_post = ImagePostModel.objects.get(id=image_form['id'], post=post)
                        image_post.image = image
                        image_post.alt = alt
                        image_post.save()
                    else:
                        ImagePostModel.objects.create(post=post, image=image, alt=alt)

            messages.success(request, 'Your post has been updated successfully', 'success')
            return redirect('posts:detail', post_id=post.id)

        return render(request, self.template_name, {'form': form, 'image_formset': image_formset})
    ...


class DeletePostView(View):
    def post(self, request, *args, **kwargs):
        post = PostModel.objects.get(pk=kwargs['pk'])
        if post.user != request.user:
            messages.error(request, 'You are not authorized to delete this post.')
            return redirect(post.get_absolute_url())
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('accounts:user_profile')


class DetailPostView(View):
    template_name = 'posts/detail_post.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(PostModel, slug=kwargs['slug'])
        comments = post.get_comments_list()
        images = post.post_images()
        movies = post.post_movies()
        context = {'post': post, 'comments': comments, 'images': images, 'movies': movies}
        return render(request, self.template_name, context)



class LikePostView(View):
    ...


class DislikePostView(View):
    ...


class SentCommentView(View):
    ...


class EditCommentView(View):
    ...


class DeleteCommentView(View):
    ...


class ReportPostView(View):
    ...


class SavePostToWishList(View):
    ...

