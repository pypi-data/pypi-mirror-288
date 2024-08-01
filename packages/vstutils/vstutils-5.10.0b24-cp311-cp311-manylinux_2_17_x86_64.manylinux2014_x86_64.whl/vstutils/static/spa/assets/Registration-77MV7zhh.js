import{e as w,S as g,f as n,o as y,U as b,l as h}from"./index-ChQenSU6.js";import{b as k,c as x}from"./index-DNGCnQFv.js";import{F as S}from"./FormGroup-D4NQ4Aj9.js";import{B as C}from"./BackButton-C5cHxyXp.js";const F=w({__name:"Registration",setup(_){const e=g(),{i18n:t}=k(),r=x(),s=n(),a=n(),o=n(""),d=n(""),u=n({}),i=n([]),f=n(!1);y(()=>{b(()=>{var l;(l=a.value)==null||l.setCustomValidity(o.value!==d.value?t.t("Passwords do not match."):"")})});async function v(){const l=s.value;if(l)try{const p=new URL("oauth2/registration/",r.api.url);p.search=new URLSearchParams({lang:t.locale}).toString();const m=await fetch(p,{method:"POST",body:JSON.stringify(Object.fromEntries(new FormData(l).entries())),headers:{"Content-Type":"application/json"}}),c=await m.json();u.value={},i.value=[],m.ok?c.email_confirmation_required?f.value=!0:e.push({name:"login"}):m.status===400?(u.value=c,c.detail&&(i.value=[c.detail])):i.value=["An error occurred. Please try again later."]}catch{u.value={},i.value=["An error occurred. Please try again later."]}}return{__sfc:!0,router:e,i18n:t,config:r,formEl:s,password2El:a,password1:o,password2:d,errors:u,nonFieldsErrors:i,emailConfirmationRequired:f,register:v,FormGroup:S,BackButton:C}}});var P=function(){var e=this,t=e._self._c,r=e._self._setupProxy;return r.emailConfirmationRequired?t("div",{staticStyle:{gap:"10px",display:"flex","flex-direction":"column"}},[e._v(" "+e._s(e.$t("You have successfully registered. Please check your email for a confirmation link."))+" "),t("router-link",{staticClass:"btn btn-primary btn-block",staticStyle:{"text-transform":"capitalize"},attrs:{to:{name:"login"}}},[e._v(e._s(e.$t("login")))])],1):t("form",{ref:"formEl",on:{submit:function(s){return s.preventDefault(),r.register.apply(null,arguments)}}},[t(r.FormGroup,{attrs:{label:"Username",errors:r.errors.username},scopedSlots:e._u([{key:"default",fn:function({classes:s,id:a}){return[t("input",{class:s,attrs:{id:a,autocomplete:"username",autofocus:"",name:"username",required:"",type:"text"}})]}}])}),t(r.FormGroup,{attrs:{label:"Email",errors:r.errors.email},scopedSlots:e._u([{key:"default",fn:function({classes:s,id:a}){return[t("input",{class:s,attrs:{id:a,autocomplete:"email",name:"email",required:"",type:"text"}})]}}])}),t(r.FormGroup,{attrs:{label:"Password",errors:r.errors.password},scopedSlots:e._u([{key:"default",fn:function({classes:s,id:a}){return[t("input",{directives:[{name:"model",rawName:"v-model",value:r.password1,expression:"password1"}],class:s,attrs:{id:a,autocomplete:"new-password",name:"password",required:"",type:"password"},domProps:{value:r.password1},on:{input:function(o){o.target.composing||(r.password1=o.target.value)}}})]}}])}),t(r.FormGroup,{attrs:{label:"Repeat password",errors:r.errors.password2},scopedSlots:e._u([{key:"default",fn:function({classes:s,id:a}){return[t("input",{directives:[{name:"model",rawName:"v-model",value:r.password2,expression:"password2"}],ref:"password2El",class:s,attrs:{id:a,autocomplete:"new-password",name:"password2",type:"password",required:""},domProps:{value:r.password2},on:{input:function(o){o.target.composing||(r.password2=o.target.value)}}})]}}])}),e._l(r.nonFieldsErrors,function(s,a){return t("div",{key:a,staticClass:"alert alert-danger",attrs:{role:"alert"}},[e._v(" "+e._s(e.$t(s))+" ")])}),t("button",{staticClass:"btn btn-primary btn-block",staticStyle:{"text-transform":"capitalize"}},[e._v(" "+e._s(e.$t("register"))+" ")]),t(r.BackButton)],2)},E=[],R=h(F,P,E,!1,null,null,null,null);const j=R.exports;export{j as default};
