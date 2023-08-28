import * as Gluon from "@gluon-framework/gluon";

(async () => {
  const window = await Gluon.open("index.html", {
    windowSize: [800, 500],
  });
  window.ipc.log = async (msg) => {
    return "hoge" + msg;
  };
})();
