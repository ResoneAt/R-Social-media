from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import RelationModel, FollowRequestModel, ReportUserModel, MessageModel, NotificationModel


class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass'))
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.is_active)

    def test_user_str(self):
        self.assertEqual(str(self.user), 'test@example.com')

    def test_user_following(self):
        user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass2'
        )
        relation = RelationModel(from_user=self.user, to_user=user2)
        relation.save()

        self.assertTrue(self.user.is_following(user2))
        self.assertFalse(self.user.is_followed_by(user2))
        self.assertEqual(self.user.get_following_count(), 1)
        self.assertEqual(self.user.get_follower_count(), 0)

    def test_user_follower(self):
        user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass2'
        )
        relation = RelationModel(from_user=user2, to_user=self.user)
        relation.save()

        self.assertFalse(self.user.is_following(user2))
        self.assertTrue(self.user.is_followed_by(user2))
        self.assertEqual(self.user.get_following_count(), 0)
        self.assertEqual(self.user.get_follower_count(), 1)

    # def test_user_image(self):
    #     image = ImageUserModel.objects.create(
    #         image='test.jpg',
    #         user=self.user,
    #         alt='Test Image'
    #     )
    #
    #     self.assertEqual(str(image), 'Test Image - user : testuser')
    #     self.assertEqual(self.user.profile_images().count(), 1)
    #     self.assertEqual(self.user.main_profile_image(), image)

    def test_user_report(self):
        user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass2'
        )
        report = ReportUserModel.objects.create(
            user=user2,
            user_reported=self.user,
            body='Test report'
        )

        self.assertEqual(str(report), 'testuser - Test report...')
        self.assertEqual(self.user.get_report_post_list().count(), 1)

    def test_user_notification(self):
        notification = NotificationModel.objects.create(
            user=self.user,
            title='Test notification',
            body='Test body'
        )

        self.assertEqual(str(notification), 'Test notification for user testuser')
        self.assertEqual(self.user.notificationmodel_set.count(), 1)

    def test_user_absolute_url(self):
        url = reverse('user_profile', kwargs={'user_id': self.user.pk})
        self.assertEqual(self.user.get_absolute_url(), url)


class RelationModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass1'
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass2'
        )

    def test_relation_creation(self):
        relation = RelationModel(from_user=self.user1, to_user=self.user2)
        relation.save()

        self.assertEqual(str(relation), 'testuser1 follows testuser2')
        self.assertEqual(self.user1.following.count(), 1)
        self.assertEqual(self.user2.follower.count(), 1)


class FollowRequestModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass1'
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass2'
        )

    def test_follow_request_creation(self):
        request = FollowRequestModel(from_user=self.user1, to_user=self.user2)
        request.save()

        self.assertEqual(str(request), 'testuser1 to testuser2 - {}'.format(request.created_at))
        self.assertEqual(self.user1.request_sent.count(), 1)
        self.assertEqual(self.user2.request_receive.count(), 1)


# class ImageUserModelTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             username='testuser',
#             email='test@example.com',
#             password='testpass'
#         )
#         self.image = ImageUserModel.objects.create(
#             image='test.jpg',
#             user=self.user,
#             alt='Test Image'
#         )
#
#     def test_image_creation(self):
#         self.assertEqual(str(self.image), 'Test Image - user : testuser')
#         self.assertEqual(self.image.user, self.user)
#
#     def test_image_user_relationship(self):
#         self.assertEqual(self.user.profile_images().count(), 1)
#         self.assertEqual(self.user.main_profile_image(), self.image)


class ReportUserModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass1'
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass2'
        )
        self.report = ReportUserModel.objects.create(
            user=self.user2,
            user_reported=self.user1,
            body='Test report'
        )

    def test_report_creation(self):
        self.assertEqual(str(self.report), 'testuser1 - Test report...')
        self.assertEqual(self.report.user, self.user2)
        self.assertEqual(self.report.user_reported, self.user1)


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass1'
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass2'
        )
        self.message = MessageModel.objects.create(
            from_user=self.user1,
            to_user=self.user2,
            message='Test message'
        )

    def test_message_creation(self):
        self.assertEqual(str(self.message), 'testuser1 to testuser2 - Test message...')
        self.assertEqual(self.message.from_user, self.user1)
        self.assertEqual(self.message.to_user, self.user2)


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        self.notification = NotificationModel.objects.create(
            user=self.user,
            title='Test notification',
            body='Test body'
        )

    def test_notification_creation(self):
        self.assertEqual(str(self.notification), 'Test notification for user testuser')
        self.assertEqual(self.notification.user, self.user)
