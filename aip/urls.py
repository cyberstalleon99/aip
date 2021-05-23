from django.contrib import admin
from django.urls import path, include

from django.views.generic.base import TemplateView

import debug_toolbar

admin.site.site_header = 'AIP Construction'


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('salamat', TemplateView.as_view(template_name='success.html'), name='success'),
    path('maintenance', TemplateView.as_view(template_name='under_construction.html'), name='maintenance'),

    path('workforce/', include('workforce.urls')),
    path('fleet/', include('fleet.urls')),
    path('fuel/', include('fuel.urls')),
    path('operation/', include('operation.urls')),
    path('accounting/', include('accounting.urls')),
    path('warehouse/', include('warehouse.urls')),
    path('gallery/', include('gallery.urls')),
    path('tutorials/', include('tutorials.urls')),

    # API URLs
    path('api/fleet/', include('fleet.api.urls')),

    path('__debug__/', include(debug_toolbar.urls)),
]
