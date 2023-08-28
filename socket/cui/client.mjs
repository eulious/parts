import { spawn } from "child_process";

class CppProcess {
  constructor() {
    this.cmd = spawn("./echo.py", {
      cwd: ".",
      env: process.env,
    });
    this.queue = [];
    this.cmd.stdout.setEncoding("utf-8");
    this.cmd.stdout.on("data", (data) => {
      console.log("out", data);
      this.queue[0](data.trim());
      this.queue.shift();
    });
  }

  async send(data) {
    const promise = new Promise((resolve) => {
      this.queue.push(resolve);
    });
    this.cmd.stdin.write(data + "\n");
    return promise;
  }

  quit() {
    this.cmd.stdout.destroy();
    this.cmd.stderr.destroy();
    this.cmd.kill("SIGINT");
  }
}

(async () => {
  const cpp = new CppProcess();
  await cpp.send("1");
  await cpp.send("2");
  await cpp.send("3");
  console.log(await cpp.send("4"));
  cpp.quit();
})();
