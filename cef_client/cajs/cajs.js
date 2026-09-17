// SPDX-License-Identifier: MIT
(function () {
  if (
    typeof document.URL == "string" &&
    document.URL.startsWith("chrome-devtools://")
  ) {
    throw new Error("Don't inject into devtools.");
  }
})();
