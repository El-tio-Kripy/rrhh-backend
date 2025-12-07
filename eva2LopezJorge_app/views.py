from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import LoginForm
from .models import Usuarios
from eva2Trabajador_app.models import Liquidacion

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data["usuario"]
            contrasena = form.cleaned_data["contrasena"]
            try:
                u = Usuarios.objects.get(username=usuario)
            except Usuarios.DoesNotExist:
                messages.error(request, "Usuario no registrado")
                return render(request, "eva2LopezJorge_app/login.html", {"form": form})

            if u.password != contrasena:
                # Se mantiene el mismo mensaje para no revelar si existe el usuario o no.
                messages.error(request, "Usuario no registrado")
                return render(request, "eva2LopezJorge_app/login.html", {"form": form})

            # Login correcto
            request.session["usuario_id"] = u.id
            request.session["perfil"] = u.perfil

            if u.perfil == 1:
                return redirect("dashboard_admin")
            elif u.perfil == 2:
                return redirect("dashboard_trabajador")
            elif u.perfil == 3:
                return redirect("dashboard_jefe")
            else:
                messages.error(request, "Perfil de usuario no válido.")
    else:
        form = LoginForm()

    return render(request, "eva2LopezJorge_app/login.html", {"form": form})

def logout_view(request):
    request.session.flush()
    return redirect("login")

def _get_usuario_en_sesion(request):
    uid = request.session.get("usuario_id")
    if not uid:
        return None
    try:
        return Usuarios.objects.get(id=uid)
    except Usuarios.DoesNotExist:
        return None

def dashboard_admin(request):
    u = _get_usuario_en_sesion(request)
    if not u or u.perfil != 1:
        return redirect("login")
    return render(request, "eva2LopezJorge_app/dashboard_admin.html", {"usuario": u})

def dashboard_trabajador(request):
    u = _get_usuario_en_sesion(request)
    if not u or u.perfil != 2:
        return redirect("login")

    # Se asume que el username del trabajador corresponde a su RUT.
    rut = u.username
    hoy = timezone.now()
    mes = hoy.month
    anio = hoy.year
    liquidacion = Liquidacion.objects.filter(rut=rut, mes=mes, anio=anio).first()

    contexto = {
        "usuario": u,
        "rut": rut,
        "liquidacion": liquidacion,
        "mes": mes,
        "anio": anio,
    }
    return render(request, "eva2LopezJorge_app/dashboard_trabajador.html", contexto)

def dashboard_jefe(request):
    u = _get_usuario_en_sesion(request)
    if not u or u.perfil != 3:
        return redirect("login")

    mes = request.GET.get("mes")
    anio = request.GET.get("anio")
    liquidaciones = None
    if mes and anio:
        try:
            mes = int(mes)
            anio = int(anio)
            liquidaciones = Liquidacion.objects.filter(mes=mes, anio=anio)
        except ValueError:
            mes = anio = None

    contexto = {
        "usuario": u,
        "liquidaciones": liquidaciones,
        "mes": mes,
        "anio": anio,
    }
    return render(request, "eva2LopezJorge_app/dashboard_jefe.html", contexto)
