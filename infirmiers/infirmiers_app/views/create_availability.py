from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from infirmiers_app.forms.availabilityForm import AvailabilityForm
from infirmiers_app.models.nurse import Nurse
from infirmiers_app.models.availableDay import AvailableDay
from infirmiers_app.models.interval import Interval

def availability_creation_view(request, nurse_id):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            WeekDay = form.cleaned_data['AvailableDay'][0]
            Start_time = manipulate_time(form.cleaned_data['Start_time'])
            End_time = manipulate_time(form.cleaned_data['End_time'])

            #create an object Interval
            time_available = Interval(start_time=Start_time, end_time=End_time)
            time_available.save()

            #create an object AvailableDay
            availability = AvailableDay(weekday=WeekDay)
            availability.save()
            availability.intervals.add(time_available)

            #create an object Nurse
            nurse = Nurse.objects.get(pk = nurse_id)
            nurse.availableDays.add(availability)

            return HttpResponseRedirect(reverse("nurse_list"))

    else:
        form = AvailabilityForm()

    return render(request, 'createAvailability.html', {'form': form, 'nurse_id':nurse_id })

def manipulate_time(time):
    """Function that calcule the number of about fifteen in the time"""
    hours_time = time.hour
    minute_time = time.minute
    return hours_time*4 + minute_time/15
