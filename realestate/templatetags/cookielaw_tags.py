import warnings

from classytags.helpers import InclusionTag
from django import template
from django.template.loader import render_to_string


register = template.Library()


class CookielawBanner(InclusionTag):
    """
    only show if not clicked away yet
    """

    template = 'realestate/cookiebanner.html'

    def render_tag(self, context, **kwargs):
        template_filename = self.get_template(context, **kwargs)

        if 'request' not in context:
            warnings.warn('No request object in context. '
                          'Are you sure you have django.core.context_processors.request enabled?')

        if context['request'].COOKIES.get('cookielaw_accepted', False):
            return ''

        data = self.get_context(context, **kwargs)
        return render_to_string(template_filename, data, context_instance=context)

register.tag(CookielawBanner)