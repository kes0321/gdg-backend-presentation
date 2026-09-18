const joinForm = document.querySelector("#join-form");
const nameInput = document.querySelector("#player-name");
const joinPanel = document.querySelector(".join-panel");
const gamePanel = document.querySelector("#game-panel");
const gameArea = document.querySelector("#game-area");
const playerCount = document.querySelector("#player-count");
const connectionStatus = document.querySelector("#connection-status");

let socket;
let playerId;

joinForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const name = nameInput.value.trim();
  if (!name) return;

  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  socket = new WebSocket(`${protocol}://${window.location.host}/ws`);

  socket.addEventListener("open", () => {
    socket.send(JSON.stringify({ type: "join", name }));
  });

  socket.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (message.type === "state") renderPlayers(message.players);
  });

  socket.addEventListener("close", () => {
    connectionStatus.textContent = "Connection closed.";
  });

  socket.addEventListener("error", () => {
    connectionStatus.textContent = "Could not connect to the game server.";
  });
});

function renderPlayers(players) {
  playerCount.textContent = `Players: ${players.length}`;
  gameArea.replaceChildren();

  for (const player of players) {
    const playerElement = document.createElement("div");
    playerElement.className = "player";
    playerElement.style.left = `${player.x}px`;
    playerElement.style.top = `${player.y}px`;

    const nameElement = document.createElement("span");
    nameElement.className = "player-name";
    nameElement.textContent = player.name;
    playerElement.append(nameElement);
    gameArea.append(playerElement);

    if (player.name === nameInput.value.trim()) playerId = player.id;
  }

  joinPanel.classList.add("hidden");
  gamePanel.classList.remove("hidden");
}
