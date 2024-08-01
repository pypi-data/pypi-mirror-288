import{openBlock as l,createElementBlock as p,unref as t,createElementVNode as e,renderSlot as Q,defineComponent as M,ref as w,onMounted as P,watchEffect as N,resolveComponent as O,createVNode as _,withCtx as y,createTextVNode as C,toDisplayString as s,createCommentVNode as z,normalizeClass as Y,Fragment as B,renderList as F,createBlock as S,computed as E,Teleport as j,withModifiers as L,createApp as oe}from"vue";import{d as R,aj as H,_ as J,p as T,P as se,aF as re,g as Z,a as X,o as ae,ag as x,aG as ne,aH as le,e as W,I as ie,a8 as de,M as ce,aI as ue,V as _e,aJ as me,aK as K,aL as fe,aM as be,aN as ee,aO as he,aP as pe,aQ as ve,ao as ge,aR as $e,aS as ye,au as we,ap as ke,ax as G,ai as ze,ay as Ae,az as Me,aA as Ce,U as Re,aT as Ie,aU as Se,aB as qe,aC as Oe,aD as Te}from"./sentry.5.1.1.dev24290.js";import"./_commonjsHelpers.5.1.1.dev24290.js";function zs(){import.meta.url,import("_").catch(()=>1);async function*v(){}}const Be=["aria-label"],Pe={class:"fr-breadcrumb__list"},D={__name:"Breadcrumb",setup(v){const{t:o}=R();return(r,i)=>(l(),p("nav",{rol:"navigation","aria-label":t(o)("You're here:"),class:"fr-breadcrumb fr-mb-5v"},[e("ol",Pe,[Q(r.$slots,"default")])],8,Be))}},Ue={class:"fr-container--fluid"},Ve={key:0},Ee={class:"fr-breadcrumb__link","aria-current":"page"},He={class:"fr-alert fr-alert--info"},De={class:"fr-alert__title"},Le=M({__name:"Datasets",props:{oid:{}},setup(v){const{t:o}=R(),r=v,i="/admin/organization/".concat(r.oid,"/"),a=w(null),n=w(null);return P(async()=>a.value=await H()),N(()=>{var c,d;n.value=(d=(c=a.value)==null?void 0:c.organizations.find(b=>b.id===r.oid))!=null?d:null}),(c,d)=>{const b=O("router-link");return l(),p("div",Ue,[_(D,null,{default:y(()=>[e("li",null,[_(b,{class:"fr-breadcrumb__link",to:"/"},{default:y(()=>[C(s(t(o)("Administration")),1)]),_:1})]),n.value?(l(),p("li",Ve,[_(b,{class:"fr-breadcrumb__link",to:"/"},{default:y(()=>[C(s(n.value.name),1)]),_:1})])):z("",!0),e("li",null,[e("a",Ee,s(t(o)("Datasets")),1)])]),_:1}),e("div",He,[e("h3",De,s(t(o)("This is a WIP page")),1),e("p",null,[e("a",{href:i},s(t(o)("You can manage your datasets on the current admin.")),1)])])])}}}),Ne={class:"fr-container--fluid"},je={key:0},We={class:"fr-breadcrumb__link","aria-current":"page"},Ye={class:"fr-alert fr-alert--info"},Fe={class:"fr-alert__title"},Ge=M({__name:"Reuses",props:{oid:{}},setup(v){const{t:o}=R(),r=v,i="/admin/organization/".concat(r.oid,"/"),a=w(null),n=w(null);return P(async()=>a.value=await H()),N(()=>{var c,d;n.value=(d=(c=a.value)==null?void 0:c.organizations.find(b=>b.id===r.oid))!=null?d:null}),(c,d)=>{const b=O("router-link");return l(),p("div",Ne,[_(D,null,{default:y(()=>[e("li",null,[_(b,{class:"fr-breadcrumb__link",to:"/"},{default:y(()=>[C(s(t(o)("Administration")),1)]),_:1})]),n.value?(l(),p("li",je,[_(b,{class:"fr-breadcrumb__link",to:"/"},{default:y(()=>[C(s(n.value.name),1)]),_:1})])):z("",!0),e("li",null,[e("a",We,s(t(o)("Reuses")),1)])]),_:1}),e("div",Ye,[e("h3",Fe,s(t(o)("This is a WIP page")),1),e("p",null,[e("a",{href:i},s(t(o)("You can manage your reuses on the current admin.")),1)])])])}}}),Je={class:"fr-container--fluid"},Ze={class:"fr-breadcrumb__link","aria-current":"page"},Ke={key:0,class:"fr-h1"},Qe={class:"fr-alert fr-alert--info"},Xe={class:"fr-alert__title"},xe={href:"/admin/me/"},et=M({__name:"Me",setup(v){const{t:o}=R(),r=w(null);return P(async()=>r.value=await H()),(i,a)=>{const n=O("router-link");return l(),p("div",Je,[_(D,null,{default:y(()=>[e("li",null,[_(n,{class:"fr-breadcrumb__link",to:"/"},{default:y(()=>[C(s(t(o)("Administration")),1)]),_:1})]),e("li",null,[e("a",Ze,s(t(o)("Me")),1)])]),_:1}),r.value?(l(),p("h1",Ke,s(r.value.first_name)+" "+s(r.value.last_name),1)):z("",!0),e("div",Qe,[e("h3",Xe,s(t(o)("This is a WIP page")),1),e("p",null,[e("a",xe,s(t(o)("You can edit your profil on the current admin.")),1)])])])}}}),tt={class:"fr-sidemenu__item"},ot=["innerHTML"],st=M({__name:"AdminSidebarLink",props:{label:{},icon:{},iconHtml:{},to:{}},setup(v){return(o,r)=>{const i=O("router-link");return l(),p("li",tt,[e("div",{class:Y([{"fr-icon-svg fr-icon--sm":o.iconHtml},"fr-enlarge-link fr-sidemenu__link fr-mb-1w"])},[o.iconHtml?(l(),p("div",{key:0,class:"fr-mr-1w fr-grid-row",innerHTML:o.iconHtml},null,8,ot)):o.icon?(l(),p("div",{key:1,class:Y([o.icon,"fr-mr-1w fr-icon--sm"]),"aria-hidden":"true"},null,2)):z("",!0),_(i,{to:o.to},{default:y(()=>[C(s(o.label),1)]),_:1},8,["to"])],2)])}}});const V=J(st,[["__scopeId","data-v-6240fbee"]]),rt='<svg width="24" height="24" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">\n<path d="M5 12V18C5 18 5 21 12 21C19 21 19 18 19 18V12" stroke="currentColor" stroke-width="1.5"/>\n<path d="M5 6V12C5 12 5 15 12 15C19 15 19 12 19 12V6" stroke="currentColor" stroke-width="1.5"/>\n<path d="M12 3C19 3 19 6 19 6C19 6 19 9 12 9C5 9 5 6 5 6C5 6 5 3 12 3Z" stroke="currentColor" stroke-width="1.5"/>\n</svg>\n',at=["aria-expanded","aria-controls","aria-current"],nt={class:"logo logo--sm"},lt={class:"fr-mx-1w fr-col text-overflow-ellipsis"},it=["id"],dt={class:"fr-sidemenu__list fr-mx-1w fr-my-3v"},ct=M({__name:"AdminSidebarOrganizationMenu",props:{organization:{},isOpened:{type:Boolean}},setup(v){const{t:o}=R(),r=T("organization-menu");return(i,a)=>(l(),p("li",{class:Y(["fr-sidemenu__item",{"fr-sidemenu__item--active":i.isOpened}])},[e("button",{class:"fr-sidemenu__btn","aria-expanded":i.isOpened,"aria-controls":t(r),"aria-current":i.isOpened},[e("div",nt,[_(se,{type:"organization",src:i.organization.logo_thumbnail,size:20},null,8,["src"])]),e("p",lt,s(i.organization.name),1)],8,at),e("div",{class:"fr-collapse","data-fr-js-collapse":"",id:t(r)},[e("ul",dt,[_(V,{iconHtml:t(rt),label:t(o)("Datasets"),to:{name:"organization-datasets",params:{oid:i.organization.id}}},null,8,["iconHtml","label","to"]),_(V,{icon:"fr-icon-line-chart-line",label:t(o)("Reuses"),to:{name:"organization-reuses",params:{oid:i.organization.id}}},null,8,["label","to"]),_(V,{icon:"fr-icon-parent-line",label:t(o)("Members"),to:{name:"organization-members",params:{oid:i.organization.id}}},null,8,["label","to"]),_(V,{icon:"fr-icon-user-line",label:t(o)("Profile"),to:{name:"organization-profile",params:{oid:i.organization.id}}},null,8,["label","to"])])],8,it)],2))}});const ut=J(ct,[["__scopeId","data-v-dc2a4e61"]]),_t={class:"fr-container--fluid h-100"},mt={class:"fr-grid-row h-100 bg-grey-50"},ft={class:"fr-col-12 fr-col-md-4 fr-col-lg-3 fr-col-xl-2"},bt=["aria-label"],ht={class:"fr-sidemenu__inner"},pt=["aria-controls"],vt=["id"],gt={class:"fr-sidemenu__list"},$t={class:"fr-sidemenu__item"},yt=["aria-controls"],wt={class:"fr-mx-1v"},kt=["id"],zt={class:"fr-col-12 fr-col-md-8 fr-col-lg-9 fr-col-xl-10 h-100 fr-px-2w"},At=M({__name:"Admin",setup(v){const{t:o}=R(),r=re(),i=T("menu"),a=T("profil-submenu"),n=w(null),c=w(null);function d(b){return b===c.value}return P(async()=>{n.value=await H(),n.value.organizations.length>0&&(r.params.oid?c.value=r.params.oid:c.value=n.value.organizations[0].id)}),(b,$)=>{const A=O("router-view");return l(),p("div",_t,[e("div",mt,[e("div",ft,[e("nav",{class:"fr-sidemenu","aria-label":t(o)("Administration menu")},[e("div",ht,[e("button",{class:"fr-sidemenu__btn",hidden:"","aria-controls":t(i),"aria-expanded":"false"},s(t(o)("Open menu")),9,pt),e("div",{class:"fr-collapse",id:t(i)},[e("ul",gt,[e("li",$t,[e("button",{class:"fr-sidemenu__btn border-bottom border-default-grey","aria-expanded":"false","aria-controls":t(a)},[_(Z,{user:t(X),size:24,rounded:!0},null,8,["user"]),e("p",wt,s(t(o)("My Profil")),1)],8,yt),e("div",{class:"fr-collapse",id:t(a)},[_(V,{icon:"fr-icon-account-circle-line",label:t(o)("Me"),to:"/me"},null,8,["label"])],8,kt)]),n.value?(l(!0),p(B,{key:0},F(n.value.organizations,m=>(l(),S(ut,{organization:m,"is-opened":d(m.id)},null,8,["organization","is-opened"]))),256)):z("",!0)])],8,vt)])],8,bt)]),e("div",zt,[(l(),S(A,{key:t(r).fullPath}))])])])}}});const Mt=J(At,[["__scopeId","data-v-7df981bd"]]),Ct={class:"fr-grid-row fr-grid-row--gutters fr-grid-row--middle"},te=M({__name:"AdminDangerZone",setup(v){return(o,r)=>(l(),S(t(ae),{color:"error",type:"secondary",weight:"regular"},{default:y(()=>[e("div",Ct,[Q(o.$slots,"default")])]),_:3}))}}),Rt=["aria-labelledby","id"],It={class:"fr-container fr-container--fluid fr-container-md"},St={class:"fr-grid-row fr-grid-row--center"},qt={class:"fr-col-12 fr-col-md-8"},Ot={class:"fr-modal__body"},Tt={class:"fr-modal__header"},Bt=["title","aria-controls"],Pt={class:"fr-modal__content"},Ut=["id"],Vt={class:"fr-grid-row fr-grid-row--middle fr-text--bold fr-mb-2w"},Et={class:"fr-col"},Ht={class:"fr-col-auto"},Dt=["disabled"],Lt={class:"fr-col"},Nt={class:"fr-m-0 text-grey-500"},jt={class:"fr-m-0 fr-text--xs text-default-error"},Wt={class:"fr-col-auto"},Yt=["disabled"],Ft=M({__name:"AdminEditMemberModal",props:{id:{},member:{},oid:{},roles:{}},emits:["memberUpdated"],setup(v,{emit:o}){const r=v,i=o,a=E(()=>"fr-modal-title-user-"+r.id),{t:n}=R(),{toast:c}=W(),d=w(!1);async function b(u){if(!u.newRole){m();return}try{d.value=!0,await ne(r.oid,u.user.id,u.newRole),i("memberUpdated"),m()}catch(h){c.error(n("An error occurred while update member role."))}finally{d.value=!1}}async function $(u){try{d.value=!0,await le(r.oid,u.user.id),i("memberUpdated")}catch(h){c.error(n("An error occurred while removing this member."))}finally{d.value=!1}}function A(u){return r.roles.map(h=>{const g={...h};return g.value===u&&(g.selected=!0),g})}function m(){d.value=!1;const u=document.getElementById(r.id);globalThis.dsfr(u).modal.conceal()}return(u,h)=>(l(),S(j,{to:"body"},[e("dialog",{"aria-labelledby":a.value,role:"dialog",id:u.id,class:"fr-modal"},[e("div",It,[e("div",St,[e("div",qt,[e("div",Ot,[e("div",Tt,[e("button",{class:"fr-btn--close fr-btn",title:t(n)("Close the modal dialog"),"aria-controls":u.id},s(t(n)("Close")),9,Bt)]),e("div",Pt,[e("h1",{id:a.value,class:"fr-modal__title fr-mb-2w"},s(t(n)("Edit member")),9,Ut),e("p",Vt,[_(Z,{class:"fr-mr-1v",user:u.member.user,rounded:!0,size:24},null,8,["user"]),C(" "+s(u.member.user.first_name)+" "+s(u.member.user.last_name),1)]),e("form",{class:"fr-grid-row fr-grid-row--gutters fr-grid-row--bottom",onSubmit:h[1]||(h[1]=L(g=>b(u.member),["prevent"]))},[e("div",Et,[u.roles.length>0?(l(),S(x,{key:0,label:t(n)("Role of the member"),"model-value":u.member.role,"onUpdate:modelValue":h[0]||(h[0]=g=>u.member.newRole=g),options:A(u.member.role)},null,8,["label","model-value","options"])):z("",!0)]),e("div",Ht,[e("button",{class:"fr-btn",type:"submit",disabled:d.value},s(t(n)("Validate")),9,Dt)])],32),_(te,{class:"fr-mt-2w"},{default:y(()=>[e("div",Lt,[e("p",Nt,s(t(n)("Remove member from the organization")),1),e("p",jt,s(t(n)("Be careful, this action can't be reverse.")),1)]),e("div",Wt,[e("button",{class:"fr-btn fr-btn--secondary fr-btn--secondary--error fr-btn--icon-left fr-icon-logout-box-r-line",disabled:d.value,onClick:h[2]||(h[2]=g=>$(u.member))},s(t(n)("Remove member")),9,Yt)])]),_:1})])])])])])],8,Rt)]))}}),Gt=["aria-controls"],Jt=M({__name:"AdminEditMemberButton",props:{member:{},oid:{},roles:{}},emits:["memberUpdated"],setup(v){const o=v,{t:r}=R(),i=E(()=>"fr-modal-user-"+o.member.user.id);return(a,n)=>(l(),p(B,null,[e("button",{class:"fr-btn fr-btn--sm fr-btn--tertiary-no-outline fr-icon-pencil-line","data-fr-opened":"false","aria-controls":i.value},s(t(r)("Edit")),9,Gt),_(Ft,{id:i.value,member:a.member,oid:a.oid,roles:a.roles,onMemberUpdated:n[0]||(n[0]=c=>a.$emit("memberUpdated"))},null,8,["id","member","oid","roles"])],64))}}),Zt={class:"fr-mt-n9v fr-mb-2w"},Kt={class:"fr-badge fr-badge--info fr-badge--no-icon"},Qt=e("span",{class:"fr-icon-user-add-line","aria-hidden":"true"},null,-1),Xt={class:"fr-grid-row fr-grid-row--gutters fr-grid-row--middle"},xt={class:"fr-col"},eo={class:"fr-grid-row fr-grid-row--middle"},to={class:"fr-ml-3v fr-mt-1-5v fr-mb-0 filet filet-default-grey fr-text--sm"},oo={key:0,class:"fr-col-auto fr-grid-row flex-direction-column"},so=["disabled"],ro=["disabled","aria-controls"],ao=["aria-labelledby","id"],no={class:"fr-container fr-container--fluid fr-container-md"},lo={class:"fr-grid-row fr-grid-row--center"},io={class:"fr-col-12 fr-col-md-8"},co={class:"fr-modal__body"},uo={class:"fr-modal__header"},_o=["title","aria-controls"],mo={class:"fr-modal__content"},fo=["id"],bo={class:"fr-grid-row fr-grid-row--gutters fr-grid-row--right"},ho={class:"fr-col-auto"},po=["disabled"],vo={class:"fr-col-auto"},go=["disabled"],$o=M({__name:"AdminMembershipRequest",props:{loading:{type:Boolean},oid:{},request:{},showActions:{type:Boolean}},emits:["accept","refuse"],setup(v,{emit:o}){const r=v,i=o,{t:a}=R(),n=w(""),c=T("modal"),d=T("modalTitle");function b(){const m=document.getElementById(c);globalThis.dsfr(m).modal.conceal()}function $(){i("refuse",r.request.id,n.value),b()}function A(){n.value="",b()}return(m,u)=>{const h=O("AdminMembershipRequest",!0);return l(),S(ie,{class:"drop-shadow rounded-xxs fr-mt-3w"},{default:y(()=>[e("div",Zt,[e("p",Kt,[Qt,C(" "+s(t(a)("Membership Request")),1)])]),e("div",Xt,[e("div",xt,[e("div",eo,[_(Z,{class:"fr-mr-1v",user:m.request.user,rounded:!0,size:24},null,8,["user"]),C(" "+s(t(a)("{fullName} asks to join the organization.",{fullName:m.request.user.first_name+" "+m.request.user.last_name})),1)]),e("div",to,s(m.request.comment),1)]),m.showActions?(l(),p("div",oo,[e("button",{class:"fr-btn fr-btn--sm fr-btn--icon-left fr-mb-1w fr-icon-check-line",onClick:u[0]||(u[0]=g=>m.$emit("accept",m.request.id)),disabled:m.loading,"data-testid":"accept"},s(t(a)("Accept request")),9,so),e("button",{class:"fr-btn fr-btn--icon-left fr-btn--sm fr-btn--secondary fr-btn--secondary--error fr-icon-close-line",disabled:m.loading,"data-fr-opened":"false","aria-controls":t(c),"data-testid":"refuse"},s(t(a)("Refuse")),9,ro),(l(),S(j,{to:"body"},[e("dialog",{"aria-labelledby":t(d),role:"dialog",id:t(c),class:"fr-modal","data-testid":"modal"},[e("div",no,[e("div",lo,[e("div",io,[e("div",co,[e("div",uo,[e("button",{class:"fr-btn--close fr-btn",title:t(a)("Close the modal dialog"),"aria-controls":t(c),onClick:L(A,["prevent"])},s(t(a)("Close")),9,_o)]),e("div",mo,[e("h1",{id:t(d),class:"fr-modal__title fr-mb-2w"},s(t(a)("Refuse membership request")),9,fo),_(h,{class:"fr-mt-4w fr-mb-2w",loading:!1,oid:m.oid,request:m.request,"show-actions":!1},null,8,["oid","request"]),e("form",{onSubmit:L($,["prevent"]),onReset:A},[_(de,{label:t(a)("You can provide the refusal reason:"),modelValue:n.value,"onUpdate:modelValue":u[1]||(u[1]=g=>n.value=g),"data-testid":"comment-group"},null,8,["label","modelValue"]),e("div",bo,[e("div",ho,[e("button",{class:"fr-btn fr-btn--secondary fr-btn--secondary-grey-500",type:"reset",disabled:m.loading,"data-testid":"cancel-modal-button"},s(t(a)("Cancel")),9,po)]),e("div",vo,[e("button",{class:"fr-btn",type:"submit",disabled:m.loading,"data-testid":"refuse-modal-button"},s(t(a)("Refuse request")),9,go)])])],32)])])])])])],8,ao)]))])):z("",!0)])]),_:1})}}}),yo=["aria-labelledby","id"],wo={class:"fr-container fr-container--fluid fr-container-md"},ko={class:"fr-grid-row fr-grid-row--center"},zo={class:"fr-col-12 fr-col-md-8"},Ao={class:"fr-modal__body"},Mo={class:"fr-modal__header"},Co=["title","aria-controls"],Ro={class:"fr-modal__content"},Io=["id"],So={class:"fr-modal__footer"},qo={class:"fr-btns-group fr-btns-group--right fr-btns-group--sm fr-btns-group--inline-lg fr-btns-group--icon-left"},Oo=["disabled"],To=["disabled"],Bo=M({__name:"AdminAddMemberModal",props:{id:{},oid:{},roles:{}},emits:["memberAdded"],setup(v,{emit:o}){const r=v,i=o,{t:a}=R(),{toast:n}=W(),c=w(!1),d=w(),b=w("editor"),$=E(()=>"fr-modal-title-user-"+r.id);async function A(){try{c.value=!0,d.value&&(await ue(r.oid,d.value,b.value),i("memberAdded"),u())}catch(h){n.error(a("An error occurred while update member role."))}finally{c.value=!1}}function m(h){return h.map(g=>{var k;const f={...g,avatar_thumbnail:(k=g.avatar_url)!=null?k:void 0};return{value:f.id,label:f.first_name+" "+f.last_name,image:_e(f,32)}})}function u(){c.value=!1,d.value=void 0,b.value="editor";const h=document.getElementById(r.id);globalThis.dsfr(h).modal.conceal()}return(h,g)=>(l(),S(j,{to:"body"},[e("dialog",{"aria-labelledby":$.value,role:"dialog",id:h.id,class:"fr-modal"},[e("div",wo,[e("div",ko,[e("div",zo,[e("div",Ao,[e("div",Mo,[e("button",{class:"fr-btn--close fr-btn",title:t(a)("Close the modal dialog"),"aria-controls":h.id},s(t(a)("Close")),9,Co)]),e("form",{onSubmit:L(A,["prevent"])},[e("div",Ro,[e("h1",{id:$.value,class:"fr-modal__title fr-mb-2w"},s(t(a)("Add member to the organization")),9,Io),_(ce,{placeholder:h.$t("Search a user"),searchPlaceholder:h.$t("Search a user..."),suggestUrl:"/users/suggest/",values:d.value,onChange:g[0]||(g[0]=f=>d.value=f),allOption:h.$t("Select a user"),addAllOption:!1,onSuggest:m,roundedImages:!0},null,8,["placeholder","searchPlaceholder","values","allOption"]),h.roles.length>0?(l(),S(x,{key:0,label:t(a)("Role of the member"),"model-value":b.value,"onUpdate:modelValue":g[1]||(g[1]=f=>b.value=f),options:h.roles},null,8,["label","model-value","options"])):z("",!0)]),e("div",So,[e("div",qo,[e("button",{class:"fr-btn fr-btn--secondary fr-btn--secondary-grey-500",type:"button",onClick:u,disabled:c.value},s(t(a)("Cancel")),9,Oo),e("button",{class:"fr-btn",type:"submit",disabled:c.value},s(t(a)("Add to the organization")),9,To)])])],32)])])])])],8,yo)]))}}),Po=["aria-controls"],Uo=M({__name:"AdminAddMemberButton",props:{oid:{},roles:{}},emits:["memberAdded"],setup(v){const o=v,{t:r}=R(),i=E(()=>"fr-modal-add-user-"+o.oid);return(a,n)=>(l(),p(B,null,[e("button",{class:"fr-btn fr-btn--sm fr-btn--icon-left fr-icon-add-line","data-fr-opened":"false","aria-controls":i.value},s(t(r)("Add member")),9,Po),_(Bo,{id:i.value,oid:a.oid,roles:a.roles,onMemberAdded:n[0]||(n[0]=c=>a.$emit("memberAdded"))},null,8,["id","oid","roles"])],64))}}),Vo={key:0},Eo=e("li",null,null,-1),Ho={class:"fr-grid-row fr-grid-row--gutters fr-grid-row--middle justify-center"},Do={class:"fr-col-12 fr-col-md"},Lo={class:"fr-h1 fr-mb-2w"},No={key:0,class:"fr-col-auto"},jo={class:"subtitle subtitle--uppercase"},Wo={class:"subtitle subtitle--uppercase fr-mt-2w fr-mb-1v"},Yo={class:"fr-table fr-table--layout-fixed"},Fo={scope:"col"},Go={scope:"col"},Jo={key:0,scope:"col"},Zo={class:"fr-badge"},Ko={key:0},Qo=M({__name:"Members",props:{oid:{}},setup(v){const o=v,{t:r}=R(),{toast:i}=W(),a=w([]),n=E(()=>me||b.value.some(f=>{var k;return f.user.id===((k=X)==null?void 0:k.id)&&f.role==="admin"})),c=w([]),d={name:"SomeName"},b=w([]),$=w(!1);function A(f){var k,I;return(I=(k=c.value.find(q=>q.value===f))==null?void 0:k.label)!=null?I:f}async function m(){const f=await ee(o.oid);b.value=f.members}async function u(){const f=await K(o.oid);a.value=f}async function h(f){$.value=!0;const k=[];try{await he(o.oid,f),k.push(u()),k.push(m())}catch(I){i.error(r("An error occurred while accepting this membership."))}finally{Promise.all(k).finally(()=>$.value=!1)}}async function g(f,k){$.value=!0;const I=[];try{await pe(o.oid,f,k),I.push(u()),I.push(m())}catch(q){i.error(r("An error occurred while refusing this membership."))}finally{Promise.all(I).finally(()=>$.value=!1)}}return N(()=>{n.value&&K(o.oid).then(f=>a.value=f)}),P(()=>{fe().then(be).then(f=>c.value=f),m()}),(f,k)=>{const I=O("router-link");return l(),p("div",null,[_(D,null,{default:y(()=>[e("li",null,[_(I,{class:"fr-breadcrumb__link",to:"/"},{default:y(()=>[C(s(t(r)("Administration")),1)]),_:1})]),d?(l(),p("li",Vo,[_(I,{class:"fr-breadcrumb__link",to:"/"},{default:y(()=>[C(s(d.name),1)]),_:1})])):z("",!0),Eo]),_:1}),e("div",Ho,[e("div",Do,[e("h1",Lo,s(t(r)("Members")),1)]),n.value?(l(),p("div",No,[_(Uo,{oid:f.oid,roles:c.value,onMemberAdded:m},null,8,["oid","roles"])])):z("",!0)]),a.value.length?(l(),p(B,{key:0},[e("h2",jo,s(t(r)("{n} requests",{n:a.value.length})),1),(l(!0),p(B,null,F(a.value,q=>(l(),S($o,{class:"fr-mb-4w",key:q.id,loading:$.value,oid:f.oid,request:q,"show-actions":!0,onAccept:h,onRefuse:g},null,8,["loading","oid","request"]))),128))],64)):z("",!0),e("h2",Wo,s(t(r)("{n} members",{n:b.value.length})),1),e("div",Yo,[e("table",null,[e("thead",null,[e("tr",null,[e("th",Fo,s(t(r)("Members")),1),e("th",Go,s(t(r)("Status")),1),n.value?(l(),p("th",Jo,s(t(r)("Action")),1)):z("",!0)])]),e("tbody",null,[(l(!0),p(B,null,F(b.value,q=>(l(),p("tr",{key:q.user.id},[e("td",null,s(q.user.first_name)+" "+s(q.user.last_name),1),e("td",null,[e("p",Zo,s(A(q.role)),1)]),n.value?(l(),p("td",Ko,[_(Jt,{member:q,oid:f.oid,roles:c.value,onMemberUpdated:m},null,8,["member","oid","roles"])])):z("",!0)]))),128))])])])])}}}),Xo={class:"fr-container--fluid"},xo={key:0},es={class:"fr-breadcrumb__link","aria-current":"page"},ts=["id"],os=["disabled","onClick"],ss={class:"fr-col"},rs={class:"fr-m-0 text-grey-500"},as={class:"fr-m-0 fr-text--xs text-default-error"},ns={class:"fr-col-auto"},ls=["disabled","aria-controls"],is=["aria-labelledby","id"],ds={class:"fr-container fr-container--fluid fr-container-md"},cs={class:"fr-grid-row fr-grid-row--center"},us={class:"fr-col-12 fr-col-md-8"},_s={class:"fr-modal__body"},ms={class:"fr-modal__header"},fs=["title","aria-controls"],bs={class:"fr-modal__content"},hs=["id"],ps={class:"fr-text--bold"},vs={class:"fr-modal__footer"},gs={class:"fr-btns-group fr-btns-group--right fr-btns-group--inline-reverse fr-btns-group--inline-lg fr-btns-group--icon-left"},$s=["disabled"],ys=M({__name:"Profile",props:{oid:{}},setup(v){const{t:o}=R(),{toast:r}=W(),i=v,a=ve(),n=w(null),c=w(null),d=w(null),b=w([]),$=w(!1),A=T("modal"),m=T("modalTitle");function u(){d.value&&($.value=!0,$e(d.value.id).then(()=>{a.replace("/"),window.location.reload()}).catch(()=>r.error(o("An error occured when deleting the organization."))).finally(()=>$.value=!1))}function h(g,f){$.value=!0,ye(g).then(()=>r.success(o("Organization updated !"))).catch(()=>r.error(o("An error occured when updating the organization."))).finally(()=>$.value=!1)}return P(async()=>n.value=await H()),N(async()=>{d.value=await ee(i.oid)}),(g,f)=>{const k=O("router-link");return l(),p("div",Xo,[_(D,null,{default:y(()=>[e("li",null,[_(k,{class:"fr-breadcrumb__link",to:"/"},{default:y(()=>[C(s(t(o)("Administration")),1)]),_:1})]),d.value?(l(),p("li",xo,[_(k,{class:"fr-breadcrumb__link",to:"/"},{default:y(()=>[C(s(d.value.name),1)]),_:1})])):z("",!0),e("li",null,[e("a",es,s(t(o)("Profile")),1)])]),_:1}),c.value?(l(),p("h2",{key:0,class:"subtitle subtitle--uppercase fr-mb-5v",id:c.value.legend},s(t(o)("Edit profile")),9,ts)):z("",!0),d.value?(l(),S(ge,{key:1,organization:d.value,errors:b.value,showLegend:!1,showWell:!1,ref_key:"form",ref:c,onSubmit:h},{submitButton:y(({submit:I})=>[e("button",{class:"fr-btn fr-btn--icon-left fr-icon-save-line",disabled:$.value,"data-testid":"submitButton",onClick:I},s(t(o)("Save")),9,os)]),default:y(()=>[_(te,{class:"fr-mt-6w"},{default:y(()=>[e("div",ss,[e("p",rs,s(t(o)("Delete the organization")),1),e("p",as,s(t(o)("Be careful, this action can't be reverse.")),1)]),e("div",ns,[e("button",{class:"fr-btn fr-btn--secondary fr-btn--secondary--error fr-btn--icon-left fr-icon-delete-line",disabled:$.value,"data-fr-opened":"false","aria-controls":t(A)},s(t(o)("Delete")),9,ls),(l(),S(j,{to:"body"},[e("dialog",{"aria-labelledby":t(m),role:"dialog",id:t(A),class:"fr-modal"},[e("div",ds,[e("div",cs,[e("div",us,[e("div",_s,[e("div",ms,[e("button",{class:"fr-btn--close fr-btn",title:t(o)("Close the modal dialog"),"aria-controls":t(A)},s(t(o)("Close")),9,fs)]),e("div",bs,[e("h1",{id:t(m),class:"fr-modal__title fr-mb-2w"},s(t(o)("Are you sure you want to delete this organization ?")),9,hs),e("p",ps,s(t(o)("This action can't be reverse.")),1),e("p",null,s(t(o)("All content published with this organization will stay online, with the same URL but in an anonymous form, i.e. without being linked to a data producer.")),1),e("p",null,s(t(o)("If you want to delete your published content too, start by deleting the contents before deleting your account.")),1)]),e("div",vs,[e("div",gs,[e("button",{class:"fr-btn fr-btn--secondary fr-btn--secondary--error",role:"button",disabled:$.value,onClick:u},s(t(o)("Delete")),9,$s)])])])])])])],8,is)]))])]),_:1})]),_:1},8,["organization","errors"])):z("",!0)])}}});we({admin_root:ke,default_lang:G.global.locale.value,only_locales:G.global.locale.value,schema_documentation_url:ze,schema_validata_url:Ae,show_copy_resource_permalink:!0,tabular_api_url:Me,tabular_page_size:Ce,title:Re});const ws=[{path:"/me",component:et},{path:"/organizations/:oid",children:[{path:"datasets",component:Le,props:!0,name:"organization-datasets"},{path:"reuses",component:Ge,props:!0,name:"organization-reuses"},{path:"members",component:Qo,props:!0,name:"organization-members"},{path:"profile",component:ys,props:!0,name:"organization-profile"}]}],ks=Ie({history:Se(),routes:ws}),U=oe(Mt);qe(U);U.use(Oe);U.use(Te);U.use(G);U.use(ks);U.mount("#admin");globalThis.dsfr.start();console.log("JS is injected !");export{zs as __vite_legacy_guard};
