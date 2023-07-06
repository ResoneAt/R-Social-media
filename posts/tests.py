from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import PostModel, CommentModel, LikeModel, ReportPostModel, MoviePostModel


class PostModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpass'
        )
        self.post = PostModel.objects.create(
            user=self.user,
            body='Test body',
            slug='test-post'
        )
        self.comment = CommentModel.objects.create(
            author=self.user,
            body='Test comment',
            post=self.post,
        )
        self.like = LikeModel.objects.create(
            user=self.user,
            post=self.post
        )
        # self.image = ImagePostModel.objects.create(
        #     image='test_image.jpg',
        #     post=self.post,
        #     alt='Test image'
        # )
        self.movie = MoviePostModel.objects.create(
            movie='test_movie.mp4',
            post=self.post
        )
        self.report = ReportPostModel.objects.create(
            user=self.user,
            post=self.post,
            body='Test report'
        )

    def test_post_model(self):
        post = PostModel.objects.get(id=1)
        self.assertEqual(post.slug, 'test-post')
        self.assertEqual(post.comment_count(), 1)
        self.assertEqual(post.like_count(), 1)
        self.assertEqual(post.post_images().count(), 1)
        self.assertEqual(post.post_movies().count(), 1)
        self.assertEqual(post.get_report_list().count(), 1)
        self.assertEqual(str(post), 'test-post')

    def test_comment_model(self):
        comment = CommentModel.objects.get(id=1)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.body, 'Test comment')
        self.assertEqual(comment.post, self.post)
        self.assertEqual(str(comment), 'testuser - Test comment - test-post')

    def test_like_model(self):
        like = LikeModel.objects.get(id=1)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)
        self.assertEqual(str(like), 'test-post-testuser')

    # def test_image_post_model(self):
    #     image = ImagePostModel.objects.get(id=1)
    #     self.assertEqual(image.image, 'test_image.jpg')
    #     self.assertEqual(image.post, self.post)
    #     self.assertEqual(image.alt, 'Test image')
    #     self.assertEqual(str(image), 'Test image')

    def test_movie_post_model(self):
        movie = MoviePostModel.objects.get(id=1)
        self.assertEqual(movie.movie, 'test_movie.mp4')
        self.assertEqual(movie.post, self.post)

    def test_report_post_model(self):
        report = ReportPostModel.objects.get(id=1)
        self.assertEqual(report.user, self.user)
        self.assertEqual(report.post, self.post)
        self.assertEqual(report.body, 'Test report')
        self.assertEqual(str(report), 'test-post - Test report')