# Python
import urllib
import urlparse

# Django
from django.template import Context
from django.template.loader import get_template

# A+
from apps.models import *


def build_plugin_renderers(plugins, view_name,
                           user_profile=None,
                           submission=None,
                           exercise=None,
                           course_instance=None,
                           course=None,
                           course_module=None,
                           category=None):
    if view_name == "submission":
        context = {
            "user_profile": user_profile,
            "submission": submission
        }
    else:
        raise ValueError(view_name + " is not supported for plugins.")

    plugins = plugins.filter(views__contains=view_name)

    renderers = []
    for p in plugins:
        # TODO: as_leaf_class in for loop causes database call on each cycle
        p = p.as_leaf_class()
        if hasattr(p, "get_renderer_class"):
            renderers.append(p.get_renderer_class()(p, view_name, context))
        else:
            # TODO: use some general renderer instead which supports the old
            # rendering style where plugin's render method is called
            renderers.append(p)

    return renderers


class IFrameToServicePluginRenderer(object):
    def __init__(self, plugin, view_name, context):
        self.plugin = plugin
        self.view_name = view_name
        self.context = context

    def _build_src(self):
        params = {
            "submission_id": self.context["submission"].encode_id(),
            "user_profile": self.context["user_profile"].encode_id(),
            "view_name": self.view_name
        }

        url = self.plugin.service_url

        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qs(url_parts[4]))
        query.update(params)

        url_parts[4] = urllib.urlencode(query)

        return urlparse.urlunparse(url_parts)

    def render(self):
        t = get_template("plugins/iframe_to_service_plugin.html")
        return t.render(Context({
            "height": self.plugin.height,
            "width": self.plugin.width,
            "src": self._build_src(),
            "title": self.plugin.title,
            "view_name": self.view_name
        }))


