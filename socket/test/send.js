const child_process = require("child_process");
const fs = require("fs");

const content = fs.readFileSync("input.txt", "utf8");

const cmd = child_process.spawn("./a.out", {
  cwd: ".",
  env: process.env,
});

cmd.stdout.setEncoding("utf8");

const callback = {
  resolve: () => undefined,
  reject: () => undefined,
};

cmd.stdout.on("data", (data) => {
  callback.resolve(data);
  callback.resolve = () => undefined;
});

cmd.stderr.on("data", (data) => {
  callback.reject(data);
  callback.reject = () => undefined;
});

function send(data) {
  const promise = new Promise((resolve, reject) => {
    callback.resolve = (response) => resolve(response);
    callback.reject = (error) => reject(error);
  });
  cmd.stdin.write(data + "\n");
  return promise;
}

(async () => {
  console.log("start");
  for (let i = 0; i < 100; i++) {
    console.log(i);
    console.log(await send(content));
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }
})();
