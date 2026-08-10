import { copyFile, mkdir } from "node:fs/promises";
import { dirname, join } from "node:path";

const root = new URL("../dist/", import.meta.url).pathname;
const pages = [
  {
    from: "writing/task-positive-programming/index.html",
    to: "2024/11/01/Task-Positive-Programming.html",
  },
  {
    from: "writing/human-memory/index.html",
    to: "2024/12/04/Human-Memory.html",
  },
];

for (const page of pages) {
  const destination = join(root, page.to);
  await mkdir(dirname(destination), { recursive: true });
  await copyFile(join(root, page.from), destination);
}
