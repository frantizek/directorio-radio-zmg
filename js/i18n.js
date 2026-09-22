"use strict";

var translations = {
  es: {
    "app.title": "Directorio de Radio ZMG",
    "lang.switch": "Cambiar idioma",
    "search.placeholder": "Buscar por nombre o frecuencia...",
    "filter.all": "Todas",
    "filter.fm": "FM",
    "filter.am": "AM",
    "auth.login": "Iniciar sesi\u00f3n",
    "auth.logout": "Cerrar sesi\u00f3n",
    "auth.token_label": "Token de GitHub",
    "auth.token_help": "Pega un personal access token (fine-grained) con permisos Contents y Pull requests sobre el repositorio.",
    "auth.token_save": "Guardar token",
    "auth.cancel": "Cancelar",
    "auth.login_required": "Inicia sesi\u00f3n para editar.",
    "auth.signed_in": "Sesi\u00f3n iniciada",
    "state.loading": "Cargando...",
    "error.load": "No se pudieron cargar los datos de estaciones.",
    "error.retry": "Reintentar",
    "error.401": "Token inv\u00e1lido o expirado. Verifica que el PAT tenga permisos de Contents y Pull requests sobre el repositorio.",
    "error.403": "Sin permisos sobre el repositorio. Revisa los permisos del token.",
    "error.404": "Repositorio o archivo no encontrado. Revisa CONFIG en js/config.js.",
    "error.config": "Configura CONFIG.owner en js/config.js antes de guardar.",
    "error.generic": "Error en la API de GitHub.",
    "list.new": "Nueva estaci\u00f3n",
    "list.empty": "No se encontraron estaciones.",
    "badge.verified": "Verificado",
    "detail.back": "Volver",
    "detail.edit": "Editar",
    "detail.contacts": "Contactos",
    "detail.programs": "Programas",
    "detail.no_contacts": "Sin contactos registrados.",
    "detail.no_programs": "Sin programas registrados.",
    "program.tbd": "Por confirmar",
    "program.hosts": "Locutores",
    "program.show_contacts": "Ver contactos",
    "program.hide_contacts": "Ocultar contactos",
    "edit.title_new": "Nueva estaci\u00f3n",
    "edit.title_edit": "Editar estaci\u00f3n",
    "edit.section_station": "Estaci\u00f3n",
    "edit.band": "Banda",
    "edit.frequency": "Frecuencia",
    "edit.name": "Nombre",
    "edit.verified": "Verificada",
    "edit.contacts": "Contactos",
    "edit.contact_type": "Tipo",
    "edit.contact_value": "Valor",
    "edit.contact_label": "Etiqueta",
    "edit.add_contact": "A\u00f1adir contacto",
    "edit.remove": "Quitar",
    "edit.programs": "Programas",
    "edit.program_name": "Nombre del programa",
    "edit.program_schedule": "Horario (ej. 10:00 - 12:00)",
    "edit.add_host": "A\u00f1adir locutor",
    "edit.add_program": "A\u00f1adir programa",
    "edit.save": "Guardar cambios",
    "edit.saving": "Guardando...",
    "edit.delete": "Eliminar estaci\u00f3n",
    "edit.delete_undo": "No eliminar",
    "edit.delete_marked": "Esta estaci\u00f3n se eliminar\u00e1 al guardar.",
    "edit.cancel": "Cancelar",
    "edit.pr_success": "Cambios guardados. Abre el pull request para revisarlos:",
    "edit.open_pr": "Abrir PR",
    "common.close": "Cerrar",
    "footer.note": "Directorio de radio FM y AM de Guadalajara (ZMG). Los datos viven en GitHub.",
    "contact.telefono": "Tel\u00e9fono",
    "contact.whatsapp": "WhatsApp",
    "contact.telegram": "Telegram",
    "contact.instagram": "Instagram",
    "contact.facebook": "Facebook",
    "contact.x": "X",
    "contact.threads": "Threads",
    "contact.tiktok": "TikTok",
    "contact.youtube": "YouTube",
    "contact.tunein": "TuneIn",
    "contact.iheart": "iHeart",
    "contact.web": "Web",
    "contact.email": "Correo",
    "day.1": "Lunes",
    "day.2": "Martes",
    "day.3": "Mi\u00e9rcoles",
    "day.4": "Jueves",
    "day.5": "Viernes",
    "day.6": "S\u00e1bado",
    "day.7": "Domingo",
    "days.everyday": "Todos los d\u00edas",
    "days.weekdays": "Lunes a viernes"
  },
  en: {
    "app.title": "ZMG Radio Directory",
    "lang.switch": "Switch language",
    "search.placeholder": "Search by name or frequency...",
    "filter.all": "All",
    "filter.fm": "FM",
    "filter.am": "AM",
    "auth.login": "Sign in",
    "auth.logout": "Sign out",
    "auth.token_label": "GitHub token",
    "auth.token_help": "Paste a fine-grained personal access token with Contents and Pull requests permissions on the repository.",
    "auth.token_save": "Save token",
    "auth.cancel": "Cancel",
    "auth.login_required": "Sign in to edit.",
    "auth.signed_in": "Signed in",
    "state.loading": "Loading...",
    "error.load": "Could not load station data.",
    "error.retry": "Retry",
    "error.401": "Invalid or expired token. Make sure the PAT has Contents and Pull requests permissions on the repository.",
    "error.403": "No permission on the repository. Check your token permissions.",
    "error.404": "Repository or file not found. Check CONFIG in js/config.js.",
    "error.config": "Set CONFIG.owner in js/config.js before saving.",
    "error.generic": "GitHub API error.",
    "list.new": "New station",
    "list.empty": "No stations found.",
    "badge.verified": "Verified",
    "detail.back": "Back",
    "detail.edit": "Edit",
    "detail.contacts": "Contacts",
    "detail.programs": "Programs",
    "detail.no_contacts": "No registered contacts.",
    "detail.no_programs": "No registered programs.",
    "program.tbd": "To be confirmed",
    "program.hosts": "Hosts",
    "program.show_contacts": "Show contacts",
    "program.hide_contacts": "Hide contacts",
    "edit.title_new": "New station",
    "edit.title_edit": "Edit station",
    "edit.section_station": "Station",
    "edit.band": "Band",
    "edit.frequency": "Frequency",
    "edit.name": "Name",
    "edit.verified": "Verified",
    "edit.contacts": "Contacts",
    "edit.contact_type": "Type",
    "edit.contact_value": "Value",
    "edit.contact_label": "Label",
    "edit.add_contact": "Add contact",
    "edit.remove": "Remove",
    "edit.programs": "Programs",
    "edit.program_name": "Program name",
    "edit.program_schedule": "Schedule (e.g. 10:00 - 12:00)",
    "edit.add_host": "Add host",
    "edit.add_program": "Add program",
    "edit.save": "Save changes",
    "edit.saving": "Saving...",
    "edit.delete": "Delete station",
    "edit.delete_undo": "Undo delete",
    "edit.delete_marked": "This station will be deleted on save.",
    "edit.cancel": "Cancel",
    "edit.pr_success": "Changes saved. Open the pull request to review:",
    "edit.open_pr": "Open PR",
    "common.close": "Close",
    "footer.note": "FM and AM radio directory of Guadalajara (ZMG). The data lives on GitHub.",
    "contact.telefono": "Phone",
    "contact.whatsapp": "WhatsApp",
    "contact.telegram": "Telegram",
    "contact.instagram": "Instagram",
    "contact.facebook": "Facebook",
    "contact.x": "X",
    "contact.threads": "Threads",
    "contact.tiktok": "TikTok",
    "contact.youtube": "YouTube",
    "contact.tunein": "TuneIn",
    "contact.iheart": "iHeart",
    "contact.web": "Web",
    "contact.email": "Email",
    "day.1": "Monday",
    "day.2": "Tuesday",
    "day.3": "Wednesday",
    "day.4": "Thursday",
    "day.5": "Friday",
    "day.6": "Saturday",
    "day.7": "Sunday",
    "days.everyday": "Every day",
    "days.weekdays": "Monday to Friday"
  }
};

function detectLang() {
  try {
    var saved = localStorage.getItem("radio_lang");
    if (saved === "es" || saved === "en") return saved;
  } catch (e) {}
  var nav = String(navigator.language || "es").toLowerCase();
  if (nav.indexOf("en") === 0) return "en";
  return "es";
}

function getLang() {
  try {
    if (window.Alpine && Alpine.store("i18n")) return Alpine.store("i18n").lang;
  } catch (e) {}
  return detectLang();
}

function t(key) {
  var dict = translations[getLang()] || translations.es;
  if (Object.prototype.hasOwnProperty.call(dict, key)) return dict[key];
  if (Object.prototype.hasOwnProperty.call(translations.es, key)) return translations.es[key];
  return key;
}

function setLang(lang) {
  if (lang !== "es" && lang !== "en") return;
  try {
    if (window.Alpine && Alpine.store("i18n")) {
      Alpine.store("i18n").set(lang);
      return;
    }
  } catch (e) {}
  try { localStorage.setItem("radio_lang", lang); } catch (e) {}
  document.documentElement.lang = lang;
}

function toggleLang() {
  setLang(getLang() === "es" ? "en" : "es");
}

function otherLangLabel() {
  return getLang() === "es" ? "EN" : "ES";
}