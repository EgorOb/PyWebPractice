from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

# Create your models here.


class Author(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+79\d{9}$',
        message="Телефонный номер должен быть формата: '+79123456789'."
    )

    username = models.SlugField(verbose_name='Имя аккаунта',
                                help_text="Введите username, не длиннее 50 символов. Использовать нужно английский алфавит, разделять фразы нужно символом '-'",
                                unique=True,
                                )

    email = models.EmailField(verbose_name='Адрес электронной почты',
                              help_text="Адрес почты в формате *@*.*",
                              unique=True,
                              )

    first_name = models.CharField(max_length=100,
                                  verbose_name='Имя',
                                  help_text="Ограничение - не более 100 символов",
                                  null=True,
                                  blank=True,
                                  )

    last_name = models.CharField(max_length=100,
                                 verbose_name='Фамилия',
                                 help_text="Ограничение - не более 100 символов",
                                 null=True,
                                 blank=True,
                                 )

    middle_name = models.CharField(max_length=100,
                                   verbose_name='Отчество',
                                   help_text="Ограничение - не более 100 символов",
                                   null=True,
                                   blank=True,
                                   )

    gender = models.CharField(max_length=1,
                              choices=[('м', 'мужской'), ('ж', 'женский')],
                              verbose_name='Пол',
                              help_text="Выберите пол",
                              null=True,
                              blank=True,
                              )

    self_esteem = models.DecimalField(max_digits=2,
                                      decimal_places=1,
                                      validators=[MinValueValidator(0, "Диапазон [0.0, 5.0]"),
                                                  MaxValueValidator(5, "Диапазон [0.0, 5.0]")],
                                      verbose_name='Уровень самооценки',
                                      help_text="Введите уровень вашей самооценки, только честно! Градация от 0 до 5, где 0 - 'я молодец', 5 - 'я умница'",
                                      null=True,
                                      blank=True,
                                      )

    phone_number = models.CharField(max_length=12,
                                    validators=[phone_regex],
                                    verbose_name='Номер телефона',
                                    help_text="Введите номер телефона через '+7' без пробелов в формате +79123456789 ",
                                    null=True,
                                    blank=True,
                                    unique=True,
                                    )

    city = models.CharField(max_length=100,
                            verbose_name='Город',
                            help_text="Введите название города",
                            null=True,
                            blank=True,
                            )

    bio = models.TextField(verbose_name='Биография',
                           help_text="Напишите здесь о том, почему Вы так хороши",
                           null=True,
                           blank=True,
                           )

    age = models.IntegerField(null=True, editable=False)

    date_birth = models.DateField(verbose_name='Дата рождения',
                                  help_text="Посланцев из будущего не регистрируем!",
                                  null=True,
                                  blank=True,
                                  )

    status_rule = models.BooleanField(verbose_name='Согласие с правилами',
                                      help_text="А ты их читал или как обычно просто галочку поставил?",
                                      )

    image = models.ImageField(upload_to='foto_profile',
                              verbose_name='Картинка профиля',
                              help_text="Фото в профиль, можно не своё! Ну или хоть какое-то. Ладно можно без фото",
                              null=True,
                              blank=True,
                              )

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.last_name} {self.first_name.upper()[0]}.{self.middle_name.upper()[0]}."

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
