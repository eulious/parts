const fs = require("fs");
const exec = require("child_process").exec;

const content = fs.readFileSync("index.txt", "utf8");

const output = exec("./a.out", {
  input: content,
});

console.log(output.stdout);
