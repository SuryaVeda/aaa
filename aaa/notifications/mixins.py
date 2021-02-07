from .models import *


class CreateNotificationMixin:
    def create_comment_notification(self, post):
        if self.request.user != post.user:
            try:
                nots = Notification.objects.get(user = post.user)
            except Exception as e:
                nots = Notification.objects.create(user=post.user, count = 0)
            mess = Message.objects.create(post_url = post.get_absolute_url(), type='post', text = 'A new comment is added to {0}.. by {1}'.format(post.heading[:10], self.request.user.username))

            nots.message.add(mess)
            nots.count += 1
            nots.save()
        comments = post.comments.all()
        if comments:
            for comment in comments:
                if comment.user != post.user and comment.user != self.request.user:
                    try:
                        nots = Notification.objects.get(user = comment.user)
                    except Exception as e:
                        nots = Notification.objects.create(user=comment.user, count = 0)
                    mess = Message.objects.create(post_url = post.get_absolute_url(), type='post', text = 'A new comment is added to {0}.. by {1}'.format(post.heading[:10], self.request.user.username))
                    nots.message.add(mess)
                    nots.count += 1
                    nots.save()
        return True
