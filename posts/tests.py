from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import PostModel, CommentModel, LikeModel, ReportPostModel


class PostModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.image = SimpleUploadedFile(
            'test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        self.post = PostModel.objects.create(
            user=self.user,
            body='Test post',
            location='Test location',
            image=self.image,
            is_active=True,
            slug='test-post'
        )

    def test_post_model_str(self):
        self.assertEqual(str(self.post), 'testuser@example.com')

    def test_post_model_comment_count(self):
        CommentModel.objects.create(
            author=self.user,
            body='Test comment',
            post=self.post
        )
        self.assertEqual(self.post.comment_count(), 1)

    def test_post_model_like_count(self):
        LikeModel.objects.create(
            user=self.user,
            post=self.post
        )
        self.assertEqual(self.post.like_count(), 1)

    def test_post_model_get_comments_list(self):
        comment = CommentModel.objects.create(
            author=self.user,
            body='Test comment',
            post=self.post
        )
        comments_list = self.post.get_comments_list()
        self.assertIn(comment, comments_list)

    def test_post_model_get_liker_list(self):
        liker = get_user_model().objects.create_user(
            username='testliker',
            email='testliker@example.com',
            password='testpass'
        )
        LikeModel.objects.create(
            user=liker,
            post=self.post
        )
        liker_list = self.post.get_liker_list()
        self.assertIn(liker, liker_list)

    def test_post_model_get_report_list(self):
        reporter = get_user_model().objects.create_user(
            username='testreporter',
            email='testreporter@example.com',
            password='testpass'
        )
        report = ReportPostModel.objects.create(
            user=reporter,
            post=self.post,
            body='Test report'
        )
        report_list = self.post.get_report_list()
        self.assertIn(report, report_list)

    def test_post_model_delete(self):
        self.post.delete()
        self.assertFalse(self.post.is_active)
        self.assertTrue(self.post.is_deleted)
        self.assertIsNotNone(self.post.deleted_at)

    def test_post_model_get_absolute_url(self):
        url = reverse('posts:detail_post', kwargs={'slug': self.post.slug})
        self.assertEqual(self.post.get_absolute_url(), url)


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.post = PostModel.objects.create(
            user=self.user,
            body='Test post'
        )
        self.comment = CommentModel.objects.create(
            author=self.user,
            body='Test comment',
            post=self.post
        )

    def test_comment_model_str(self):
        self.assertEqual(str(self.comment), 'testuser - Test comment - Test post')

    def test_comment_model_replies(self):
        reply = CommentModel.objects.create(
            user=self.user,
            post=self.post,
            parent=self.comment,
            body='Test reply'
        )
        replies = self.comment.get_replies()
        self.assertTrue(self.comment.has_replies())
        self.assertIn(reply, replies)
        self.assertTrue(reply.is_reply)

    def test_comment_model_replies_count(self):
        reply = CommentModel.objects.create(
            user=self.user,
            post=self.post,
            parent=self.comment,
            body='Test reply'
        )
        self.assertEqual(self.comment.get_replies().count(), 1)


class LikeModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.post = PostModel.objects.create(
            user=self.user,
            body='Test post'
        )
        self.like = LikeModel.objects.create(
            user=self.user,
            post=self.post
        )

    def test_like_model_str(self):
        self.assertEqual(str(self.like), 'testuser - Test post')

    def test_like_model_unique_together_constraint(self):
        with self.assertRaises(Exception) as context:
            LikeModel.objects.create(
                user=self.user,
                post=self.post
            )
        self.assertTrue('unique constraint' in str(context.exception).lower())

    def test_like_model_delete(self):
        self.assertEqual(self.post.likes.count(), 1)
        self.like.delete()
        self.assertEqual(self.post.likes.count(), 0)

class ReportPostModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.post = PostModel.objects.create(
            user=self.user,
            body='Test post'
        )
        self.report = ReportPostModel.objects.create(
            user=self.user,
            post=self.post,
            body='Test report'
        )

    def test_report_post_model_str(self):
        self.assertEqual(str(self.report), 'testuser - Test post')

    def test_report_post_model_delete(self):
        self.assertEqual(self.post.reports.count(), 1)
        self.report.delete()
        self.assertEqual(self.post.reports.count(), 0)