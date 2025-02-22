# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser

from ..user.models import UserProfile

from spirit.core.conf import settings


class CategoryQuerySet(models.QuerySet):
    def unremoved(self):
        return self.filter(
            Q(parent=None) | Q(parent__is_removed=False),
            is_removed=False)

    def public(self):
        return self.filter(is_private=False)

    def visible(self, user):
            if isinstance(user, AnonymousUser):
                return self.unremoved().public()

            return self.unremoved().filter(users__exact = user) | self.unremoved().public()

    def opened(self):
        return self.filter(
            Q(parent=None) | Q(parent__is_closed=False),
            is_closed=False)

    def parents(self):
        return self.filter(parent=None)

    def children(self, parent):
        if parent.is_subcategory:
            return self.none()

        return self.filter(parent=parent)

    def ordered(self):
        if settings.ST_ORDERED_CATEGORIES:
            return self.order_by('sort', 'pk')
        return self.order_by('title', 'pk')
