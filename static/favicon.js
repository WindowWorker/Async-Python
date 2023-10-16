function changeIcon(){

  
  let icon = document.querySelector('link[rel*="icon"]:not([touched])');
  if(icon){
    icon.href = "https://raw.githubusercontent.com/Patrick-ring-motive/Async-Python-Reverse-Proxy/main/static/static/favicon.png";
    icon.setAttribute('touched','true');
  }else if(!document.querySelector('link[rel*="icon"]')){
    let link = document.createElement('link');
    link.rel = 'icon';
    link.href = 'https://raw.githubusercontent.com/Patrick-ring-motive/Async-Python-Reverse-Proxy/main/static/static/favicon.png';
    link.setAttribute('touched','true');
    document.head.appendChild(link);
  }
}

setInterval(function(){changeIcon();},100);


document.addEventListener("readystatechange", (event) => {
  changeIcon();
});

document.addEventListener("DOMContentLoaded", (event) => {
  changeIcon();
});

document.addEventListener("load", (event) => {
  changeIcon();
});

changeIcon();
