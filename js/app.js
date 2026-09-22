"use strict";

var CONTACT_TYPES = ["telefono", "whatsapp", "telegram", "instagram", "facebook", "x", "threads", "tiktok", "youtube", "tunein", "iheart", "web", "email"];

var ICON_ATTRS = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"';

var ICON_PATHS = {
  phone: '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"></path>',
  whatsapp: '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>',
  telegram: '<line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>',
  web: '<circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>',
  email: '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline>',
  check: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>',
  link: '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>'
};

function iconEl(name) {
  var path = ICON_PATHS[name] || ICON_PATHS.link;
  return '<svg class="icon" ' + ICON_ATTRS + '>' + path + '</svg>';
}

function contactIcon(tipo) {
  var name = "link";
  if (tipo === "telefono") name = "phone";
  else if (tipo === "whatsapp") name = "whatsapp";
  else if (tipo === "telegram") name = "telegram";
  else if (tipo === "web") name = "web";
  else if (tipo === "email") name = "email";
  return iconEl(name);
}

function formatPhone(value) {
  var digits = String(value || "").replace(/\D/g, "");
  if (digits.indexOf("52") === 0 && digits.length >= 12) digits = digits.slice(2);
  if (digits.indexOf("1") === 0 && digits.length === 11) digits = digits.slice(1);
  if (digits.length === 10) {
    return digits.slice(0, 2) + " " + digits.slice(2, 6) + " " + digits.slice(6);
  }
  return digits;
}

