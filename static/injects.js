
import('/boa.js');
import('/get-prism.js');
import('/favicon.js');
if(!globalThis.hostTargetList){
  globalThis.hostTargetList = ['www.python.org',
                              // 'packaging.python.org',
                               'packaging-python-org.vercel.app',
                               'packaging-python-org.weblet.repl.co',
                               //'docs.python.org',
                               'docs-python-org.weblet.repl.co',
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
  (window.location.href.includes('docs-python-org.weblet.repl.co')||
   (window.location.href.includes('docs.python.org')))&&
  document.body&&document.body.innerText.startsWith('40')){
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



async function transformLinks(attr){


 let pkgs = document.querySelectorAll('['+attr+'^="/"]:not([backup]),['+attr+'^="./"]:not([backup]),['+attr+'^="../"]:not([backup]),['+attr+']:not(['+attr+'*=":"]):not([backup])');
  let pkgs_length = pkgs.length;
  for(let i=0;i<pkgs_length;i++){
    await backupNode(pkgs[i]);
       pkgs[i].setAttribute(attr,pkgs[i][attr]);
  }

  const hostTargetList_length = globalThis.hostTargetList.length;
  for(let i=0;i<hostTargetList_length;i++){
    pkgs = document.querySelectorAll('['+attr+'^="https://'+globalThis.hostTargetList[i]+'"]:not([backup])');
    pkgs_length = pkgs.length;
    for(let x=0;x<pkgs_length;x++){
      await backupNode(pkgs[x]);
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
                              '&referer='+window.location.host+
                              hash);
    }  

  }
  
  pkgs = document.querySelectorAll('['+attr+'^="http://"]:not([backup])');
    pkgs_length = pkgs.length;
    for(let x=0;x<pkgs_length;x++){
      await backupNode(pkgs[x]);
      let char='?';
      if(pkgs[x][attr].includes('?')){char='&';}
         pkgs[x].setAttribute(attr,
                           pkgs[x][attr].replaceAll("http://","https://"));
    }
  
  pkgs = document.querySelectorAll('['+attr+'^="https://python.org"]:not([backup])');
    pkgs_length = pkgs.length;
    for(let x=0;x<pkgs_length;x++){
      await backupNode(pkgs[x]);
      let char='?';
      if(pkgs[x][attr].includes('?')){char='&';}
         pkgs[x].setAttribute(attr,
                           pkgs[x][attr].replaceAll("https://python.org","https://www.python.org"));
    }
  
  pkgs = document.querySelectorAll('['+attr+'*="packaging.python.org"]:not([backup]),['+attr+'*="www.pypa.io"],'+
                                   '['+attr+'*="docs.python.org"]:not([backup]),'+
                                   '['+attr+'*="bugs.python.org"]:not([backup]),['+attr+'*="devguide.python.org"]:not([backup])');
    pkgs_length = pkgs.length;
    for(let x=0;x<pkgs_length;x++){
      await backupNode(pkgs[x]);
      let char='?';
      if(pkgs[x][attr].includes('?')){char='&';}
         pkgs[x].setAttribute(attr,
                           pkgs[x][attr].replaceAll("packaging.python.org","packaging-python-org.vercel.app")
     .replaceAll("www.pypa.io","wwwpypaio.weblet.repl.co")
      .replaceAll('docs.python.org','docs-python-org.weblet.repl.co')
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
                           pkgs[x][attr].split('#')[0]+char+'hostname='+localhostname+'&referer='+window.location.host+hash);
    }
  

}




if(!globalThis.backupElements){globalThis.backupElements={};}
async function backupNode(element){try{
  if(element.tagName.toLowerCase()!='link'){return;}
  if(element.getAttribute('rel')!='stylesheet'){return;}
  if(document.querySelector('[href="'+element.getAttribute('href')+'"][backup]')){
await new Promise((resolve, reject) => {setTimeout(resolve,100);})

  }
  let backup = element.cloneNode(true);
  let backupId = new Date().getTime();
  backup.setAttribute('backup',backupId);
  document.head.insertBefore(backup,document.head.firstElementChild);
  backup.promise = new Promise((resolve, reject) => {
    globalThis.backupElements[''+backupId]={"promise":backup.promise,"resolve":resolve};
});
  backup.onerror = function(e){globalThis.backupElements[backupId].resolve();}
  backup.onload = function(e){globalThis.backupElements[backupId].resolve();}
  backup.style.visibility="hidden";
  document.head.insertBefore(backup,document.head.firstElementChild);
const promise1 = new Promise((resolve, reject) => {setTimeout(resolve,1000);});

  await Promise.race([backup.promise,promise1]) ;
  return;
}catch(e){
  return;
  }
}