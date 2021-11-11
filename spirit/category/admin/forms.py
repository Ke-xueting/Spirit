# -*- coding: utf-8 -*-

import re

from django import forms
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str
from django.utils import timezone

from ..models import Category
from ...core import utils
from ...core.utils.forms import NestedModelChoiceField


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = (
            "parent",
            "title",
            "description",
            "is_global",
            "is_closed",
            "is_removed",
            "is_private",
            "color",
            "users"
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.pop('user',None)
        queryset = (
            Category.objects
            .visible(self.user)
            .parents()
            .ordered())

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        self.fields['parent'] = forms.ModelChoiceField(
            queryset=queryset, required=False)
        self.fields['parent'].label_from_instance = (
            lambda obj: smart_str(obj.title))

    def clean_parent(self):
        parent = self.cleaned_data["parent"]

        if self.instance.pk:
            has_children = self.instance.category_set.all().exists()

            if parent and has_children:
                raise forms.ValidationError(
                    _("The category you are updating "
                      "can not have a parent since it has childrens"))

        return parent

    def clean_color(self):
        color = self.cleaned_data["color"]

        if color and not re.match(r'^#([A-Fa-f0-9]{3}){1,2}$', color):
            raise forms.ValidationError(
                _("The input is not a valid hex color."))

        return color

    def get_max_sort(self):
        return (
            Category.objects
            .aggregate(max_sort=Max('sort'))['max_sort'] or 0)

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.sort = self.get_max_sort() + 1
        self.instance.reindex_at = timezone.now()
        return super().save(commit)



class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = (
            "parent",
            "title",
            "description",
            "users"
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.pop('user',None)

        # self.fields['parent'] = NestedModelChoiceField(
        #     queryset=Category.objects.visible(self.user).parents().ordered(),
        #     related_name='category_set',
        #     parent_field='parent_id',
        #     label_field='title',
        #     label=_("Parent"),
        #     empty_label=_("Choose a category"))

        queryset = (
            Category.objects
            .visible(self.user)
            .parents()
            .ordered())

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        self.fields['parent'] = forms.CharField(
            queryset=queryset, required=False)
        self.fields['parent'].label_from_instance = (
            lambda obj: smart_str(obj.title))

    def clean_parent(self):
        parent = self.cleaned_data["parent"]

        if self.instance.pk:
            has_children = self.instance.category_set.all().exists()

            if parent and has_children:
                raise forms.ValidationError(
                    _("The category you are updating "
                      "can not have a parent since it has childrens"))

        return parent

    def clean_color(self):
        color = self.cleaned_data["color"]

        if color and not re.match(r'^#([A-Fa-f0-9]{3}){1,2}$', color):
            raise forms.ValidationError(
                _("The input is not a valid hex color."))

        return color

    def get_max_sort(self):
        return (
            Category.objects
            .aggregate(max_sort=Max('sort'))['max_sort'] or 0)

    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.sort = self.get_max_sort() + 1
        self.instance.reindex_at = timezone.now()
        return super().save(commit)