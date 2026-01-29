from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Usuario, Cliente, Orden, ItemServicio, Requerimiento, Tarea
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm, ClienteForm, OrdenForm
from django.utils.timezone import now
from django.contrib.auth import logout
from django.db.models import Q
from django.utils.timezone import now


def logout_view(request):
    logout(request)
    return redirect('login')  # redirige a tu vista de login

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


# ============================
#       vista cliente
# ============================


@login_required(login_url='login')
def clientes_list(request):
    query = request.GET.get("q", "").strip()

    if query:
        clientes = Cliente.objects.filter(
            Q(id__icontains=query) |
            Q(nombre__icontains=query) |
            Q(cedula__icontains=query) |
            Q(telefono__icontains=query) |
            Q(correo__icontains=query) |
            Q(tipo_cliente__icontains=query) |
            Q(categoria__icontains=query)
        )
    else:
        clientes = Cliente.objects.all()


        print("QUERY:", query)
        print("CLIENTES:", clientes.count())

    return render(
        request,
        "appR/clientes_list.html",
        {
            "clientes": clientes,
            "query": query
        }
    )

@login_required(login_url='login')
def cliente_agregar(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente agregado correctamente.")
            return redirect("clientes_list")
        else:
            messages.error(request, "Error: revisa los datos ingresados.")
    else:
        form = ClienteForm()

    return render(request, "appR/cliente_form.html", {
        "form": form,
        "titulo": "Agregar Cliente"
    })



@login_required(login_url='login')
def cliente_editar(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect("clientes_list")
        else:
            messages.error(request, "Error: revisa los datos.")
    else:
        form = ClienteForm(instance=cliente)

    return render(request, "appR/cliente_form.html", {
        "form": form,
        "titulo": "Editar Cliente"
    })

# ============================
#       vista ordenes
# ============================

@login_required
def ordenes_list(request):
    ordenes = Orden.objects.select_related(
        "cliente",
        "responsable"
    ).order_by("-fecha_creacion")

    return render(request, "appR/ordenes_list.html", {
        "ordenes": ordenes
    })

@login_required
def crear_orden(request):
    if request.method == "POST":
        form = OrdenForm(request.POST)

        if form.is_valid():
            orden = form.save(commit=False)
            orden.responsable = request.user   # 👈 USUARIO LOGUEADO
            orden.save()

            items = request.POST.getlist("item_nombre[]")
            cantidades = request.POST.getlist("item_cantidad[]")

            for index, nombre in enumerate(items):
                item = ItemServicio.objects.create(
                    orden=orden,
                    nombre=nombre,
                    cantidad=cantidades[index]
                )

                requerimientos = request.POST.getlist(f"requerimientos_{index}[]")
                for req in requerimientos:
                    Requerimiento.objects.create(
                        item=item,
                        descripcion=req
                    )

            return redirect("ordenes_list")
    else:
        form = OrdenForm()

    return render(request, "appR/orden_form.html", {"form": form})


# views.py
@login_required
def orden_edit(request, orden_id):
    orden = get_object_or_404(Orden, pk=orden_id)
    form = OrdenForm(request.POST or None, instance=orden)

    # Preparamos los items existentes
    items = orden.items.all().prefetch_related('requerimientos')

    if request.method == "POST" and form.is_valid():
        form.save()

        # Eliminamos items antiguos y requerimientos para reemplazar por los nuevos del form
        orden.items.all().delete()

        # Guardamos los nuevos items y requerimientos
        items_nombres = request.POST.getlist("item_nombre[]")
        items_cantidades = request.POST.getlist("item_cantidad[]")

        for idx, nombre in enumerate(items_nombres):
            item = ItemServicio.objects.create(
                orden=orden,
                nombre=nombre,
                cantidad=items_cantidades[idx]
            )
            requerimientos = request.POST.getlist(f"requerimientos_{idx}[]")
            for req in requerimientos:
                Requerimiento.objects.create(item=item, descripcion=req)

        return redirect('orden_detail', orden_id=orden.id)

    return render(request, "appR/orden_form.html", {
        "form": form,
        "editando": True,
        "items": items,  # enviamos los items existentes al template
    })


@login_required
def orden_detail(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id)

    # Prepara los items con sus requerimientos
    items_con_req = []
    for item in orden.items.all():
        requerimientos = item.requerimientos.all()
        items_con_req.append({
            "nombre": item.nombre,
            "cantidad": item.cantidad,
            "requerimientos": requerimientos
        })

    return render(request, "appR/orden_detail.html", {
        "orden": orden,
        "items_con_req": items_con_req
    })


@login_required
def orden_delete(request, pk):
    orden = get_object_or_404(Orden, pk=pk)

    if request.method == "POST":
        orden.delete()
        messages.success(request, "Orden eliminada correctamente")
        return redirect("ordenes_list")

    return redirect("orden_detail", pk=pk)

@login_required(login_url='login')
def dasboard_layaut_Principal_view(request):
    today = now().date()

    # ================= TARJETAS =================
    total_orders = Orden.objects.count()

    in_progress = Orden.objects.filter(
        estado="En proceso"
    ).count()

    finished_orders = Orden.objects.filter(
        estado="Completado"
    ).count()

    late_orders = Orden.objects.filter(
        estado="En proceso",
        fecha_entrega__lt=today
    ).count()

    # ================= ÓRDENES RECIENTES =================
    recent_orders = Orden.objects.select_related("cliente") \
        .order_by("-fecha_creacion")[:5]

    for order in recent_orders:
        if order.estado == "Completado":
            order.progress = 100
        elif order.estado == "En proceso":
            order.progress = 50
        else:
            order.progress = 0

    # ================= SEMÁFORO DE ÓRDENES =================
    late_count = Orden.objects.filter(
        estado="En proceso",
        fecha_entrega__lt=today
    ).count()

    risk_count = Orden.objects.filter(
        estado="En proceso",
        fecha_entrega=today
    ).count()

    ontime_count = Orden.objects.filter(
        estado="En proceso",
        fecha_entrega__gt=today
    ).count()

    # ================= SERVICIOS RECIENTES =================
    recent_services = ItemServicio.objects.select_related(
        "orden"
    ).order_by("-id")[:6]

    context = {
        "total_orders": total_orders,
        "in_progress": in_progress,
        "finished_orders": finished_orders,
        "late_orders": late_orders,

        "recent_orders": recent_orders,

        "late_count": late_count,
        "risk_count": risk_count,
        "ontime_count": ontime_count,

        "recent_services": recent_services,
        "user": request.user,
    }

    return render(
        request,
        "appR/dasboard_layaut_Principal.html",
        context
    )


@login_required
def orden_revision(request, orden_id):

    orden = get_object_or_404(Orden, id=orden_id)

    if request.method == "POST":
        item_id = request.POST.get("item_id")
        estado = request.POST.get("estado")

        item = get_object_or_404(ItemServicio, id=item_id, orden=orden)
        item.estado = estado
        item.save()

        # 🔥 actualizar estado general de la orden
        actualizar_estado_orden(orden)

        return redirect("orden_revision", orden_id=orden.id)

    servicios = ItemServicio.objects.filter(orden=orden)

    return render(request, "appR/orden_revision.html", {
        "orden": orden,
        "servicios": servicios
    })



@login_required
def tareas_usuario(request):

    if request.method == "POST":
        Tarea.objects.create(
            usuario=request.user,
            titulo=request.POST.get("titulo"),
            descripcion=request.POST.get("descripcion"),
            fecha_inicio=request.POST.get("fecha_inicio"),
            fecha_fin=request.POST.get("fecha_fin"),
        )
        return redirect("mis_tareas")

    tareas = Tarea.objects.filter(usuario=request.user).order_by("fecha_inicio")

    return render(request, "appR/tareas.html", {
        "tareas": tareas
    })



@login_required
def completar_tarea(request, tarea_id):

    tarea = get_object_or_404(
        Tarea,
        id=tarea_id,
        usuario=request.user
    )

    tarea.estado = "Completada"
    tarea.save()

    return redirect("mis_tareas")


@login_required
def eliminar_tarea(request, tarea_id):

    tarea = get_object_or_404(
        Tarea,
        id=tarea_id,
        usuario=request.user
    )

    tarea.delete()

    return redirect("mis_tareas")




def actualizar_estado_orden(orden):

    servicios = orden.items.all()

    total = servicios.count()
    verdes = servicios.filter(estado="Completado").count()
    amarillos = servicios.filter(estado="En proceso").count()
    rojos = servicios.filter(estado="Pendiente").count()

    from django.utils.timezone import now
    hoy = now().date()

    # 🟢 TODOS COMPLETADOS
    if verdes == total and total > 0:
        orden.estado = "Completado"

    # 🟡 EN PROCESO
    elif amarillos > 0:
        orden.estado = "En proceso"

    # 🔴 TODOS PENDIENTES
    elif rojos == total:
        orden.estado = "Pendiente"

    # ⚠️ RIESGO
    if orden.estado == "En proceso" and orden.fecha_entrega <= hoy:
        orden.estado = "En proceso"

    orden.save()
