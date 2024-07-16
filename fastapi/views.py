from django.http import FileResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree as ET
import os

from script_builder.director import Director
from script_builder.fast_api_builder import FastAPIBuilder
from script_builder.nest_js_builder import NestApiBuilder

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
    
@csrf_exempt
def downloadFileNest(request):
    director = Director()
    if request.method == 'POST':
        try:
            
            tree = ET.ElementTree(ET.fromstring(request.body))
            root = tree.getroot()
            
            director.builder = NestApiBuilder(root.find('psm-model'))
            
            director.so = root.find('psm-model').find("so").get("so-name")
            
            director.build_nest_js_api_rest(root.find('csm-model'), root.find('relational-model'))
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            print(current_dir)

            file_name = 'prueba2.'+ ("bat" if director.so=="WINDOWS" else "sh")
            file_path = os.path.join(current_dir, file_name)
            print(file_path)

            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
            else:
                raise Http404("File not found")
         
            return JsonResponse({'status': 'success', 'message': 'File processed successfully.'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
