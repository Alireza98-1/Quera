from django.contrib import admin
from .models import Form, ShortTextQuestion, LongTextQuestion, EmailQuestion, NumericQuestion


class QuestionInline(admin.TabularInline):
    model = None  # به صورت داینامیک مشخص می‌شود
    extra = 1


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = []

    def get_inlines(self, request, obj=None):
        self.inlines = []
        for model in [ShortTextQuestion, LongTextQuestion, EmailQuestion, NumericQuestion]:
            inline = type(f"{model.__name__}Inline", (QuestionInline,), {"model": model})
            self.inlines.append(inline)
        return super().get_inlines(request, obj)


@admin.register(ShortTextQuestion)
class ShortTextQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'max_length', 'form')


@admin.register(LongTextQuestion)
class LongTextQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'max_length', 'form')


@admin.register(EmailQuestion)
class EmailQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'form')


@admin.register(NumericQuestion)
class NumericQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'min_value', 'max_value', 'is_decimal_allowed', 'form')
