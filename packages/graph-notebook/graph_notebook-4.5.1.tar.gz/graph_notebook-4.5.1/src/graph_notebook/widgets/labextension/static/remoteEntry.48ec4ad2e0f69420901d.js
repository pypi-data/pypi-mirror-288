var _JUPYTERLAB;(()=>{"use strict";var e,r,t,o,n,a,i,f,s,u,d,l,c,h,p,v,g,b,m,y,w,k,j,S={69:(e,r,t)=>{var o={"./index":()=>Promise.all([t.e(612),t.e(934),t.e(509)]).then((()=>()=>t(509))),"./extension":()=>Promise.all([t.e(612),t.e(934),t.e(122)]).then((()=>()=>t(122)))},n=(e,r)=>(t.R=r,r=t.o(o,e)?o[e]():Promise.resolve().then((()=>{throw new Error('Module "'+e+'" does not exist in container.')})),t.R=void 0,r),a=(e,r)=>{if(t.S){var o="default",n=t.S[o];if(n&&n!==e)throw new Error("Container initialization failed as it has already been initialized with a different share scope");return t.S[o]=e,t.I(o,r)}};t.d(r,{get:()=>n,init:()=>a})}},_={};function E(e){var r=_[e];if(void 0!==r)return r.exports;var t=_[e]={id:e,loaded:!1,exports:{}};return S[e].call(t.exports,t,t.exports,E),t.loaded=!0,t.exports}E.m=S,E.c=_,E.d=(e,r)=>{for(var t in r)E.o(r,t)&&!E.o(e,t)&&Object.defineProperty(e,t,{enumerable:!0,get:r[t]})},E.f={},E.e=e=>Promise.all(Object.keys(E.f).reduce(((r,t)=>(E.f[t](e,r),r)),[])),E.u=e=>e+"."+{122:"fc08b4dbecf908890e0b",509:"5b2cd676ea356af98dd4",543:"6c537ab2c3fc874b1b35",612:"126cd4ef04c3319b5d00",692:"edd4283fa264c17ec1cc",911:"f1ebd162cb2a9d2cf8bf",934:"0cff004c1b822b288ed9"}[e]+".js?v="+{122:"fc08b4dbecf908890e0b",509:"5b2cd676ea356af98dd4",543:"6c537ab2c3fc874b1b35",612:"126cd4ef04c3319b5d00",692:"edd4283fa264c17ec1cc",911:"f1ebd162cb2a9d2cf8bf",934:"0cff004c1b822b288ed9"}[e],E.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),E.o=(e,r)=>Object.prototype.hasOwnProperty.call(e,r),e={},r="graph_notebook_widgets:",E.l=(t,o,n,a)=>{if(e[t])e[t].push(o);else{var i,f;if(void 0!==n)for(var s=document.getElementsByTagName("script"),u=0;u<s.length;u++){var d=s[u];if(d.getAttribute("src")==t||d.getAttribute("data-webpack")==r+n){i=d;break}}i||(f=!0,(i=document.createElement("script")).charset="utf-8",i.timeout=120,E.nc&&i.setAttribute("nonce",E.nc),i.setAttribute("data-webpack",r+n),i.src=t),e[t]=[o];var l=(r,o)=>{i.onerror=i.onload=null,clearTimeout(c);var n=e[t];if(delete e[t],i.parentNode&&i.parentNode.removeChild(i),n&&n.forEach((e=>e(o))),r)return r(o)},c=setTimeout(l.bind(null,void 0,{type:"timeout",target:i}),12e4);i.onerror=l.bind(null,i.onerror),i.onload=l.bind(null,i.onload),f&&document.head.appendChild(i)}},E.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},E.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),(()=>{E.S={};var e={},r={};E.I=(t,o)=>{o||(o=[]);var n=r[t];if(n||(n=r[t]={}),!(o.indexOf(n)>=0)){if(o.push(n),e[t])return e[t];E.o(E.S,t)||(E.S[t]={});var a=E.S[t],i="graph_notebook_widgets",f=(e,r,t,o)=>{var n=a[e]=a[e]||{},f=n[r];(!f||!f.loaded&&(!o!=!f.eager?o:i>f.from))&&(n[r]={get:t,from:i,eager:!!o})},s=[];return"default"===t&&(f("feather-icons","4.28.0",(()=>E.e(911).then((()=>()=>E(911))))),f("graph_notebook_widgets","4.5.1",(()=>Promise.all([E.e(612),E.e(934),E.e(509)]).then((()=>()=>E(509))))),f("jquery","3.6.0",(()=>E.e(692).then((()=>()=>E(692))))),f("lodash","4.17.21",(()=>E.e(543).then((()=>()=>E(543)))))),e[t]=s.length?Promise.all(s).then((()=>e[t]=1)):1}}})(),(()=>{var e;E.g.importScripts&&(e=E.g.location+"");var r=E.g.document;if(!e&&r&&(r.currentScript&&(e=r.currentScript.src),!e)){var t=r.getElementsByTagName("script");if(t.length)for(var o=t.length-1;o>-1&&(!e||!/^http(s?):/.test(e));)e=t[o--].src}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),E.p=e})(),t=e=>{var r=e=>e.split(".").map((e=>+e==e?+e:e)),t=/^([^-+]+)?(?:-([^+]+))?(?:\+(.+))?$/.exec(e),o=t[1]?r(t[1]):[];return t[2]&&(o.length++,o.push.apply(o,r(t[2]))),t[3]&&(o.push([]),o.push.apply(o,r(t[3]))),o},o=(e,r)=>{e=t(e),r=t(r);for(var o=0;;){if(o>=e.length)return o<r.length&&"u"!=(typeof r[o])[0];var n=e[o],a=(typeof n)[0];if(o>=r.length)return"u"==a;var i=r[o],f=(typeof i)[0];if(a!=f)return"o"==a&&"n"==f||"s"==f||"u"==a;if("o"!=a&&"u"!=a&&n!=i)return n<i;o++}},n=e=>{var r=e[0],t="";if(1===e.length)return"*";if(r+.5){t+=0==r?">=":-1==r?"<":1==r?"^":2==r?"~":r>0?"=":"!=";for(var o=1,a=1;a<e.length;a++)o--,t+="u"==(typeof(f=e[a]))[0]?"-":(o>0?".":"")+(o=2,f);return t}var i=[];for(a=1;a<e.length;a++){var f=e[a];i.push(0===f?"not("+s()+")":1===f?"("+s()+" || "+s()+")":2===f?i.pop()+" "+i.pop():n(f))}return s();function s(){return i.pop().replace(/^\((.+)\)$/,"$1")}},a=(e,r)=>{if(0 in e){r=t(r);var o=e[0],n=o<0;n&&(o=-o-1);for(var i=0,f=1,s=!0;;f++,i++){var u,d,l=f<e.length?(typeof e[f])[0]:"";if(i>=r.length||"o"==(d=(typeof(u=r[i]))[0]))return!s||("u"==l?f>o&&!n:""==l!=n);if("u"==d){if(!s||"u"!=l)return!1}else if(s)if(l==d)if(f<=o){if(u!=e[f])return!1}else{if(n?u>e[f]:u<e[f])return!1;u!=e[f]&&(s=!1)}else if("s"!=l&&"n"!=l){if(n||f<=o)return!1;s=!1,f--}else{if(f<=o||d<l!=n)return!1;s=!1}else"s"!=l&&"n"!=l&&(s=!1,f--)}}var c=[],h=c.pop.bind(c);for(i=1;i<e.length;i++){var p=e[i];c.push(1==p?h()|h():2==p?h()&h():p?a(p,r):!h())}return!!h()},i=(e,r)=>e&&E.o(e,r),f=e=>(e.loaded=1,e.get()),s=e=>Object.keys(e).reduce(((r,t)=>(e[t].eager&&(r[t]=e[t]),r)),{}),u=(e,r,t,n)=>{var i=n?s(e[r]):e[r];return(r=Object.keys(i).reduce(((e,r)=>!a(t,r)||e&&!o(e,r)?e:r),0))&&i[r]},d=(e,r,t)=>{var n=t?s(e[r]):e[r];return Object.keys(n).reduce(((e,r)=>!e||!n[e].loaded&&o(e,r)?r:e),0)},l=(e,r,t,o)=>"Unsatisfied version "+t+" from "+(t&&e[r][t].from)+" of shared singleton module "+r+" (required "+n(o)+")",c=(e,r,t,o,a)=>{var i=e[t];return"No satisfying version ("+n(o)+")"+(a?" for eager consumption":"")+" of shared module "+t+" found in shared scope "+r+".\nAvailable versions: "+Object.keys(i).map((e=>e+" from "+i[e].from)).join(", ")},h=e=>{throw new Error(e)},p=e=>{"undefined"!=typeof console&&console.warn&&console.warn(e)},g=(e,r,t)=>t?t():((e,r)=>h("Shared module "+r+" doesn't exist in shared scope "+e))(e,r),b=(v=e=>function(r,t,o,n,a){var i=E.I(r);return i&&i.then&&!o?i.then(e.bind(e,r,E.S[r],t,!1,n,a)):e(r,E.S[r],t,o,n,a)})(((e,r,t,o,n,a)=>{if(!i(r,t))return g(e,t,a);var s=u(r,t,n,o);return s?f(s):a?a():void h(c(r,e,t,n,o))})),m=v(((e,r,t,o,n,s)=>{if(!i(r,t))return g(e,t,s);var u=d(r,t,o);return a(n,u)||p(l(r,t,u,n)),f(r[t][u])})),y={},w={93:()=>m("default","@jupyter-widgets/base",!1,[,[1,4],[1,3],[1,2],1,1]),148:()=>b("default","feather-icons",!1,[4,4,28,0],(()=>E.e(911).then((()=>()=>E(911))))),226:()=>b("default","jquery",!1,[,[-1,4,0,0],[0,1,8,0],2],(()=>E.e(692).then((()=>()=>E(692))))),916:()=>b("default","lodash",!1,[4,4,17,21],(()=>E.e(543).then((()=>()=>E(543))))),992:()=>b("default","jquery",!1,[4,3,6,0],(()=>E.e(692).then((()=>()=>E(692)))))},k={934:[93,148,226,916,992]},j={},E.f.consumes=(e,r)=>{E.o(k,e)&&k[e].forEach((e=>{if(E.o(y,e))return r.push(y[e]);if(!j[e]){var t=r=>{y[e]=0,E.m[e]=t=>{delete E.c[e],t.exports=r()}};j[e]=!0;var o=r=>{delete y[e],E.m[e]=t=>{throw delete E.c[e],r}};try{var n=w[e]();n.then?r.push(y[e]=n.then(t).catch(o)):t(n)}catch(e){o(e)}}}))},(()=>{var e={117:0};E.f.j=(r,t)=>{var o=E.o(e,r)?e[r]:void 0;if(0!==o)if(o)t.push(o[2]);else{var n=new Promise(((t,n)=>o=e[r]=[t,n]));t.push(o[2]=n);var a=E.p+E.u(r),i=new Error;E.l(a,(t=>{if(E.o(e,r)&&(0!==(o=e[r])&&(e[r]=void 0),o)){var n=t&&("load"===t.type?"missing":t.type),a=t&&t.target&&t.target.src;i.message="Loading chunk "+r+" failed.\n("+n+": "+a+")",i.name="ChunkLoadError",i.type=n,i.request=a,o[1](i)}}),"chunk-"+r,r)}};var r=(r,t)=>{var o,n,[a,i,f]=t,s=0;if(a.some((r=>0!==e[r]))){for(o in i)E.o(i,o)&&(E.m[o]=i[o]);f&&f(E)}for(r&&r(t);s<a.length;s++)n=a[s],E.o(e,n)&&e[n]&&e[n][0](),e[n]=0},t=self.webpackChunkgraph_notebook_widgets=self.webpackChunkgraph_notebook_widgets||[];t.forEach(r.bind(null,0)),t.push=r.bind(null,t.push.bind(t))})(),E.nc=void 0;var P=E(69);(_JUPYTERLAB=void 0===_JUPYTERLAB?{}:_JUPYTERLAB).graph_notebook_widgets=P})();