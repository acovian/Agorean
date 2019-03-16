from django.db import models
from ..user_app.models import User

# Create your models here.

class MessageManager(models.Manager):
    def validate(self, message, user_id):
        errors = []
        if len(message)<1:
            errors.append("* Please include a message in order to post one.")
        if errors:
            return (False, errors)
        else:
            user = User.objects.get(id=user_id)
            message = Message.objects.create(message=message, user=user)
            return (True, message)

    def destroy_message(self, message_id):
        message_id = int(message_id)
        message = Message.objects.get(id=message_id)
        message.delete()
        return True

    def update_information(self, data, id):
        message = self.filter(id=id)
        if data["message"]:
            message.update(message=data["message"])
        return True

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageManager()

############

class CommentManager(models.Manager):
    def create_comment(self, comment, message, user):
        comment = self.create(comment=comment, message=message, user=user)
        return comment

    def validate_comment(self, data, user_id, id):
        errors = []
        if len(data["comment"])<1:
            errors.append("* Make sure you have written something to comment.")
            return (False, errors)
        else:
            user = User.objects.get(id=user_id)
            message = Message.objects.get(id=id)
            comment = self.create_comment(data["comment"], message, user)
            return (True, comment)

    def destroy_comment(self, comment_id):
        comment_id = int(comment_id)
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return True

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="comment")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()

############

class LikeManager(models.Manager):
    def create_like(self, user, message_id):
        message = Message.objects.get(id=message_id)
        self.create(user=user, message=message)

    def validate_like(self, user_id, message_id):
        thing1 = int(message_id)
        message = Message.objects.get(id=thing1)
        thing2 = int(user_id)
        user = User.objects.get(id=thing2)
        try:
            self.get(user=user, message=message)
            return False
        except:
            self.create_like(user, message_id)
            return True

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="messagelikes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = LikeManager()
