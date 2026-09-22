"use strict";

var CONTACT_TYPES = ["telefono", "whatsapp", "telegram", "instagram", "facebook", "x", "threads", "tiktok", "youtube", "tunein", "iheart", "web", "email"];
var DAYS = [1, 2, 3, 4, 5, 6, 7];
var DAY_NAMES = { 1: "Lunes", 2: "Martes", 3: "Miércoles", 4: "Jueves", 5: "Viernes", 6: "Sábado", 7: "Domingo" };
var ERRORS = {
  incomplete: "Completa al menos el nombre y la frecuencia de la estación.",
  duplicate: "Ya existe una estación con esa frecuencia en la misma banda.",
  not_found: "La estación no existe."
};

var state = {
  estaciones: [],
  search: "",
  banda: "ALL",
  editing: null,
  isNew: false,
  originalId: null
};

function $(id) { return document.getElementById(id); }

function esc(value) {
  return String(value == null ? "" : value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function api(path, options) {
  options = options || {};
  options.headers = options.headers || {};
  options.headers["Content-Type"] = "application/json";
  return fetch(path, options).then(function (res) {
    return res.json().catch(function () { return {}; }).then(function (data) {
      if (!res.ok) {
        var err = new Error(ERRORS[data.error] || ("Error HTTP " + res.status));
        err.status = res.status;
        throw err;
      }
      return data;
    });
  });
}

function flash(message) {
  var el = $("flash");
  el.textContent = message;
  el.hidden = false;
  setTimeout(function () { el.hidden = true; }, 3000);
}

function showError(message) {
  var el = $("error");
  el.textContent = message;
  el.hidden = false;
  setTimeout(function () { el.hidden = true; }, 5000);
}

function loadList() {
  return api("/api/estaciones").then(function (data) {
    state.estaciones = data.estaciones || [];
  });
}

function render() {
  if (state.editing) renderEdit();
  else renderList();
}

function renderList() {
  var q = state.search.trim().toLowerCase();
  var list = state.estaciones.filter(function (s) {
    if (state.banda !== "ALL" && s.banda !== state.banda) return false;
    if (!q) return true;
    return s.nombre.toLowerCase().indexOf(q) !== -1 ||
      String(s.frecuencia).indexOf(q) !== -1;
  }).sort(function (a, b) {
    if (a.banda !== b.banda) return a.banda === "FM" ? -1 : 1;
    return parseFloat(a.frecuencia) - parseFloat(b.frecuencia);
  });

  var rows = list.map(function (s) {
    return "<tr>" +
      '<td><span class="freq-badge">' + esc(s.frecuencia + " " + s.banda) + "</span></td>" +
      "<td>" + esc(s.nombre) + (s.verificado ? ' <span class="verified">Verificado</span>' : "") + "</td>" +
      '<td class="col-actions">' +
        '<button type="button" class="btn btn-small" data-action="edit" data-id="' + esc(s.id) + '">Editar</button> ' +
        '<button type="button" class="btn btn-danger btn-small" data-action="delete" data-id="' + esc(s.id) + '">Eliminar</button>' +
      "</td>" +
    "</tr>";
  }).join("");

  $("list-view").hidden = false;
  $("edit-view").hidden = true;
  $("table-body").innerHTML = rows || '<tr><td colspan="3" class="muted">No se encontraron estaciones.</td></tr>';
  $("count").textContent = state.estaciones.length + " estaciones";
}

function contactRow(c) {
  var opts = CONTACT_TYPES.map(function (tp) {
    return '<option value="' + tp + '"' + (c.tipo === tp ? " selected" : "") + ">" + tp + "</option>";
  }).join("");
  return '<div class="row contact-row">' +
    '<select class="c-tipo">' + opts + "</select>" +
    '<input type="text" class="c-valor" value="' + esc(c.valor) + '" placeholder="Valor">' +
    '<input type="text" class="c-etiqueta" value="' + esc(c.etiqueta || "") + '" placeholder="Etiqueta">' +
    '<button type="button" class="btn btn-danger btn-small" data-remove="contact">Quitar</button>' +
  "</div>";
}

function programCard(p) {
  var dias = DAYS.map(function (d) {
    var checked = (p.dias || []).indexOf(d) !== -1 ? " checked" : "";
    return '<label class="check"><input type="checkbox" class="p-dia" value="' + d + '"' + checked + "> " + DAY_NAMES[d] + "</label>";
  }).join("");
  var locutores = (p.locutores || []).map(function (h) {
    return '<div class="row">' +
      '<input type="text" class="p-locutor" value="' + esc(h) + '" placeholder="Locutor">' +
      '<button type="button" class="btn btn-danger btn-small" data-remove="locutor">Quitar</button>' +
    "</div>";
  }).join("");
  var contactos = (p.contactos || []).map(contactRow).join("");
  return '<div class="sub-card">' +
    '<div class="sub-card-head">' +
      '<input type="text" class="p-nombre" value="' + esc(p.nombre) + '" placeholder="Nombre del programa">' +
      '<button type="button" class="btn btn-danger btn-small" data-remove="programa">Quitar</button>' +
    "</div>" +
    '<div class="field"><label>Horario</label>' +
      '<input type="text" class="p-horario" value="' + esc(p.horario || "") + '" placeholder="Horario (ej. 10:00 - 12:00)"></div>' +
    '<div><label class="days-label">Días</label><div class="days">' + dias + "</div></div>" +
    '<div><label class="days-label">Locutores</label><div class="hosts">' + locutores + "</div>" +
      '<button type="button" class="btn btn-small" data-add="locutor">Añadir locutor</button></div>' +
    '<div><label class="days-label">Contactos</label>' + contactos +
      '<div style="margin-top: 8px;"><button type="button" class="btn btn-small" data-add="contacto-programa">Añadir contacto</button></div></div>' +
  "</div>";
}

function renderEdit() {
  var st = state.editing;
  $("list-view").hidden = true;
  $("edit-view").hidden = false;
  $("edit-title").textContent = state.isNew ? "Nueva estación" : "Editar estación";
  $("edit-banda").value = st.banda;
  $("edit-frecuencia").value = st.frecuencia;
  $("edit-nombre").value = st.nombre;
  $("edit-verificado").checked = !!st.verificado;
  $("contactos").innerHTML = (st.contactos || []).map(contactRow).join("");
  $("programas").innerHTML = (st.programas || []).map(programCard).join("");
  $("btn-delete").hidden = state.isNew;
  window.scrollTo(0, 0);
}

function collectEdit() {
  var st = {
    banda: $("edit-banda").value,
    frecuencia: $("edit-frecuencia").value.trim(),
    nombre: $("edit-nombre").value.trim(),
    verificado: $("edit-verificado").checked,
    contactos: [],
    programas: []
  };
  document.querySelectorAll("#contactos .contact-row").forEach(function (row) {
    st.contactos.push({
      tipo: row.querySelector(".c-tipo").value,
      valor: row.querySelector(".c-valor").value,
      etiqueta: row.querySelector(".c-etiqueta").value
    });
  });
  document.querySelectorAll("#programas .sub-card").forEach(function (card) {
    var p = {
      nombre: card.querySelector(".p-nombre").value.trim(),
      horario: card.querySelector(".p-horario").value.trim() || null,
      dias: [],
      locutores: [],
      contactos: []
    };
    card.querySelectorAll(".p-dia:checked").forEach(function (cb) {
      p.dias.push(parseInt(cb.value, 10));
    });
    card.querySelectorAll(".p-locutor").forEach(function (input) {
      p.locutores.push(input.value.trim());
    });
    card.querySelectorAll(".contact-row").forEach(function (row) {
      p.contactos.push({
        tipo: row.querySelector(".c-tipo").value,
        valor: row.querySelector(".c-valor").value,
        etiqueta: row.querySelector(".c-etiqueta").value
      });
    });
    st.programas.push(p);
  });
  return st;
}

function startEdit(id) {
  var st = state.estaciones.find(function (s) { return s.id === id; });
  if (!st) return;
  state.editing = clone(st);
  state.originalId = st.id;
  state.isNew = false;
  render();
}

function startNew() {
  state.editing = { banda: "FM", frecuencia: "", nombre: "", verificado: false, contactos: [], programas: [] };
  state.originalId = null;
  state.isNew = true;
  render();
}

function cancelEdit() {
  state.editing = null;
  state.isNew = false;
  state.originalId = null;
  render();
}

function saveEdit() {
  var payload = collectEdit();
  var req;
  if (state.isNew) {
    req = api("/api/estaciones", { method: "POST", body: JSON.stringify(payload) });
  } else {
    req = api("/api/estaciones/" + encodeURIComponent(state.originalId), { method: "PUT", body: JSON.stringify(payload) });
  }
  req.then(function () {
    return loadList();
  }).then(function () {
    state.editing = null;
    state.isNew = false;
    state.originalId = null;
    render();
    flash("Cambios guardados.");
  }).catch(function (err) {
    showError(err.message);
  });
}

function deleteStation(id) {
  if (!confirm("¿Eliminar esta estación?")) return;
  api("/api/estaciones/" + encodeURIComponent(id), { method: "DELETE" }).then(function () {
    return loadList();
  }).then(function () {
    render();
    flash("Estación eliminada.");
  }).catch(function (err) {
    showError(err.message);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  $("search").addEventListener("input", function () {
    state.search = this.value;
    renderList();
  });

  $("filter-all").addEventListener("click", function () { setBand("ALL"); });
  $("filter-fm").addEventListener("click", function () { setBand("FM"); });
  $("filter-am").addEventListener("click", function () { setBand("AM"); });

  function setBand(banda) {
    state.banda = banda;
    $("filter-all").classList.toggle("active", banda === "ALL");
    $("filter-fm").classList.toggle("active", banda === "FM");
    $("filter-am").classList.toggle("active", banda === "AM");
    renderList();
  }

  $("btn-new").addEventListener("click", startNew);

  $("table-body").addEventListener("click", function (e) {
    var btn = e.target.closest("button[data-action]");
    if (!btn) return;
    if (btn.dataset.action === "edit") startEdit(btn.dataset.id);
    else if (btn.dataset.action === "delete") deleteStation(btn.dataset.id);
  });

  $("edit-form").addEventListener("submit", function (e) {
    e.preventDefault();
    saveEdit();
  });

  $("btn-cancel").addEventListener("click", cancelEdit);

  $("btn-delete").addEventListener("click", function () {
    if (state.isNew) return;
    deleteStation(state.originalId);
  });

  $("btn-add-contact").addEventListener("click", function () {
    $("contactos").insertAdjacentHTML("beforeend", contactRow({ tipo: "whatsapp", valor: "", etiqueta: "" }));
  });

  $("btn-add-programa").addEventListener("click", function () {
    $("programas").insertAdjacentHTML("beforeend", programCard({ nombre: "", horario: null, dias: [], locutores: [], contactos: [] }));
  });

  $("edit-view").addEventListener("click", function (e) {
    var removeBtn = e.target.closest("button[data-remove]");
    if (removeBtn) {
      var kind = removeBtn.dataset.remove;
      if (kind === "contact") removeBtn.closest(".contact-row").remove();
      else if (kind === "locutor") removeBtn.closest(".row").remove();
      else if (kind === "programa") removeBtn.closest(".sub-card").remove();
      return;
    }
    var addBtn = e.target.closest("button[data-add]");
    if (!addBtn) return;
    if (addBtn.dataset.add === "locutor") {
      addBtn.closest(".sub-card").querySelector(".hosts").insertAdjacentHTML(
        "beforeend",
        '<div class="row"><input type="text" class="p-locutor" placeholder="Locutor">' +
        '<button type="button" class="btn btn-danger btn-small" data-remove="locutor">Quitar</button></div>'
      );
    } else if (addBtn.dataset.add === "contacto-programa") {
      addBtn.insertAdjacentHTML("beforebegin", contactRow({ tipo: "whatsapp", valor: "", etiqueta: "" }));
    }
  });

  loadList().then(render).catch(function (err) {
    showError(err.message);
  });
});