# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from imagekit.cachefiles import ImageCacheFile
from pilkit.processors import ResizeToFill

from .models import *
from .widgets import *
from imagekit.admin import AdminThumbnail
from imagekit import ImageSpec


class CssMixin(object):
    class Media:
        css = {"all": ("css/style.css",)}


class AdminThumbnailSpecS(ImageSpec):
    processors = [ResizeToFill(50, 50)]
    format = 'PNG'
    options = {'quality': 50}


class AdminThumbnailSpecM(ImageSpec):
    processors = [ResizeToFill(150, 150)]
    format = 'PNG'
    options = {'quality': 80}


def cached_admin_thumb_factory(name, size):
    def cached_admin_thumb(instance):
        # `image` is the name of the image field on the model
        if size == 'S':
            cached = ImageCacheFile(AdminThumbnailSpecS(getattr(instance, name)))
        else:
            cached = ImageCacheFile(AdminThumbnailSpecM(getattr(instance, name)))
        # only generates the first time, subsequent calls use cache
        cached.generate()
        return cached

    return cached_admin_thumb


class OptionInlineForm(forms.ModelForm, CssMixin):
    class Meta:
        model = Option
        fields = '__all__'

        widgets = {
            'customScripts': JsEditor(),
        }


class OptionInline(admin.StackedInline, CssMixin):
    model = Option
    form = OptionInlineForm
    can_delete = True
    fk_name = 'dialogue'
    extra = 1

    fields = [field.name for field in model._meta.fields]

    inline_classes = ('grp-collapse grp-open',)
    readonly_fields = ('id',)


class CharacterRelInline(admin.StackedInline, CssMixin):
    extra = 0
    model = CharacterRel
    fields = [field.name for field in model._meta.fields]
    inline_classes = ('grp-collapse grp-open',)
    readonly_fields = ('id',)


class DialogueAdmin(admin.ModelAdmin, CssMixin):
    model = Dialogue

    inlines = (OptionInline,)
    list_display = [field.name for field in model._meta.fields if field.name != "id"]
    raw_id_fields = ('character',)
    autocomplete_lookup_fields = {
        'fk': ['character']
    }


class PlayerAdmin(admin.ModelAdmin, CssMixin):
    model = Player
    raw_id_fields = ('owner',)
    avatar_display_s = AdminThumbnail(image_field=cached_admin_thumb_factory('avatar', 'S'))
    avatar_display_s.short_description = 'Thumbnail'
    list_display = ['__str__', 'avatar_display_s']

    avatar_display_m = AdminThumbnail(image_field=cached_admin_thumb_factory('avatar', 'M'))
    avatar_display_m.short_description = 'Thumbnail'
    readonly_fields = ('avatar_display_m',)
    inlines = (CharacterRelInline, )

    autocomplete_lookup_fields = {
        'fk': ['owner']
    }


class CharacterAdmin(admin.ModelAdmin, CssMixin):
    model = Character
    avatar_display_s = AdminThumbnail(image_field=cached_admin_thumb_factory('avatar', 'S'))
    avatar_display_s.short_description = 'Thumbnail'
    avatar_display_m = AdminThumbnail(image_field=cached_admin_thumb_factory('avatar', 'M'))
    avatar_display_m.short_description = 'Thumbnail'
    list_display = ['__str__', 'description', 'avatar_display_s']
    readonly_fields = ('avatar_display_m',)


admin.site.register(Player, PlayerAdmin)
admin.site.register(Dialogue, DialogueAdmin)
admin.site.register(Character, CharacterAdmin)
