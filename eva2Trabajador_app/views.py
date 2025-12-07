from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone


from .models import Usuarios
from eva2Trabajador_app.models import Liquidaciones, Trabajador, Descuentos


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
                messages.error(request, "Usuario no registrado")
                return render(request, "eva2LopezJorge_app/login.html", {"form": form})

            request.session["usuario_id"] = u.id
            request.session["perfil"] = u.perfil

            if u.perfil == 1:
                return redirect("dashboard_admin")
            elif u.perfil == 2:
                return redirect("dashboard_trabajador")
            elif u.perfil == 3:
                return redirect("dashboard_jefe")

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

    rut = u.username
    hoy = timezone.now()
    mes = hoy.month
    anio = hoy.year

    trabajador = Trabajador.objects.filter(rut=rut).first()
    Liquidaciones = Liquidaciones.objects.filter(rut=rut, mes=mes, anio=anio).first()
    descuentos = Descuentos.objects.filter(rut=rut, fecha__year=anio, fecha__month=mes)

    contexto = {
        "usuario": u,
        "rut": rut,
        "trabajador": trabajador,
        "liquidacion": Liquidaciones,
        "descuentos": descuentos,
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
            liquidaciones = Liquidaciones.objects.filter(mes=int(mes), anio=int(anio))
        except ValueError:
            liquidaciones = None

    contexto = {
        "usuario": u,
        "liquidaciones": liquidaciones,
        "mes": mes,
        "anio": anio,
    }
    return render(request, "eva2LopezJorge_app/dashboard_jefe.html", contexto)