

if(!globalThis.hostTargetList){
  globalThis.hostTargetList = ['www.python.org',
                              // 'packaging.python.org',
                               'packaging-python-org.vercel.app',
                               'packaging-python-org.weblet.repl.co',
                               //'docs.python.org',
                               'docspythonorg.weblet.repl.co',
                               'pypi.org',
                               'wwwpypaio.weblet.repl.co',
                           //    'www.pypa.io',
                               'wiki.python.org',
                               'peps.python.org',
                               'mail.python.org',
                               'bugspythonorg.weblet.repl.co',
                               'discuss.python.org',
                               'devguidepythonorg.weblet.repl.co',
                               'planetpython.org',
                               'pyfound.blogspot.com'
                              ];
}


if(/*window.location.pathname.startsWith('/installing/')&&*/
  (window.location.href.includes('docspythonorg.weblet.repl.co')||
   (window.location.href.includes('docs.python.org')))&&
  document.body.innerText.startsWith('40')){
  window.location.href=window.location.origin+'/3'+window.location.pathname+window.location.search+window.location.hash;
}
try{
  document.firstElementChild.style.filter='hue-rotate(-45deg)';

  void async function(){
    if(document.querySelector('[id="injectcss"]')){return;}
      let st=document.createElement('style');
      st.id="injectcss";
      st.innerHTML=await(await fetch('/injects.css')).text();
      document.head.appendChild(st);
  }();
   }catch(e){}
window.addEventListener("DOMContentLoaded", (event) => {try{

}catch(e){}});


setInterval(function(){

  transformLinks('href');
  transformLinks('src');
  transformLinks('action');
 
},100);



function transformLinks(attr){


 let pkgs = document.querySelectorAll('['+attr+'^="/"],['+attr+'^="./"],['+attr+'^="../"],['+attr+']:not(['+attr+'*=":"])');
  let pkgs_length = pkgs.length;
  for(let i=0;i<pkgs_length;i++){
       pkgs[i].setAttribute(attr,pkgs[i][attr]);
  }

  const hostTargetList_length = globalThis.hostTargetList.length;
  for(let i=0;i<hostTargetList_length;i++){
    pkgs = document.querySelectorAll('['+attr+'^="https://'+globalThis.hostTargetList[i]+'"]');
    pkgs_length = pkgs.length;
    for(let x=0;x<pkgs_length;x++){
      let hash='';
      if(pkgs[x][attr].includes('#')){hash='#'+pkgs[x][attr].split('#')[1];}
      let char='?';
      if(pkgs[x][attr].includes('?')){char='&';}
         pkgs[x].setAttribute(attr,
                           pkgs[x][attr].split('#')[0]
                              .replace('https://'+globalThis.hostTargetList[i],
                               window.location.origin)+
                              char+'hostname='+
                              globalThis.hostTargetList[i]+
                              hash);
    }  

  }
  
  pkgs = document.querySelectorAll('['+attr+'^="http://"]');
    pkgs_length = pkgs.length;
    for(let x=0;x<pkgs_length;x++){
      let char='?';
      if(pkgs[x][attr].includes('?')){char='&';}
         pkgs[x].setAttribute(attr,
                           pkgs[x][attr].replaceAll("http://","https://"));
    }
  
  pkgs = document.querySelectorAll('['+attr+'^="https://python.org"]');
    pkgs_length = pkgs.length;
    for(let x=0;x<pkgs_length;x++){
      let char='?';
      if(pkgs[x][attr].includes('?')){char='&';}
         pkgs[x].setAttribute(attr,
                           pkgs[x][attr].replaceAll("https://python.org","https://www.python.org"));
    }
  
  pkgs = document.querySelectorAll('['+attr+'*="packaging.python.org"],['+attr+'*="www.pypa.io"],'+
                                   '['+attr+'*="docs.python.org"],'+
                                   '['+attr+'*="bugs.python.org"],['+attr+'*="devguide.python.org"]');
    pkgs_length = pkgs.length;
    for(let x=0;x<pkgs_length;x++){
      let char='?';
      if(pkgs[x][attr].includes('?')){char='&';}
         pkgs[x].setAttribute(attr,
                           pkgs[x][attr].replaceAll("packaging.python.org","packaging-python-org.vercel.app")
     .replaceAll("www.pypa.io","wwwpypaio.weblet.repl.co")
      .replaceAll('docs.python.org','docspythonorg.weblet.repl.co')
       .replaceAll('bugs.python.org','bugspythonorg.weblet.repl.co')
        .replaceAll('devguide.python.org','devguidepythonorg.weblet.repl.co'));
    }
  
  

    if(!window.location.href.includes('hostname=')){return;}
    let localhostname = window.location.href.split('hostname=')[1].split('&')[0].split('?')[0].split('#')[0];
    pkgs = document.querySelectorAll('['+attr+'^="'+window.location.origin+'"]:not(['+attr+'*="hostname="],['+attr+'$="tour"],['+attr+'$="tour/"])');
    pkgs_length = pkgs.length;
    for(let x=0;x<pkgs_length;x++){
      let hash='';
      if(pkgs[x][attr].includes('#')){hash='#'+pkgs[x][attr].split('#')[1];}
      let char='?';
      if(pkgs[x][attr].includes('?')){char='&';}
         pkgs[x].setAttribute(attr,
                           pkgs[x][attr].split('#')[0]+char+'hostname='+localhostname+hash);
    }
  

}




void async function getPrism(){

  addEventListener("DOMContentLoaded", (event) => {
    getp();
  });  

getp();
setTimeout(function(){getp();},1);
  
}();


async function getp(){
/*nope*/return;
  
  let thisLang = 'python';
  let codes=document.querySelectorAll('pre:not([highlighted])');
  let codes_length=codes.length;
  for(let i=0;i<codes_length;i++){
    codes[i].innerHTML='<code class="language-'+thisLang+'">'+codes[i].innerHTML+'</code>';
    codes[i].setAttribute('highlighted','true');
  }

  if(!document.querySelector('[id="prismmincss"]')){
  let l=document.createElement('link');
  l.href='https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/themes/prism.min.css';
  l.rel='stylesheet';
  l.id="prismmincss";
  document.body.appendChild(l);
  }
  
  if(!document.querySelector('[id="prismminjs"]')){
  let m=document.createElement('script');
  m.src='https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/prism.min.js';
  m.id="prismminjs";
  m.onload=function(){
    if(!document.querySelector('[id="prism'+thisLang+'minjs"]')){
    let g=document.createElement('script');
    g.src='https://cdnjs.cloudflare.com/ajax/libs/prism/9000.0.1/components/prism-'+thisLang+'.min.js';
    g.id="prism"+thisLang+"minjs";
    g.onload=function(){Prism.highlightAll();};
    document.body.appendChild(g); 
    }  
  };
  document.body.appendChild(m);
  }


  


  
}