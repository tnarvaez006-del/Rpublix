document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const container = document.getElementById("items-container");
    const addBtn = document.getElementById("add-item");
    const submitBtn = document.getElementById("submit-btn");

    let index = 0;

    function validarFormulario() {
        let valid = true;

        const items = container.querySelectorAll(".item-box");

        if (items.length === 0) return false;

        items.forEach(item => {
            const inputs = item.querySelectorAll("input");

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                }
            });

            const reqs = item.querySelectorAll('[name^="requerimientos_"]');
            if (reqs.length === 0) valid = false;
        });

        return valid;
    }

    function actualizarEstadoBoton() {
        submitBtn.disabled = !validarFormulario();
    }

    function crearItem(nombre = "", cantidad = 1, requerimientos = []) {
        const div = document.createElement("div");
        div.classList.add("item-box");

        div.innerHTML = `
            <div class="item-header">
                <h4>Producto</h4>
                <button type="button" class="btn-remove-item">🗑️</button>
            </div>

            <label>Producto / Servicio</label>
            <input type="text" name="item_nombre[]" value="${nombre}">

            <label>Cantidad</label>
            <input type="number" name="item_cantidad[]" value="${cantidad}" min="1">

            <div class="requerimientos">
                <div class="requerimientos-title">Requerimientos</div>
                <div id="req-${index}"></div>

                <button type="button" class="btn-add-req" data-index="${index}">
                    ➕ Agregar requerimiento
                </button>
            </div>
        `;

        container.appendChild(div);

        div.querySelector(".btn-remove-item").addEventListener("click", () => {
            div.remove();
            actualizarEstadoBoton();
        });

        requerimientos.forEach(r => agregarReq(index, r));

        div.querySelector(".btn-add-req").addEventListener("click", function () {
            agregarReq(this.dataset.index);
        });

        div.querySelectorAll("input").forEach(input => {
            input.addEventListener("input", actualizarEstadoBoton);
        });

        index++;
        actualizarEstadoBoton();
    }

    function agregarReq(i, valor = "") {
        const div = document.getElementById(`req-${i}`);

        const wrap = document.createElement("div");
        wrap.classList.add("requerimiento");

        wrap.innerHTML = `
            <input type="text" name="requerimientos_${i}[]" value="${valor}">
            <button type="button" class="btn-remove-req">✖</button>
        `;

        wrap.querySelector(".btn-remove-req").addEventListener("click", () => {
            wrap.remove();
            actualizarEstadoBoton();
        });

        wrap.querySelector("input").addEventListener("input", actualizarEstadoBoton);

        div.appendChild(wrap);
        actualizarEstadoBoton();
    }

    addBtn.addEventListener("click", () => crearItem());

    form.addEventListener("submit", function (e) {
        if (!validarFormulario()) {
            e.preventDefault();
            alert("⚠️ Completa todos los campos antes de guardar");
        }
    });

    /* Cargar items existentes */
    if (typeof existingItems !== "undefined" && existingItems.length > 0) {
        existingItems.forEach(item => {
            crearItem(item.nombre, item.cantidad, item.requerimientos);
        });
    }

    actualizarEstadoBoton();
});



