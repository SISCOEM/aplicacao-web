from .settings import AUX

def global_variables(request):
    # Adicione as variáveis que você deseja tornar globais
    return {
        'AUX': AUX,
        "link": f"http://{AUX['ip']}:8000/",
    }
