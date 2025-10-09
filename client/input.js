const socket = new WebSocket("ws://localhost:9000");

socket.onopen = () => console.log("Connected to input server");

document.addEventListener("keydown", (e) => {
  socket.send(JSON.stringify({ type: "key", key: e.key, action: "down" }));
});

document.addEventListener("keyup", (e) => {
  socket.send(JSON.stringify({ type: "key", key: e.key, action: "up" }));
});

document.addEventListener("mousemove", (e) => {
  socket.send(
    JSON.stringify({
      type: "mouse_move",
      dx: e.movementX,
      dy: e.movementY,
    })
  );
});

document.addEventListener("mousedown", (e) => {
  const button = e.button === 0 ? "left" : "right";
  socket.send(JSON.stringify({ type: "mouse_click", button, action: "down" }));
});

document.addEventListener("mouseup", (e) => {
  const button = e.button === 0 ? "left" : "right";
  socket.send(JSON.stringify({ type: "mouse_click", button, action: "up" }));
});