function contactDisplay(c) {
  var v = String(c.valor || "");
  if (c.tipo === "telefono" || c.tipo === "whatsapp") return formatPhone(v);
  if (c.tipo === "web") return v.replace(/^https?:\/\//, "");
  return v;
}

function contactHref(c) {
  var v = String(c.valor || "").trim();
  var handle = v.replace(/^@/, "");
  switch (c.tipo) {
    case "telefono":
      return "tel:+" + (v.indexOf("+") === 0 ? v.slice(1) : v);
    case "whatsapp":
      return "https://wa.me/" + v;
    case "telegram":
      return "https://t.me/" + handle;
    case "instagram":
      return "https://instagram.com/" + handle;
    case "facebook":
      return "https://facebook.com/" + handle;
    case "x":
      return "https://x.com/" + handle;
    case "threads":
      return "https://threads.net/" + handle;
    case "tiktok":
      return "https://tiktok.com/" + handle;
    case "youtube":
      return "https://youtube.com/" + handle;
    case "tunein":
      return "https://tunein.com/search/?query=" + encodeURIComponent(v);
    case "iheart":
      return "https://www.iheart.com/search/?q=" + encodeURIComponent(v);
    case "web": {
      var u;
      try { u = new URL(v.indexOf("//") === 0 ? "https:" + v : v); } catch (e) { return "#"; }
      return (u.protocol === "https:" || u.protocol === "http:") ? u.href : "#";
    }
    case "email":
      return "mailto:" + v;
    default:
      return "#";
  }
}

function contactBlank(c) {
  return c.tipo !== "telefono" && c.tipo !== "email";
}

function quickContacts(st) {
  var order = ["whatsapp", "telefono", "web"];
  return (st.contactos || [])
    .filter(function (c) { return order.indexOf(c.tipo) !== -1; })
    .sort(function (a, b) { return order.indexOf(a.tipo) - order.indexOf(b.tipo); });
}

function formatDays(dias) {
  if (!dias || !dias.length) return "";
  var sorted = dias.slice().sort(function (a, b) { return a - b; });
  if (sorted.length === 7) return t("days.everyday");
  if (sorted.join(",") === "1,2,3,4,5") return t("days.weekdays");
  return sorted.map(function (d) { return t("day." + d); }).join(", ");
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function normalizeContact(c) {
  var tipo = CONTACT_TYPES.indexOf(c.tipo) !== -1 ? c.tipo : "whatsapp";
  var valor = String(c.valor || "").trim().slice(0, 500);
  if (tipo === "telefono" || tipo === "whatsapp") {
    var digits = valor.replace(/\D/g, "");
    if (digits.length === 10) valor = "52" + digits;
    else if (digits.length === 12 && digits.indexOf("52") === 0) valor = digits;
    else valor = digits;
  }
  if (!valor) return null;
  var out = { tipo: tipo, valor: valor };
  if (c.etiqueta) out.etiqueta = String(c.etiqueta).trim().slice(0, 100);
  if (c.verificado) out.verificado = true;
  return out;
}

function normalizeStations(list) {
  return list.map(function (st) {
    var banda = String(st.banda || "FM").toUpperCase();
    if (banda !== "FM" && banda !== "AM") banda = "FM";
    var frecuencia = String(st.frecuencia || "").trim().slice(0, 20);
    var contactos = (st.contactos || []).map(normalizeContact).filter(Boolean);
    var programas = (st.programas || []).map(function (p) {
      return {
        nombre: String(p.nombre || "").trim().slice(0, 200),
        horario: p.horario ? String(p.horario).trim().slice(0, 200) : null,
        dias: (p.dias || []).map(Number).filter(function (d) {
          return Number.isInteger(d) && d >= 1 && d <= 7;
        }).sort(function (a, b) { return a - b; }),
        locutores: (p.locutores || []).map(function (x) { return String(x).trim().slice(0, 200); }).filter(Boolean),
        contactos: (p.contactos || []).map(normalizeContact).filter(Boolean)
      };
    }).filter(function (p) { return p.nombre; });
    return {
      id: (banda + "-" + frecuencia).toLowerCase(),
      banda: banda,
      frecuencia: frecuencia,
      nombre: String(st.nombre || "").trim().slice(0, 200),
      verificado: !!st.verificado,
      contactos: contactos,
      programas: programas
    };
  }).filter(function (st) { return st.nombre && st.frecuencia; });
}

document.addEventListener("alpine:init", function () {
  Alpine.store("i18n", {
    lang: detectLang(),
    set: function (lang) {
      this.lang = lang;
      try { localStorage.setItem("radio_lang", lang); } catch (e) {}
      document.documentElement.lang = lang;
    }
  });
  document.documentElement.lang = Alpine.store("i18n").lang;

  Alpine.data("radioDirectory", function () {
    return {
      loading: true,
      loadFailed: false,
      estaciones: [],
      search: "",
      banda: "ALL",
      view: "list",
      selectedId: null,
      openPrograms: {},
      editing: null,
      isNew: false,
      deleteMarked: false,
      showLogin: false,
      tokenInput: "",
      loginError: null,
      loginErrorKey: null,
      loggedIn: false,
      userName: "",
      saving: false,
      saveError: null,
      saveErrorKey: null,
      prUrl: null,
      savedDirect: false,

      init: function () {
        this.loggedIn = github.isLoggedIn();
        try { this.userName = localStorage.getItem(github.userKey) || ""; } catch (e) {}
        this.loadData();
      },

      loadData: async function () {
        this.loading = true;
        this.loadFailed = false;
        try {
          var res = await fetch("data/estaciones.json", { cache: "no-cache" });
          if (!res.ok) throw new Error("HTTP " + res.status);
          var data = await res.json();
          if (!data || !Array.isArray(data.estaciones)) throw new Error("bad payload");
          this.estaciones = data.estaciones;
        } catch (e) {
          this.loadFailed = true;
        } finally {
          this.loading = false;
        }
      },

      get selected() {
        var self = this;
        return this.estaciones.find(function (s) { return s.id === self.selectedId; }) || null;
      },

      get filtered() {
        var q = this.search.trim().toLowerCase();
        var banda = this.banda;
        return this.estaciones
          .filter(function (s) {
            if (banda !== "ALL" && s.banda !== banda) return false;
            if (!q) return true;
            return s.nombre.toLowerCase().indexOf(q) !== -1 ||
              String(s.frecuencia).indexOf(q) !== -1;
          })
          .sort(function (a, b) {
            if (a.banda !== b.banda) return a.banda === "FM" ? -1 : 1;
            var na = parseFloat(a.frecuencia);
            var nb = parseFloat(b.frecuencia);
            if (Number.isNaN(na)) return 1;
            if (Number.isNaN(nb)) return -1;
            return na - nb;
          });
      },

      openDetail: function (st) {
        this.selectedId = st.id;
        this.openPrograms = {};
        this.view = "detail";
        window.scrollTo(0, 0);
      },

      backToList: function () {
        this.view = "list";
        this.editing = null;
        this.deleteMarked = false;
        this.saveError = null;
        this.saveErrorKey = null;
        this.prUrl = null;
        this.savedDirect = false;
        window.scrollTo(0, 0);
      },

      toggleProgramContacts: function (i) {
        this.openPrograms[i] = !this.openPrograms[i];
      },

      openLogin: function () {
        this.showLogin = true;
        this.loginError = null;
        this.loginErrorKey = null;
        var self = this;
        this.$nextTick(function () {
          if (self.$refs.tokenInput) self.$refs.tokenInput.focus();
        });
      },

      submitLogin: async function () {
        this.loginError = null;
        this.loginErrorKey = null;
        try {
          var user = await github.login(this.tokenInput);
          this.loggedIn = true;
          this.userName = user.login || "";
          try { localStorage.setItem(github.userKey, this.userName); } catch (e) {}
          this.tokenInput = "";
          this.showLogin = false;
        } catch (err) {
          this.loginError = err.message;
          this.loginErrorKey = err.i18n || null;
          this.tokenInput = "";
        }
      },

      logout: function () {
        github.clearToken();
        try { localStorage.removeItem(github.userKey); } catch (e) {}
        this.loggedIn = false;
        this.userName = "";
        if (this.view === "edit") {
          var self = this;
          var stillHere = this.selectedId && this.estaciones.find(function (s) { return s.id === self.selectedId; });
          this.editing = null;
          this.deleteMarked = false;
          this.view = stillHere ? "detail" : "list";
        }
      },

      prepForEdit: function (st) {
        var s = clone(st);
        s.contactos = s.contactos || [];
        s.programas = (s.programas || []).map(function (p) {
          return {
            nombre: p.nombre || "",
            horario: p.horario == null ? null : p.horario,
            dias: p.dias || [],
            locutores: p.locutores || [],
            contactos: p.contactos || []
          };
        });
        return s;
      },

      startEdit: function (st) {
        if (!this.loggedIn) return;
        this.editing = this.prepForEdit(st);
        this.selectedId = st.id;
        this.isNew = false;
        this.deleteMarked = false;
        this.saveError = null;
        this.saveErrorKey = null;
        this.prUrl = null;
        this.savedDirect = false;
        this.view = "edit";
        window.scrollTo(0, 0);
      },

      startNew: function () {
        if (!this.loggedIn) return;
        this.editing = this.prepForEdit({ banda: "FM", frecuencia: "", nombre: "", verificado: false, contactos: [], programas: [] });
        this.isNew = true;
        this.deleteMarked = false;
        this.saveError = null;
        this.saveErrorKey = null;
        this.prUrl = null;
        this.savedDirect = false;
        this.view = "edit";
        window.scrollTo(0, 0);
      },

      cancelEdit: function () {
        var st = this.estaciones.find(function (s) {
          return s.id === this.selectedId;
        }.bind(this));
        this.editing = null;
        this.deleteMarked = false;
        this.prUrl = null;
        this.savedDirect = false;
        this.view = (!this.isNew && st) ? "detail" : "list";
        window.scrollTo(0, 0);
      },

      addContact: function () {
        this.editing.contactos.push({ tipo: "whatsapp", valor: "", etiqueta: "" });
      },

      addProgram: function () {
        this.editing.programas.push({ nombre: "", horario: null, dias: [], locutores: [], contactos: [] });
      },

      addHost: function (p) {
        p.locutores.push("");
      },

      addProgramContact: function (p) {
        p.contactos.push({ tipo: "whatsapp", valor: "", etiqueta: "" });
      },

      toggleDeleteMark: function () {
        this.deleteMarked = !this.deleteMarked;
      },

      save: async function () {
        if (this.saving) return;
        if (!github.isLoggedIn()) {
          this.saveError = t("auth.login_required");
          this.saveErrorKey = "auth.login_required";
          return;
        }
        this.saving = true;
        this.saveError = null;
        this.saveErrorKey = null;
        try {
          var editingId = this.editing.id;
          var normEditing = normalizeStations([clone(this.editing)])[0] || null;
          if (!normEditing) {
            this.saveError = t("error.incomplete");
            this.saveErrorKey = "error.incomplete";
            return;
          }
          var list;
          if (this.deleteMarked && !this.isNew) {
            list = this.estaciones.filter(function (s) { return s.id !== editingId; });
          } else if (this.isNew) {
            list = this.estaciones.slice();
            list.push(this.editing);
          } else {
            list = this.estaciones.map(function (s) {
              return s.id === editingId ? clone(this.editing) : s;
            }, this);
          }
          list = normalizeStations(list);
          var duplicates = list.filter(function (s) { return s.id === normEditing.id; }).length > 1;
          if (duplicates) {
            this.saveError = t("error.duplicate");
            this.saveErrorKey = "error.duplicate";
            return;
          }
          var prUrl = await github.saveChanges(list);
          this.estaciones = list;
          this.prUrl = prUrl;
          this.savedDirect = !prUrl;
          if (this.deleteMarked && !this.isNew) {
            this.editing = null;
            this.deleteMarked = false;
            this.selectedId = null;
            this.view = "list";
          } else {
            this.selectedId = normEditing.id;
            this.editing = null;
            this.isNew = false;
            this.view = "detail";
          }
        } catch (err) {
          this.saveError = err.message;
          this.saveErrorKey = err.i18n || null;
        } finally {
          this.saving = false;
        }
      }
    };
  });
});