(function () {
  if (
    typeof document.URL == "string" &&
    document.URL.startsWith("chrome-devtools://")
  ) {
    throw new Error("Don't inject into devtools.");
  }
})();

function testSync() {
  const test2 = "testSync";
  return test2;
}
