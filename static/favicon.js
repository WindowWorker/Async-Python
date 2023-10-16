function changeIcon(){

  
  let icon = document.querySelector('link[rel*="icon"]:not([touched])');
  if(icon){
    icon.href = "https://raw.githubusercontent.com/Patrick-ring-motive/Async-Python-Reverse-Proxy/main/static/static/favicon.png";
    icon.setAttribute('touched','true');
  }
}

setInterval(function(){changeIcon();},100);