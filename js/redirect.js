source.addEventListener(
  "last-item",
  function(event) {
    source.close();
    redirect(event.data);
  },
  false
);

function redirect(url) {
  //document.location = url;
  document.location.replace(url);
}
