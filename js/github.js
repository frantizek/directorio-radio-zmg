"use strict";

var github = {
  tokenKey: "github_token",
  userKey: "github_user",

  getToken: function () {
    try { return localStorage.getItem(this.tokenKey) || ""; } catch (e) { return ""; }
  },

  setToken: function (token) {
    try { localStorage.setItem(this.tokenKey, token); } catch (e) {}
  },

  clearToken: function () {
    try { localStorage.removeItem(this.tokenKey); } catch (e) {}
  },

  isLoggedIn: function () {
    return !!this.getToken();
  },

  api: async function (path, options) {
    options = options || {};
    var headers = Object.assign({}, options.headers, {
      Authorization: "Bearer " + this.getToken(),
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28"
    });
    if (options.body) headers["Content-Type"] = "application/json";
    var res = await fetch("https://api.github.com" + path, Object.assign({}, options, { headers: headers }));
    if (!res.ok) {
      var apiMessage = "";
      try {
        var data = await res.json();
        apiMessage = data.message || "";
      } catch (e) {}
      if (res.status === 401) this.clearToken();
      throw this.errorFrom(res.status, apiMessage, res.headers);
    }
    if (res.status === 204) return null;
    return res.json();
  },

  errorFrom: function (status, apiMessage, headers) {
    var key = null;
    if (status === 429 || (status === 403 && headers && headers.get("x-ratelimit-remaining") === "0")) {
      key = "error.rate_limit";
    } else if (status === 401) {
      key = "error.401";
    } else if (status === 403) {
      key = "error.403";
    } else if (status === 404) {
      key = "error.404";
    } else if (status === 422 || status === 409) {
      key = "error.conflict";
    }
    var err = new Error(key ? t(key) : (apiMessage || t("error.generic")));
    if (key) err.i18n = key;
    err.status = status;
    return err;
  },

  simpleError: function (key) {
    var err = new Error(t(key));
    err.i18n = key;
    return err;
  },

  login: async function (token) {
    var clean = String(token || "").trim();
    var res = await fetch("https://api.github.com/user", {
      method: "GET",
      headers: {
        Authorization: "Bearer " + clean,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
      }
    });
    if (!res.ok) {
      var apiMessage = "";
      try {
        var data = await res.json();
        apiMessage = data.message || "";
      } catch (e) {}
      throw this.errorFrom(res.status, apiMessage, res.headers);
    }
    var user = await res.json();
    this.setToken(clean);
    return user;
  },

  saveChanges: async function (estaciones) {
    if (!this.getToken()) throw this.simpleError("auth.login_required");
    if (!this.validConfig()) throw this.simpleError("error.config");

    var owner = CONFIG.owner;
    var repo = CONFIG.repo;
    var path = CONFIG.dataPath;

    var repoInfo = await this.api("/repos/" + owner + "/" + repo);
    var baseBranch = repoInfo.default_branch;
    var canPush = !!(repoInfo.permissions && repoInfo.permissions.push);

    var content = toBase64(JSON.stringify({ estaciones: estaciones }, null, 2) + "\n");

    if (canPush) {
      var fileSha;
      try {
        var file = await this.api("/repos/" + owner + "/" + repo + "/contents/" + path + "?ref=" + encodeURIComponent(baseBranch));
        fileSha = file.sha;
      } catch (e) {
        if (e.status !== 404) throw e;
      }
      var putBody = {
        message: "Actualizar directorio de estaciones desde el frontend",
        content: content,
        branch: baseBranch
      };
      if (fileSha) putBody.sha = fileSha;
      await this.api("/repos/" + owner + "/" + repo + "/contents/" + path, {
        method: "PUT",
        body: JSON.stringify(putBody)
      });
      return null;
    }

    var refInfo = await this.api("/repos/" + owner + "/" + repo + "/git/ref/heads/" + baseBranch.split("/").map(encodeURIComponent).join("/"));
    var baseSha = refInfo.object.sha;

    var branch = "edit/directorio-" + Date.now() + "-" + Math.random().toString(36).slice(2, 8);
    try {
      await this.api("/repos/" + owner + "/" + repo + "/git/refs", {
        method: "POST",
        body: JSON.stringify({ ref: "refs/heads/" + branch, sha: baseSha })
      });

      var fileSha;
      try {
        var file = await this.api("/repos/" + owner + "/" + repo + "/contents/" + path + "?ref=" + encodeURIComponent(branch));
        fileSha = file.sha;
      } catch (e) {
        if (e.status !== 404) throw e;
      }

      var putBody = {
        message: "Actualizar directorio de estaciones desde el frontend",
        content: content,
        branch: branch
      };
      if (fileSha) putBody.sha = fileSha;
      await this.api("/repos/" + owner + "/" + repo + "/contents/" + path, {
        method: "PUT",
        body: JSON.stringify(putBody)
      });

      var pr = await this.api("/repos/" + owner + "/" + repo + "/pulls", {
        method: "POST",
        body: JSON.stringify({
          title: "Actualizar directorio de estaciones",
          head: branch,
          base: baseBranch,
          body: "Cambios generados desde la interfaz web del directorio de radio."
        })
      });

      return pr.html_url;
    } catch (err) {
      try {
        await this.api("/repos/" + owner + "/" + repo + "/git/refs/heads/" + branch, { method: "DELETE" });
      } catch (e) {}
      throw err;
    }
  },

  validConfig: function () {
    return /^[\w.-]+$/.test(CONFIG.owner) &&
      /^[\w.-]+$/.test(CONFIG.repo) &&
      /^[\w./-]+$/.test(CONFIG.dataPath);
  }
};

function toBase64(str) {
  var bytes = new TextEncoder().encode(str);
  var binary = "";
  for (var i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}