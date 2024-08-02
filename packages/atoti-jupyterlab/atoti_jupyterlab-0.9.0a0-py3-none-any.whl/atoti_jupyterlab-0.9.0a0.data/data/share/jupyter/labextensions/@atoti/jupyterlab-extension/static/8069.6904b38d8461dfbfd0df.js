"use strict";(self.webpackChunk_atoti_jupyterlab_extension=self.webpackChunk_atoti_jupyterlab_extension||[]).push([[8069],{78069:(e,t,r)=>{r.r(t),r.d(t,{default:()=>u});var n=r(74389),o=r(40570),a=r(90923),i=r(31529),c=r(93345);const{RangePicker:s}=a.DatePicker,u=e=>{const t=(0,c.useRef)(null),r=(0,c.useRef)(null),u=(0,c.useRef)(null),[p,l]=(0,c.useState)(0),d=(0,i.isArray)(e.disabled)&&!e.disabled[1];return(0,c.useEffect)((()=>{if(d){const e=Array.from(t.current?.querySelectorAll(".ant-picker-input > input")??[]);r.current=e[0],u.current=e[1];const n=()=>l(0);r.current?.addEventListener("focus",n);const o=()=>l(1);return u.current?.addEventListener("focus",o),()=>{r.current?.removeEventListener("focus",n),u.current?.removeEventListener("focus",o)}}return l(0),()=>{}}),[d]),(0,n.Y)("div",{"aria-label":"Date picker",ref:t,css:o.css`
        position: relative;
        height: 290px !important;
        .ant-picker-active-bar {
          opacity: 1;
        }
        .ant-picker-dropdown {
          left: 0% !important;
          top: 32px !important;
          opacity: 1 !important;
          transform: scale(1) !important;
        }
      `,style:{...e.style,marginTop:"12px"},children:(0,n.Y)(a.ConfigProvider,{theme:{components:{DatePicker:{boxShadowSecondary:"unset",motionDurationMid:"unset",sizePopupArrow:0}}},children:(0,n.Y)(s,{...e,open:!0,onCalendarChange:(...t)=>{if(d){const e=(p+1)%2;l(e),(0===e?r:u).current?.focus()}e.onCalendarChange?.(...t)},activePickerIndex:p,getPopupContainer:e=>t?.current??e})})})}}}]);