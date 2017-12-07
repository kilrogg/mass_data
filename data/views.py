# coding: utf-8

import random
import string
from django.db import connection
from django.shortcuts import render_to_response
from django.forms.models import model_to_dict

from operator import attrgetter

from data.forms import TestDataForm
from data.models import TestData


def _write(valid_objects):
    if not valid_objects:
        return

    # existing elements
    existing = TestData.objects.in_bulk(map(attrgetter('pk'), valid_objects))

    creations = []

    # update or create?
    for instance in valid_objects:
        # update
        if instance.pk in existing:
            updated_fields = {
                field: value
                for field, value
                in model_to_dict(instance).items()
                if getattr(existing[instance.pk], field) != value
            }
            if updated_fields:
                TestData.objects.filter(pk=instance.pk).update(**updated_fields)
        # create
        else:
            creations.append(instance)

    # new elements
    TestData.objects.bulk_create(creations)


def testview(request):

    valid_objects = []

    for nr in range(1, 5000):

        data = {
            'belegnr': 'AB%s' % nr,
            'text': ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
        }

        form = TestDataForm(data)
        if form.is_valid():
            instance = form.save(commit=False)
            valid_objects.append(instance)

        if len(valid_objects) > 1000:
            _write(valid_objects)
            valid_objects = []

    _write(valid_objects)

    return render_to_response('output.html', {
        'queries': connection.queries
    })
