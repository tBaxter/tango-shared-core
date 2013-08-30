from django import template
from django.utils.timesince import timesince
register = template.Library()


@register.filter
def short_timesince(date):
	"""
	selects only the first part of the returned string, splitting on the comma from timesince.
	Ex. 3 days, 20 hours becomes "3 days ago"
	"""
	try:
		timesince_string = timesince(date).split(",")[0]
	except IndexError: # can't get valid datetime !?!
		timesince_string = "some time"
	return timesince_string