import{aV as i}from"./sentry.5.1.1.dev24290.js";import"vue";import"./_commonjsHelpers.5.1.1.dev24290.js";var l={s:["nokkrar sekúndur","nokkrar sekúndur","nokkrum sekúndum"],m:["mínúta","mínútu","mínútu"],mm:["mínútur","mínútur","mínútum"],h:["klukkustund","klukkustund","klukkustund"],hh:["klukkustundir","klukkustundir","klukkustundum"],d:["dagur","dag","degi"],dd:["dagar","daga","dögum"],M:["mánuður","mánuð","mánuði"],MM:["mánuðir","mánuði","mánuðum"],y:["ár","ár","ári"],yy:["ár","ár","árum"]};function M(u,m,n,a){var t=n?1:2,d=a?0:t,e=u.length===2&&m%10===1,s=e?u[0]:u,k=l[s],_=k[d];return u.length===1?_:"%d "+_}function r(u,m,n,a){var t=M(n,u,a,m);return t.replace("%d",u)}var o={name:"is",weekdays:"sunnudagur_mánudagur_þriðjudagur_miðvikudagur_fimmtudagur_föstudagur_laugardagur".split("_"),months:"janúar_febrúar_mars_apríl_maí_júní_júlí_ágúst_september_október_nóvember_desember".split("_"),weekStart:1,weekdaysShort:"sun_mán_þri_mið_fim_fös_lau".split("_"),monthsShort:"jan_feb_mar_apr_maí_jún_júl_ágú_sep_okt_nóv_des".split("_"),weekdaysMin:"Su_Má_Þr_Mi_Fi_Fö_La".split("_"),ordinal:function(u){return u},formats:{LT:"H:mm",LTS:"H:mm:ss",L:"DD.MM.YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY [kl.] H:mm",LLLL:"dddd, D. MMMM YYYY [kl.] H:mm"},relativeTime:{future:"eftir %s",past:"fyrir %s síðan",s:r,m:r,mm:r,h:r,hh:r,d:r,dd:r,M:r,MM:r,y:r,yy:r}};i.locale(o,null,!0);export{o as default};
