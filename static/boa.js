async function boaImages(){

  if(!document.querySelector('[id="boa-styles"]')){
    let the={};
    the['boa-styles'] = document.createElement('style');
  
    the['boa-styles'].innerHTML = `

img[src*="python" i]:not([from="wikipedia"]){
visibility:hidden;
}

    
    img[from="wikipedia"]{
    width:unset !important;
    height:unset !important;
    }

    
    a:has(img[from="wikipedia"]){
    width:min-content;
    height:min-content;
    display:inline-flex;

    }
    
    a:has(img[from="wikipedia"])::after{
    content:"Boa";
    
    }
    `;
    the['boa-styles'].id='boa-styles';
    document.body.appendChild(the['boa-styles']);
  }

  let snakes = document.querySelectorAll('img[src*="python" i]:not([from="wikipedia"])');
  let snakes_length = snakes.length;
  for(let i=0;i<snakes_length;i++){
    let size=Math.max(Math.min(snakes[i].naturalWidth,snakes[i].naturalHeight),12)+'px';
    snakes[i].style.maxWidth=size;
    snakes[i].style.maxHeight=size;
    snakes[i].setAttribute('from','wikipedia');
    snakes[i].src='https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg';

  

  }

  
}

function boa(el){
  if(!el){return;}
  var n, a=[], walk=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,null,false);
  while(n=walk.nextNode()){ 
  a.push(n);
    let ntext=n.textContent;

  ntext=ntext.replace(/python/gi,'Boa');

  if(ntext!=n.textContent){
    n.textContent=ntext;
  }

  };
  if(document.title.toLowerCase().includes('python')){
    document.title=document.title.replace(/python/gi,'Boa');
  }
  boaImages();
  return a;
}


boa(document.body);

setInterval(async function(){
boa(document.body);
},100);


document.addEventListener("readystatechange", (event) => {
  boa(document.body);
});

document.addEventListener("DOMContentLoaded", (event) => {
  boa(document.body);
});

document.addEventListener("load", (event) => {
  boa(document.body);
});



