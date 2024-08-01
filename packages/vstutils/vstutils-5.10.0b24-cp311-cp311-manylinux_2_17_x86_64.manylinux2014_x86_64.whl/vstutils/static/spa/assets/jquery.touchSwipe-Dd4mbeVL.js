import{b as vt,r as St}from"./index-ChQenSU6.js";function Et(H,f){for(var k=0;k<f.length;k++){const v=f[k];if(typeof v!="string"&&!Array.isArray(v)){for(const S in v)if(S!=="default"&&!(S in H)){const E=Object.getOwnPropertyDescriptor(v,S);E&&Object.defineProperty(H,S,E.get?E:{enumerable:!0,get:()=>v[S]})}}}return Object.freeze(Object.defineProperty(H,Symbol.toStringTag,{value:"Module"}))}var We={exports:{}};/*!
 * @fileOverview TouchSwipe - jQuery Plugin
 * @version 1.6.18
 *
 * @author Matt Bryson http://www.github.com/mattbryson
 * @see https://github.com/mattbryson/TouchSwipe-Jquery-Plugin
 * @see http://labs.rampinteractive.co.uk/touchSwipe/
 * @see http://plugins.jquery.com/project/touchSwipe
 * @license
 * Copyright (c) 2010-2015 Matt Bryson
 * Dual licensed under the MIT or GPL Version 2 licenses.
 *
 */(function(H){(function(f){H.exports?f(St()):f(jQuery)})(function(f){var k="1.6.18",v="left",S="right",E="up",_="down",re="in",ie="out",F="none",De="auto",Oe="swipe",Pe="pinch",ae="tap",xe="doubletap",be="longtap",le="horizontal",ue="vertical",Y="all",Ye=10,ye="start",A="move",d="end",T="cancel",V="ontouchstart"in window,Q=window.navigator.msPointerEnabled&&!window.PointerEvent&&!V,R=(window.PointerEvent||window.navigator.msPointerEnabled)&&!V,N="TouchSwipe",Qe={fingers:1,threshold:75,cancelThreshold:null,pinchThreshold:20,maxTimeThreshold:null,fingerReleaseThreshold:250,longTapThreshold:500,doubleTapThreshold:200,swipe:null,swipeLeft:null,swipeRight:null,swipeUp:null,swipeDown:null,swipeStatus:null,pinchIn:null,pinchOut:null,pinchStatus:null,click:null,tap:null,doubleTap:null,longTap:null,hold:null,triggerOnTouchEnd:!0,triggerOnTouchLeave:!1,allowPageScroll:"auto",fallbackToMouseEvents:!0,excludedElements:".noSwipe",preventDefaultEvents:!0};f.fn.swipe=function(s){var G=f(this),t=G.data(N);if(t&&typeof s=="string"){if(t[s])return t[s].apply(t,Array.prototype.slice.call(arguments,1));f.error("Method "+s+" does not exist on jQuery.swipe")}else if(t&&typeof s=="object")t.option.apply(t,arguments);else if(!t&&(typeof s=="object"||!s))return Ze.apply(this,arguments);return G},f.fn.swipe.version=k,f.fn.swipe.defaults=Qe,f.fn.swipe.phases={PHASE_START:ye,PHASE_MOVE:A,PHASE_END:d,PHASE_CANCEL:T},f.fn.swipe.directions={LEFT:v,RIGHT:S,UP:E,DOWN:_,IN:re,OUT:ie},f.fn.swipe.pageScroll={NONE:F,HORIZONTAL:le,VERTICAL:ue,AUTO:De},f.fn.swipe.fingers={ONE:1,TWO:2,THREE:3,FOUR:4,FIVE:5,ALL:Y};function Ze(s){return s&&s.allowPageScroll===void 0&&(s.swipe!==void 0||s.swipeStatus!==void 0)&&(s.allowPageScroll=F),s.click!==void 0&&s.tap===void 0&&(s.tap=s.click),s||(s={}),s=f.extend({},f.fn.swipe.defaults,s),this.each(function(){var G=f(this),t=G.data(N);t||(t=new ze(this,s),G.data(N,t))})}function ze(s,t){var t=f.extend({},t),Z=V||R||!t.fallbackToMouseEvents,z=Z?R?Q?"MSPointerDown":"pointerdown":"touchstart":"mousedown",oe=Z?R?Q?"MSPointerMove":"pointermove":"touchmove":"mousemove",fe=Z?R?Q?"MSPointerUp":"pointerup":"touchend":"mouseup",I=Z?R?"mouseleave":null:"mouseleave",B=R?Q?"MSPointerCancel":"pointercancel":"touchcancel",h=0,g=null,p=null,c=0,b=0,y=0,m=1,O=0,P=0,J=null,i=f(s),l="start",o=0,u={},se=0,j=0,K=0,ce=0,L=0,W=null,X=null;try{i.on(z,he),i.on(B,C)}catch{f.error("events not supported "+z+","+B+" on jQuery.swipe")}this.enable=function(){return this.disable(),i.on(z,he),i.on(B,C),i},this.disable=function(){return Le(),i},this.destroy=function(){Le(),i.data(N,null),i=null},this.option=function(e,n){if(typeof e=="object")t=f.extend(t,e);else if(t[e]!==void 0){if(n===void 0)return t[e];t[e]=n}else if(e)f.error("Option "+e+" does not exist on jQuery.swipe.options");else return t;return null};function he(e){if(!lt()&&!(f(e.target).closest(t.excludedElements,i).length>0)){var n=e.originalEvent?e.originalEvent:e;if(!(n.pointerType&&n.pointerType=="mouse"&&t.fallbackToMouseEvents==!1)){var r,a=n.touches,x=a?a[0]:n;return l=ye,a?o=a.length:t.preventDefaultEvents!==!1&&e.preventDefault(),h=0,g=null,p=null,P=null,c=0,b=0,y=0,m=1,O=0,J=ft(),He(),te(0,x),!a||o===t.fingers||t.fingers===Y||q()?(se=M(),o==2&&(te(1,a[1]),b=y=Ee(u[0].start,u[1].start)),(t.swipeStatus||t.pinchStatus)&&(r=D(n,l))):r=!1,r===!1?(l=T,D(n,l),r):(t.hold&&(X=setTimeout(f.proxy(function(){i.trigger("hold",[n.target]),t.hold&&(r=t.hold.call(i,n,n.target))},this),t.longTapThreshold)),ee(!0),null)}}}function ge(e){var n=e.originalEvent?e.originalEvent:e;if(!(l===d||l===T||$())){var r,a=n.touches,x=a?a[0]:n,w=ke(x);if(j=M(),a&&(o=a.length),t.hold&&clearTimeout(X),l=A,o==2&&(b==0?(te(1,a[1]),b=y=Ee(u[0].start,u[1].start)):(ke(a[1]),y=Ee(u[0].end,u[1].end),P=ct(u[0].end,u[1].end)),m=st(b,y),O=Math.abs(b-y)),o===t.fingers||t.fingers===Y||!a||q()){if(g=Ge(w.start,w.end),p=Ge(w.last,w.end),Je(e,p),h=ht(w.start,w.end),c=Ve(),ot(g,h),r=D(n,l),!t.triggerOnTouchEnd||t.triggerOnTouchLeave){var me=!0;if(t.triggerOnTouchLeave){var wt=dt(this);me=pt(w.end,wt)}!t.triggerOnTouchEnd&&me?l=Te(A):t.triggerOnTouchLeave&&!me&&(l=Te(d)),(l==T||l==d)&&D(n,l)}}else l=T,D(n,l);r===!1&&(l=T,D(n,l))}}function de(e){var n=e.originalEvent?e.originalEvent:e,r=n.touches;if(r){if(r.length&&!$())return at(n),!0;if(r.length&&$())return!0}return $()&&(o=ce),j=M(),c=Ve(),ve()||!we()?(l=T,D(n,l)):t.triggerOnTouchEnd||t.triggerOnTouchEnd===!1&&l===A?(t.preventDefaultEvents!==!1&&e.cancelable!==!1&&e.preventDefault(),l=d,D(n,l)):!t.triggerOnTouchEnd&&Ce()?(l=d,U(n,l,ae)):l===A&&(l=T,D(n,l)),ee(!1),null}function C(){o=0,j=0,se=0,b=0,y=0,m=1,He(),ee(!1)}function pe(e){var n=e.originalEvent?e.originalEvent:e;t.triggerOnTouchLeave&&(l=Te(d),D(n,l))}function Le(){i.off(z,he),i.off(B,C),i.off(oe,ge),i.off(fe,de),I&&i.off(I,pe),ee(!1)}function Te(e){var n=e,r=Me(),a=we(),x=ve();return!r||x?n=T:a&&e==A&&(!t.triggerOnTouchEnd||t.triggerOnTouchLeave)?n=d:!a&&e==d&&t.triggerOnTouchLeave&&(n=T),n}function D(e,n){var r,a=e.touches;return(Ke()||Re())&&(r=U(e,n,Oe)),(je()||q())&&r!==!1&&(r=U(e,n,Pe)),rt()&&r!==!1?r=U(e,n,xe):it()&&r!==!1?r=U(e,n,be):nt()&&r!==!1&&(r=U(e,n,ae)),n===T&&C(),n===d&&(a&&a.length||C()),r}function U(e,n,r){var a;if(r==Oe){if(i.trigger("swipeStatus",[n,g||null,h||0,c||0,o,u,p]),t.swipeStatus&&(a=t.swipeStatus.call(i,e,n,g||null,h||0,c||0,o,u,p),a===!1))return!1;if(n==d&&Ae()){if(clearTimeout(W),clearTimeout(X),i.trigger("swipe",[g,h,c,o,u,p]),t.swipe&&(a=t.swipe.call(i,e,g,h,c,o,u,p),a===!1))return!1;switch(g){case v:i.trigger("swipeLeft",[g,h,c,o,u,p]),t.swipeLeft&&(a=t.swipeLeft.call(i,e,g,h,c,o,u,p));break;case S:i.trigger("swipeRight",[g,h,c,o,u,p]),t.swipeRight&&(a=t.swipeRight.call(i,e,g,h,c,o,u,p));break;case E:i.trigger("swipeUp",[g,h,c,o,u,p]),t.swipeUp&&(a=t.swipeUp.call(i,e,g,h,c,o,u,p));break;case _:i.trigger("swipeDown",[g,h,c,o,u,p]),t.swipeDown&&(a=t.swipeDown.call(i,e,g,h,c,o,u,p));break}}}if(r==Pe){if(i.trigger("pinchStatus",[n,P||null,O||0,c||0,o,m,u]),t.pinchStatus&&(a=t.pinchStatus.call(i,e,n,P||null,O||0,c||0,o,m,u),a===!1))return!1;if(n==d&&_e())switch(P){case re:i.trigger("pinchIn",[P||null,O||0,c||0,o,m,u]),t.pinchIn&&(a=t.pinchIn.call(i,e,P||null,O||0,c||0,o,m,u));break;case ie:i.trigger("pinchOut",[P||null,O||0,c||0,o,m,u]),t.pinchOut&&(a=t.pinchOut.call(i,e,P||null,O||0,c||0,o,m,u));break}}return r==ae?(n===T||n===d)&&(clearTimeout(W),clearTimeout(X),Se()&&!$e()?(L=M(),W=setTimeout(f.proxy(function(){L=null,i.trigger("tap",[e.target]),t.tap&&(a=t.tap.call(i,e,e.target))},this),t.doubleTapThreshold)):(L=null,i.trigger("tap",[e.target]),t.tap&&(a=t.tap.call(i,e,e.target)))):r==xe?(n===T||n===d)&&(clearTimeout(W),clearTimeout(X),L=null,i.trigger("doubletap",[e.target]),t.doubleTap&&(a=t.doubleTap.call(i,e,e.target))):r==be&&(n===T||n===d)&&(clearTimeout(W),L=null,i.trigger("longtap",[e.target]),t.longTap&&(a=t.longTap.call(i,e,e.target))),a}function we(){var e=!0;return t.threshold!==null&&(e=h>=t.threshold),e}function ve(){var e=!1;return t.cancelThreshold!==null&&g!==null&&(e=Fe(g)-h>=t.cancelThreshold),e}function Be(){return t.pinchThreshold!==null?O>=t.pinchThreshold:!0}function Me(){var e;return t.maxTimeThreshold&&c>=t.maxTimeThreshold?e=!1:e=!0,e}function Je(e,n){if(t.preventDefaultEvents!==!1)if(t.allowPageScroll===F)e.preventDefault();else{var r=t.allowPageScroll===De;switch(n){case v:(t.swipeLeft&&r||!r&&t.allowPageScroll!=le)&&e.preventDefault();break;case S:(t.swipeRight&&r||!r&&t.allowPageScroll!=le)&&e.preventDefault();break;case E:(t.swipeUp&&r||!r&&t.allowPageScroll!=ue)&&e.preventDefault();break;case _:(t.swipeDown&&r||!r&&t.allowPageScroll!=ue)&&e.preventDefault();break}}}function _e(){var e=Ne(),n=Ie(),r=Be();return e&&n&&r}function q(){return!!(t.pinchStatus||t.pinchIn||t.pinchOut)}function je(){return!!(_e()&&q())}function Ae(){var e=Me(),n=we(),r=Ne(),a=Ie(),x=ve(),w=!x&&a&&r&&n&&e;return w}function Re(){return!!(t.swipe||t.swipeStatus||t.swipeLeft||t.swipeRight||t.swipeUp||t.swipeDown)}function Ke(){return!!(Ae()&&Re())}function Ne(){return o===t.fingers||t.fingers===Y||!V}function Ie(){return u[0].end.x!==0}function Ce(){return!!t.tap}function Se(){return!!t.doubleTap}function qe(){return!!t.longTap}function Ue(){if(L==null)return!1;var e=M();return Se()&&e-L<=t.doubleTapThreshold}function $e(){return Ue()}function et(){return(o===1||!V)&&(isNaN(h)||h<t.threshold)}function tt(){return c>t.longTapThreshold&&h<Ye}function nt(){return!!(et()&&Ce())}function rt(){return!!(Ue()&&Se())}function it(){return!!(tt()&&qe())}function at(e){K=M(),ce=e.touches.length+1}function He(){K=0,ce=0}function $(){var e=!1;if(K){var n=M()-K;n<=t.fingerReleaseThreshold&&(e=!0)}return e}function lt(){return i.data(N+"_intouch")===!0}function ee(e){i&&(e===!0?(i.on(oe,ge),i.on(fe,de),I&&i.on(I,pe)):(i.off(oe,ge,!1),i.off(fe,de,!1),I&&i.off(I,pe,!1)),i.data(N+"_intouch",e===!0))}function te(e,n){var r={start:{x:0,y:0},last:{x:0,y:0},end:{x:0,y:0}};return r.start.x=r.last.x=r.end.x=n.pageX||n.clientX,r.start.y=r.last.y=r.end.y=n.pageY||n.clientY,u[e]=r,r}function ke(e){var n=e.identifier!==void 0?e.identifier:0,r=ut(n);return r===null&&(r=te(n,e)),r.last.x=r.end.x,r.last.y=r.end.y,r.end.x=e.pageX||e.clientX,r.end.y=e.pageY||e.clientY,r}function ut(e){return u[e]||null}function ot(e,n){e!=F&&(n=Math.max(n,Fe(e)),J[e].distance=n)}function Fe(e){if(J[e])return J[e].distance}function ft(){var e={};return e[v]=ne(v),e[S]=ne(S),e[E]=ne(E),e[_]=ne(_),e}function ne(e){return{direction:e,distance:0}}function Ve(){return j-se}function Ee(e,n){var r=Math.abs(e.x-n.x),a=Math.abs(e.y-n.y);return Math.round(Math.sqrt(r*r+a*a))}function st(e,n){var r=n/e*1;return r.toFixed(2)}function ct(){return m<1?ie:re}function ht(e,n){return Math.round(Math.sqrt(Math.pow(n.x-e.x,2)+Math.pow(n.y-e.y,2)))}function gt(e,n){var r=e.x-n.x,a=n.y-e.y,x=Math.atan2(a,r),w=Math.round(x*180/Math.PI);return w<0&&(w=360-Math.abs(w)),w}function Ge(e,n){if(Tt(e,n))return F;var r=gt(e,n);return r<=45&&r>=0||r<=360&&r>=315?v:r>=135&&r<=225?S:r>45&&r<135?_:E}function M(){var e=new Date;return e.getTime()}function dt(e){e=f(e);var n=e.offset(),r={left:n.left,right:n.left+e.outerWidth(),top:n.top,bottom:n.top+e.outerHeight()};return r}function pt(e,n){return e.x>n.left&&e.x<n.right&&e.y>n.top&&e.y<n.bottom}function Tt(e,n){return e.x==n.x&&e.y==n.y}}})})(We);var Xe=We.exports;const mt=vt(Xe),Ot=Et({__proto__:null,default:mt},[Xe]);export{Ot as j};
