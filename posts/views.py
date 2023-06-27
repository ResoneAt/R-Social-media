from django.shortcuts import render, redirect
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
    ...


class DeletePostView(View):
    ...


class DetailPostView(View):
    ...


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

