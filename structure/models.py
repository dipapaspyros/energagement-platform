from __future__ import unicode_literals

import uuid as uuid

from django.contrib.auth.models import User
from django.db import models

from .lists import UNIT_TYPES, SUPPORTED_CONNECTION_TYPES


class Location(models.Model):
    """
    A location object
    Contains both co-ordinates as well as a text representation (e.g street name/number, city etc.)
    """
    lat = models.IntegerField()
    lng = models.IntegerField()
    address = models.TextField()


class Unit(models.Model):
    """
    A distinct energy management unit
    e.g a building, power station, factory etc.
    """
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255, blank=False, null=False)
    unit_type = models.CharField(max_length=31, choices=UNIT_TYPES, blank=False, null=False)
    location = models.ForeignKey(Location)


class Connection(models.Model):
    """
    A connection to a network of sensors
    e.g a ModBus connection
    """
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255, blank=False, null=False)
    connection_type = models.CharField(max_length=31, choices=SUPPORTED_CONNECTION_TYPES, blank=False, null=False)
    connection_info = models.TextField(blank=False, null=False)


class Region(models.Model):
    """
    A physical part of a Unit
    Can be either directly under a Unit or under another Region
    """
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    parent_region = models.ForeignKey('self')
    parent_unit = models.ForeignKey(Unit)
