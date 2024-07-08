from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
import os

from script_builder.director import Director
from script_builder.fast_api_builder import FastAPIBuilder

@csrf_exempt
def download_file(request):
    director = Director()

    tree = ET.ElementTree(ET.fromstring(request.body))
    root = tree.getroot()

    director.builder = FastAPIBuilder(root.find('psm-model'))

    director.so = root.find('psm-model').find("so").get("so-name")
    director.build_fast_api_api_rest(root.find('csm-model'), root.find('relational-model'))

    current_dir = os.path.dirname(os.path.abspath(__file__))

    file_name = 'prueba.'+ ("bat" if director.so=="WINDOWS" else "sh")
    file_path = os.path.join(current_dir, file_name)

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    else:
        raise Http404("File not found")
