"use strict";

var translations = {
  es: {
    "app.title": "Directorio de Radio ZMG",
    "lang.switch": "Cambiar idioma",
    "search.placeholder": "Buscar por nombre o frecuencia...",
    "filter.all": "Todas",
    "filter.fm": "FM",
    "filter.am": "AM",
    "state.loading": "Cargando...",
    "error.load": "No se pudieron cargar los datos de estaciones.",
    "error.retry": "Reintentar",
    "list.empty": "No se encontraron estaciones.",
    "badge.verified": "Verificado",
    "detail.back": "Volver",
    "detail.contacts": "Contactos",
    "detail.programs": "Programas",
    "detail.no_contacts": "Sin contactos registrados.",
    "detail.no_programs": "Sin programas registrados.",
    "program.tbd": "Por confirmar",
    "program.hosts": "Locutores",
    "program.days": "D\u00edas",
    "program.show_contacts": "Ver contactos",
    "program.hide_contacts": "Ocultar contactos",
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
    "state.loading": "Loading...",
    "error.load": "Could not load station data.",
    "error.retry": "Retry",
    "list.empty": "No stations found.",
    "badge.verified": "Verified",
    "detail.back": "Back",
    "detail.contacts": "Contacts",
    "detail.programs": "Programs",
    "detail.no_contacts": "No registered contacts.",
    "detail.no_programs": "No registered programs.",
    "program.tbd": "To be confirmed",
    "program.hosts": "Hosts",
    "program.days": "Days",
    "program.show_contacts": "Show contacts",
    "program.hide_contacts": "Hide contacts",
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