function confirmar() {
  const pop_up = document.getElementById("popup");
  const Main = document.querySelector("main");

  pop_up.classList.toggle("active");
  Main.classList.toggle("blur");
}
