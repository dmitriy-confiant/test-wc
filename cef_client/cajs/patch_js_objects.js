(function (originalFunction) {
  window.setTimeout = function setTimeout(...params) {
    var originalResult = originalFunction.call(this, ...params);

    if (params.length < 2) {
      return originalResult;
    }

    var pFunc = params[0];
    var pMillisec = params[1];

    if (typeof pFunc == "function") {
      var funcStr = pFunc.toString();
      if (cajsNoodle.isSafeTimeoutFunc(funcStr)) {
        return originalResult;
      }

      var rHex = cajsNoodle.findHex(funcStr);
      var rUni = cajsNoodle.findUnicode(funcStr);
      if (rHex.length > 1 || rUni.length > 1) {
        var signalItem = cajsNoodle.addNewSignalItem(
          cajsNoodle.signals.ENCODED_STRINGS
        );
        cajsNoodle.addUniqueItem(
          signalItem.data.names,
          `setTimeout(function, ${pMillisec}) => hex=${rHex.length}, unicode=${rUni.length}`
        );
        cajsNoodle.addUniqueItem(signalItem.data.params, funcStr);
      }

      if (pMillisec > 89 * 1000 && pMillisec < 599 * 1000) {
        var signalItem = cajsNoodle.addNewSignalItem(
          cajsNoodle.signals.LONG_TIMEOUT
        );
        cajsNoodle.addUniqueItem(
          signalItem.data.names,
          `setTimeout(function, ${pMillisec})`
        );
        cajsNoodle.addUniqueItem(signalItem.data.params, funcStr);
      }
    }

    return originalResult;
  };

  cajsNoodle.installFunctionProxy("window.setTimeout");
})(window.setTimeout);

function testSync() {
  const test = "testSync2";
  return test;
}
