from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json
import os

from script_builder.director import Director
from script_builder.fast_api_builder import FastAPIBuilder

@csrf_exempt
def download_file(request):
    director = Director()

    model = json.loads(request.body).get("api-rest-model")

    director.builder = FastAPIBuilder(model.get("psm-model"))

    director.build_fast_api_api_rest(model.get("csm-model"), model.get("relational-model"))

    # Obtener el directorio actual del archivo Python
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta al archivo prueba.sh
    file_path = os.path.join(current_dir, "prueba.sh")

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename="prueba.sh")
    else:
        raise Http404("File not found")
