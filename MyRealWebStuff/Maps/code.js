function selectSite(e)
{
  for (i = 0; i < items.length; i++)
  {
    items[i].classList.remove("selected");
  }
  let itemSelected = e.target.parentElement.title;
  itemSelected = itemSelected.replace(" ", "_");
  itemSelected = document.getElementById(itemSelected);
  itemSelected.classList.toggle("selected");
}
let list = document.getElementsByTagName("gmp-advanced-marker");
let items = document.getElementsByClassName("item");
console.log(items.length)
for (i = 0; i < list.length; i++) {
  list[i].addEventListener("click", selectSite);
}