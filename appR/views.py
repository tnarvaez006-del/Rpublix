from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Usuario
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm
def login_view(request):
    if request.method == "POST":
        correo = request.POST.get("correo_empresarial")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=correo,     # ← IMPORTANTE
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Correo o contraseña incorrectos.")

    return render(request, "appR/login.html")



@login_required(login_url='login')
def dashboard_view(request):
    return redirect('inicio')


@login_required(login_url='login')
def usuarios_view(request):
    usuarios = Usuario.objects.all()
    return render(request, "appR/dashboard_usuarios.html", {"usuarios": usuarios})

@login_required(login_url='login')
def dasboard_layaut_Principal_view(request):
    return render(request, "appR/dasboard_layaut_Principal.html", {"user": request.user})

#vistas de usuarios

@login_required(login_url='login')
def agregar_usuario_view(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        username = request.POST.get("username")
        email = request.POST.get("email")

        # Validación: contraseñas iguales
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "appR/agregar_usuario.html", {"form": form})

        # Validación: username duplicado
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está registrado.")
            return render(request, "appR/agregar_usuario.html", {"form": form})

        # Validación: email duplicado
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está registrado.")
            return render(request, "appR/agregar_usuario.html", {"form": form})

        # Validación de Django
        if form.is_valid():
            nuevo_usuario = form.save(commit=False)
            nuevo_usuario.set_password(password1)
            nuevo_usuario.save()

            messages.success(request, "Usuario creado correctamente.")
            return redirect("list")

    else:
        form = UsuarioForm()

    return render(request, "appR/agregar_usuario.html", {"form": form})



@login_required(login_url='login')
def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)

    if request.method == "POST":
        usuario.nombre_completo = request.POST["nombre_completo"]
        usuario.correo_empresarial = request.POST["correo_empresarial"]
        usuario.rol = request.POST["rol"]

        pass1 = request.POST.get("password")
        pass2 = request.POST.get("password_confirm")

        # Validación de contraseña
        if pass1 or pass2:              # Solo si se intenta cambiar
            if pass1 != pass2:
                messages.error(request, "Las contraseñas no coinciden.")
                return render(request, "appR/editar_usuario.html", {"usuario": usuario})
            
            usuario.set_password(pass1)

        usuario.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect("list")

    return render(request, "appR/editar_usuario.html", {"usuario": usuario})



@login_required(login_url='login')
def deshabilitar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    usuario.is_active = False
    usuario.save()
    return redirect('list')


@login_required(login_url='login')
def habilitar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    usuario.is_active = True
    usuario.save()
    return redirect('list')


@login_required(login_url='login')
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    usuario.delete()
    return redirect('list')