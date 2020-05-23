//汤峻侬 搜索功能修改
const input = document.querySelector(".finder__input");
const finder = document.querySelector(".finder");
const form = document.querySelector("#search_form");


input.addEventListener("focus", () => {
  finder.classList.add("active");
});

input.addEventListener("blur", () => {
  if (input.value.length === 0) {
    finder.classList.remove("active");
  }
});

function search(){
  finder.classList.add("processing");
  finder.classList.remove("active");

  setTimeout(() => {
    finder.classList.remove("processing");
    input.disabled = false;
    if (input.value.length > 0) {
      finder.classList.add("active");
    }
  }, 1000);
  window.setTimeout('form.submit();', 1000);
}

form.addEventListener("submit", (ev) => {

  ev.preventDefault();

  finder.classList.add("processing");
  finder.classList.remove("active");

  setTimeout(() => {
    finder.classList.remove("processing");
    input.disabled = false;
    if (input.value.length > 0) {
      finder.classList.add("active");
    }

  }, 1000);

  window.setTimeout('form.submit();', 1000);

});
