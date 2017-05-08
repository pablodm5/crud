# from django.shortcuts import render
#Imports de PDF
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from reportlab.graphics import shapes
from reportlab.graphics.charts.axes import XCategoryAxis,YValueAxis
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String
from django.core.urlresolvers import reverse_lazy,reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.template import loader
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse

from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker

from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
# from reportlab.graphics.charts.piecharts import Pie
# from reportlab.graphics.widgets.grids import ShadedRect
# from reportlab.graphics.charts.legends import Legend
# from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String
# from reportlab.graphics.charts.textlabels import Label
# from excelcolors import *
from forms import CourseForm

from .models import Course

def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)

def generar_pdf(request):
    import random
    import django
    import datetime
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    from matplotlib.backends.backend_pdf import PdfPages

    model = Course
    q = Course.objects.all()
    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    for i in q:
        x.append(i.id)
        y.append(i.start_date)
    ax.plot_date(y, x, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


class CourseList(ListView):
            model = Course
class CourseDetail(DetailView):
    model = Course

def crear(request):
    	if request.method == 'POST':
    		form = CourseForm(request.POST, request.FILES)
    		if form.is_valid():
    			curso = form.save()
    			curso.save()
    			return HttpResponseRedirect('home')
    	else:
    		form = CourseForm()
    	template = loader.get_template('course_form.html')
    	context = {
    		'form': form
    	}
        return HttpResponse(template.render(context,request))

# class CourseCreation(CreateView):
#             model = Course
#             success_url = reverse_lazy('courses:list')
#             fields = ['name', 'start_date', 'end_date', 'picture']

class CourseUpdate(UpdateView):
    model = Course
    success_url = reverse_lazy('courses:list')
    fields = ['name', 'start_date', 'end_date', 'picture']
class CourseDelete(DeleteView):
    model = Course
    success_url = reverse_lazy('courses:list')

# class SimplePie(_DrawingEditorMixin,Drawing):
#     def __init__(self,width=200,height=150,*args,**kw):
#         Drawing.__init__(self,width,height,*args,**kw)
#         self._add(self,Pie(),name='chart',validate=None,desc="The main chart")
#         self.chart.width      = 100
#         self.chart.height     = 100
#         self.chart.x          = 25
#         self.chart.y          = 25
#         self.chart.slices[0].fillColor = color01
#         self.chart.slices[1].fillColor = color02
#         self.chart.slices[2].fillColor = color03
#         self.chart.slices[3].fillColor = color04
#         self.chart.slices[4].fillColor = color05
#         self.chart.slices[5].fillColor = color06
#         self.chart.slices[6].fillColor = color07
#         self.chart.slices[7].fillColor = color08
#         self.chart.slices[8].fillColor = color09
#         self.chart.slices[9].fillColor = color10
#         self.chart.data                = (100, 150, 180)
#         self._add(self,Label(),name='Title',validate=None,desc="The title at the top of the chart")
#         self.Title.fontName   = 'Helvetica-Bold'
#         self.Title.fontSize   = 7
#         self.Title.x          = 100
#         self.Title.y          = 135
#         self.Title._text      = 'Chart Title'
#         self.Title.maxWidth   = 180
#         self.Title.height     = 20
#         self.Title.textAnchor ='middle'
#         self._add(self,Legend(),name='Legend',validate=None,desc="The legend or key for the chart")
#         self.Legend.colorNamePairs = [(color01, 'North'), (color02, 'South'),(color03, 'Central')]
#         self.Legend.fontName       = 'Helvetica'
#         self.Legend.fontSize       = 7
#         self.Legend.x              = 160
#         self.Legend.y              = 85
#         self.Legend.dxTextSpace    = 5
#         self.Legend.dy             = 5
#         self.Legend.dx             = 5
#         self.Legend.deltay         = 5
#         self.Legend.alignment      ='right'
#         self.chart.slices.strokeWidth  = 1
#         self.chart.slices.fontName     = 'Helvetica'
#         self.background                = ShadedRect()
#         self.background.fillColorStart = backgroundGrey
#         self.background.fillColorEnd   = backgroundGrey
#         self.background.numShades      = 1
#         self.background.strokeWidth    = 0.5
#         self.background.x              = 25
#         self.background.y              = 25
#         self.Legend.columnMaximum  = 10
#         self._add(self,0,name='preview',validate=None,desc=None)
#         if __name__=="__main__":
#             SimplePie().save(formats=['pdf'],outDir=None,fnRoot=None)
