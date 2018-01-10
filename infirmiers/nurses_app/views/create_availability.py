from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.utils import IntegrityError

from nurses_app.forms.availabilityForm import AvailabilityForm
from nurses_app.models.nurse import Nurse
from nurses_app.models.interval import Interval
from django.contrib.auth.decorators import login_required

@login_required
def availability_creation_view(request, nurse_id):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            WeekDay = form.cleaned_data['AvailableDay'][0]
            Start_time = manipulate_time(form.cleaned_data['Start_time'])
            End_time = manipulate_time(form.cleaned_data['End_time'])

            #create an object Interval
            try:
                interval = Interval(start_time=Start_time, end_time=End_time, weekday=WeekDay)
                interval.save()
            except IntegrityError:
                interval = Interval.objects.filter(start_time=Start_time, end_time=End_time, weekday=WeekDay)[0]

            #get the corresponded Nurse
            nurse = Nurse.objects.get(pk = nurse_id)
            nurse.intervals.add(interval)

            return HttpResponseRedirect(reverse("nurse_detail",args=[nurse_id]))

    else:
        form = AvailabilityForm()

    return render(request, 'createAvailability.html', {'form': form, 'nurse_id':nurse_id })


def manipulate_time(time):
    """Function that calcule the number of about fifteen in the time"""
    hours_time = time.hour
    minute_time = time.minute
    return hours_time*4 + minute_time/15