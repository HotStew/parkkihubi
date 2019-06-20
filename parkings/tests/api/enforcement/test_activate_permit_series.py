import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework.status import HTTP_200_OK

from parkings.models import PermitSeries


def get_url(obj):
    return reverse('enforcement:v1:permitseries-detail', kwargs={'pk': obj.pk})


def test_series_get_activated(staff_api_client):
    new_permit_series = PermitSeries.objects.create(active=False)
    old_permit_series = PermitSeries.objects.create(active=True)

    response = staff_api_client.post(get_url(new_permit_series) + 'activate/')

    assert response.status_code == HTTP_200_OK
    assert response.data['status'] == "OK"
    assert PermitSeries.objects.latest_active() == new_permit_series
    assert not PermitSeries.objects.get(id=old_permit_series.id).active


def test_old_series_are_pruned(staff_api_client):
    new_permit_series = PermitSeries.objects.create(active=False)
    old_permit_series = PermitSeries.objects.create()
    old_permit_series.created_at = timezone.now() - datetime.timedelta(3)
    old_permit_series.save()

    assert PermitSeries.objects.all().count() == 2
    response = staff_api_client.post(get_url(new_permit_series) + 'activate/')
    assert response.status_code == HTTP_200_OK
    assert response.data['status'] == "OK"
    assert PermitSeries.objects.all().count() == 1
