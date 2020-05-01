from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png', ]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)

    avatar = models.FileField(upload_to='files/user/avatar/',
                              null=True,
                              blank=True,
                              validators=[validate_file_extension])

    description = models.CharField(max_length=512,
                                   null=False,
                                   blank=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Article(models.Model):
    title = models.CharField(max_length=128,
                             null=False,
                             blank=False)
    cover = models.FileField(upload_to='files/article/cover/',
                             validators=[validate_file_extension])
    short_content = models.CharField(max_length=128,
                             null=False,
                             blank=False,
                             default='لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است…')
    content = RichTextField(default='لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد، تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی، و فرهنگ پیشرو در زبان فارسی ایجاد کرد، در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها، و شرایط سخت تایپ به پایان رسد و زمان مورد نیاز شامل حروفچینی دستاوردهای اصلی، و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد.')
    created_at = models.DateTimeField(default=datetime.now,
                                      blank=False)
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile,
                               on_delete=models.CASCADE)
    promoted = models.BooleanField(default=False)
    first_slider = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=128,
                             null=False,
                             blank=False)
    cover = models.FileField(upload_to='files/article/category_cover/',
                             null=False,
                             blank=False,
                             validators=[validate_file_extension])

    def __str__(self):
        return self.title
