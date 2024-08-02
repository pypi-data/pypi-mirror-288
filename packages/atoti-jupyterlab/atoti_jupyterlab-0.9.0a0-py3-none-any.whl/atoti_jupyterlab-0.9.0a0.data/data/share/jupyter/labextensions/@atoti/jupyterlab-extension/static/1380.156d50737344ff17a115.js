"use strict";(self.webpackChunk_atoti_jupyterlab_extension=self.webpackChunk_atoti_jupyterlab_extension||[]).push([[1380],{89953:(r,o,e)=>{if(e.d(o,{DP:()=>p,NP:()=>u}),4871==e.j)var n=e(74389);var t=e(40570),a=e(90923),i=e(93345),l=e(63719);if(4871==e.j)var c=e(84845);if(4871==e.j)var d=e(42565);const s=(0,i.createContext)(null),u=r=>{const o=(0,i.useMemo)((()=>(0,d.D)(r.value)),[r.value]),e=(0,c.D)(o),u=(0,i.useMemo)((()=>({accentColor:o.primaryColor,successColor:o.successColor,warningColor:o.warningColor,errorColor:o.errorColor,whiteColor:o.backgroundColor,lightGrayColor:o.grayScale[5],darkGrayColor:o.grayScale[7]})),[o]);return(0,n.Y)(s.Provider,{value:o,children:(0,n.Y)(a.ConfigProvider,{theme:e,children:(0,n.Y)(l._IconThemeContext.Provider,{value:u,children:(0,n.Y)(a.App,{className:r.className,css:t.css`
              box-sizing: border-box;
              font-size: ${e.token?.fontSizeSM}px;
              line-height: ${e.token?.lineHeight};
              font-family: ${e.token?.fontFamily};
              color: ${e.token?.colorText};
              background-color: ${e.token?.colorBgBase};
              color-scheme: ${o.isDark?"dark":"light"};

              *,
              *:before,
              *:after {
                box-sizing: inherit;
              }

              .aui-invisible-scrollbars {
                scrollbar-width: none;
              }
              .aui-invisible-scrollbars::-webkit-scrollbar {
                display: none;
              }

              .ant-picker-dropdown {
                padding: 0;
              }
              .ant-picker-range-arrow {
                ::before,
                ::after {
                  display: none;
                }
              }

              .ant-modal-footer {
                padding-inline: ${e.components?.Modal?.paddingLG}px!important;
              }

              .ant-popconfirm-buttons {
                padding-top: ${e.components?.Popconfirm?.paddingXXS}px!important;
              }

              .ant-popover {
                .ant-popover-title {
                  border-bottom: 0px;
                }

                .ant-popover-inner-content {
                  padding: 8px 12px 8px 12px;
                }
              }

              button,
              input {
                font-family: inherit;
                line-height: inherit;
                font-size: inherit;
              }

              input[type="checkbox"] {
                margin: 0;
              }

              fieldset {
                border: none;
              }

              g.pointtext {
                display: none;
              }

              /*
           * TODO Remove when upgrading Ant Design.
           * This is an Ant Design bug fixed in https://github.com/ant-design/ant-design/commit/467741f5.
           */
              .ant-dropdown-menu-sub {
                margin: 0;
              }
            `,children:r.children})})})})};function p(){const r=(0,i.useContext)(s);if(!r)throw new Error("Missing theme. Remember to add <ThemeProvider /> at the top of your application.");return r}s.Consumer},85190:(r,o,e)=>{if(e.d(o,{O:()=>l}),4871==e.j)var n=e(69387);if(4871==e.j)var t=e(94995);if(4871==e.j)var a=e(84544);const i=4871==e.j?["transparent",void 0,null]:null,l=function(r,o,e){if(i.includes(r)&&o)return(0,t.J)((0,n.p)(o),e);if(i.includes(o)&&r)return(0,t.J)((0,n.p)(r),e);if(r&&o){const t=(0,n.p)(r),i=(0,n.p)(o);return(0,a.e)(function(r,...o){return o[0].map(((e,n)=>r(...o.map((r=>r[n])))))}(((r,o)=>Math.ceil((1-e)*r+e*o)),t,i))}throw new Error("Invalid arguments to addColorLayer")}},44930:(r,o,e)=>{e.d(o,{e:()=>i});var n=e(69387),t=e(94995);const a=/\d+(\.\d*)?|\.\d+/g,i=function({color:r,opacity:o,shadeFactor:e=0,isShading:i,isInverting:l}){const c=(0,n.p)(r),d=r.startsWith("rgba")?(r=>{const o=r.match(a);if(!o)throw new SyntaxError("Invalid rgba parameter");return Number.parseFloat(o.slice(3).join(""))})(r):1;return(0,t.J)(c.map((r=>{const o=l?(r=>255-r)(r):r;return n=i?o*(1-e):o+(255-o)*e,Math.max(0,Math.min(255,n));var n})),(s=d*o,Math.max(0,Math.min(1,s))));var s}},7830:(r,o,e)=>{if(e.d(o,{w:()=>t}),4871==e.j)var n=e(85190);const t=(r,o)=>{const e=e=>(0,n.O)(r,o,e);return[e(0),e(.02),e(.04),e(.06),e(.09),e(.15),e(.25),e(.45),e(.55),e(.65),e(.75),e(.85),e(.95),e(1)]}},84845:(r,o,e)=>{e.d(o,{D:()=>t});var n=e(90923);function t(r){return{token:{lineHeight:1.66667,fontSizeSM:12,fontFamily:"-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji",borderRadius:2,controlOutlineWidth:0,colorPrimary:r.primaryColor,colorSuccess:r.successColor,colorWarning:r.warningColor,colorText:r.textColor,colorTextPlaceholder:r.placeholderColor,colorTextDisabled:r.disabledTextColor,colorBgBase:r.backgroundColor,colorPrimaryBg:r.selectedMenuItemBackground,colorBgContainerDisabled:r.disabledBackground,colorBorder:r.cellBorderColor,colorBorderSecondary:r.cellBorderColor},components:{Menu:{radiusItem:0,radiusSubMenuItem:0,lineWidth:.5,margin:12,controlHeightLG:32,colorActiveBarBorderSize:0,activeBarWidth:3,itemSelectedColor:r.primaryColor,subMenuItemBg:r.menuInlineSubmenuBg},Tooltip:{paddingXS:8,paddingSM:12},Checkbox:{paddingXS:8},Modal:{wireframe:!0,paddingXS:8,marginXS:8,padding:11,paddingLG:16},Popover:{wireframe:!0,padding:12,paddingSM:12},Popconfirm:{marginXS:8,paddingXXS:4},Card:{padding:8.5,paddingLG:12,fontWeightStrong:500},Dropdown:{marginXS:8,controlPaddingHorizontal:8},Tabs:{colorText:r.grayScale[8],colorFillAlter:r.grayScale[3]}},algorithm:[n.theme.compactAlgorithm,...r.isDark?[n.theme.darkAlgorithm]:[],(r,o=n.theme.defaultAlgorithm(r))=>({...o,colorInfo:r.colorPrimary,colorBgContainer:r.colorBgBase,colorBgElevated:r.colorBgBase,colorBgLayout:r.colorBgBase})]}}},42565:(r,o,e)=>{e.d(o,{D:()=>S});var n=e(18956),t=e(57358),a=2,i=.16,l=.05,c=.05,d=.15,s=5,u=4,p=[{index:7,opacity:.15},{index:6,opacity:.25},{index:5,opacity:.3},{index:5,opacity:.45},{index:5,opacity:.65},{index:5,opacity:.85},{index:4,opacity:.9},{index:3,opacity:.95},{index:2,opacity:.97},{index:1,opacity:.98}];function g(r){var o=r.r,e=r.g,t=r.b,a=(0,n.wE)(o,e,t);return{h:360*a.h,s:a.s,v:a.v}}function h(r){var o=r.r,e=r.g,t=r.b;return"#".concat((0,n.Ob)(o,e,t,!1))}function m(r,o,e){var n;return(n=Math.round(r.h)>=60&&Math.round(r.h)<=240?e?Math.round(r.h)-a*o:Math.round(r.h)+a*o:e?Math.round(r.h)+a*o:Math.round(r.h)-a*o)<0?n+=360:n>=360&&(n-=360),n}function b(r,o,e){return 0===r.h&&0===r.s?r.s:((n=e?r.s-i*o:o===u?r.s+i:r.s+l*o)>1&&(n=1),e&&o===s&&n>.1&&(n=.1),n<.06&&(n=.06),Number(n.toFixed(2)));var n}function f(r,o,e){var n;return(n=e?r.v+c*o:r.v-d*o)>1&&(n=1),Number(n.toFixed(2))}function C(r){for(var o=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},e=[],n=(0,t.RO)(r),a=s;a>0;a-=1){var i=g(n),l=h((0,t.RO)({h:m(i,a,!0),s:b(i,a,!0),v:f(i,a,!0)}));e.push(l)}e.push(h(n));for(var c=1;c<=u;c+=1){var d=g(n),C=h((0,t.RO)({h:m(d,c),s:b(d,c),v:f(d,c)}));e.push(C)}return"dark"===o.theme?p.map((function(r){var n,a,i,l=r.index,c=r.opacity;return h((n=(0,t.RO)(o.backgroundColor||"#141414"),i=100*c/100,{r:((a=(0,t.RO)(e[l])).r-n.r)*i+n.r,g:(a.g-n.g)*i+n.g,b:(a.b-n.b)*i+n.b}))})):e}var v={red:"#F5222D",volcano:"#FA541C",orange:"#FA8C16",gold:"#FAAD14",yellow:"#FADB14",lime:"#A0D911",green:"#52C41A",cyan:"#13C2C2",blue:"#1890FF",geekblue:"#2F54EB",purple:"#722ED1",magenta:"#EB2F96",grey:"#666666"},y={},k={};Object.keys(v).forEach((function(r){y[r]=C(v[r]),y[r].primary=y[r][5],k[r]=C(v[r],{theme:"dark",backgroundColor:"#141414"}),k[r].primary=k[r][5]})),y.red,y.volcano,y.gold,y.orange,y.yellow,y.lime,y.green,y.cyan,y.blue,y.geekblue,y.purple,y.magenta,y.grey;var x=e(7830),w=e(74113),B=e(93145),F=e(69412);function S(r){const o=!r.isDark,e=r.white??o?"#FFFFFF":"#000000",n=r.black??o?"#000000":"#FFFFFF",t=r.backgroundColor??e,a=(0,x.w)(t,n),i=(0,F.k)([(0,B.z)(r.primaryColor)[0],"100","50"]),l=r.successColor??"#52C41A",c=r.errorColor??"#F5222D",d=C(r.primaryColor,{theme:o?"default":"dark",backgroundColor:t});return{activeMenuItemBackgroundColor:a[4],activeTabBackgroundColor:a[0],alternateCellBackgroundColor:(0,w.j)(a[2],.65),alternateBackgroundColor:a[1],backgroundColor:t,black:n,cellBackgroundDuringNegativeTransition:(0,w.j)(c,.7),cellBackgroundDuringPositiveTransition:(0,w.j)(l,.7),cellBorderColor:a[5],headerActiveColor:r.primaryColor,disabledBackground:o?"#F5F5F5":t,disabledTextColor:o?(0,w.j)(n,.35):(0,w.j)(n,.25),dropHintBorderColor:(0,w.j)(i,.2),dropHintColor:(0,w.j)(i,.15),errorColor:c,grayScale:a,hoverColor:d[5],inactiveTabBackgroundColor:a[2],menuInlineSubmenuBg:"transparent",placeholderColor:a[6],primaryScale:d,selectedMenuItemBackground:d[0],selectionOverlayColor:(0,w.j)(i,.1),selectionMarkDarkColor:"#646464",selectionMarkLightColor:"#FFFFFF",selectionColor:d[0],shadowColor:"#000C11",successColor:l,textColor:o?a[11]:(0,w.j)(n,.65),warningColor:"#FAAD14",white:e,...r}}},69387:(r,o,e)=>{function n(r,o,e){const n=(e+1)%1;return n<1/6?r+6*(o-r)*n:n<.5?o:n<2/3?r+(o-r)*(2/3-n)*6:r}e.d(o,{p:()=>i});const t=/\d+/g,a=/\d+(\.\d*)?|\.\d+/g,i=function(r){const o=r.toLowerCase();if(o.startsWith("#"))return function(r){if(6!==r.length&&3!==r.length)throw new Error(`Hex color (${r}) is not a valid 3 or 6 character string`);const o=6===r.length?r:r.charAt(0).repeat(2)+r.charAt(1).repeat(2)+r.charAt(2).repeat(2);return[Number.parseInt(o.slice(0,2),16),Number.parseInt(o.slice(2,4),16),Number.parseInt(o.slice(4,6),16)]}(r.slice(1));if(o.startsWith("rgb"))return(r=>{const o=r.match(t);if(!o)throw new SyntaxError("Invalid rgb parameter");const e=o.slice(0,3).map((r=>Number(r)));return[e[0],e[1],e[2]]})(r);if(o.startsWith("hsl"))return(r=>{const o=r.match(a);if(!o)throw new SyntaxError("Invalid hsl parameter");const e=o.slice(0,3).map((r=>Number(r)));return function(r,o,e){let t,a,i;const l=r/360,c=o/100,d=e/100;if(0===c)i=d,a=d,t=d;else{const r=d<.5?d*(1+c):d+c-d*c,o=2*d-r;t=n(o,r,l+1/3),a=n(o,r,l),i=n(o,r,l-1/3)}return t=Math.round(255*t),a=Math.round(255*a),i=Math.round(255*i),[t,a,i]}(e[0],e[1],e[2])})(r);throw new Error("Unsupported color syntax. Supported syntaxes are rgb, hsl and hex.")}},74113:(r,o,e)=>{e.d(o,{j:()=>t});var n=e(44930);function t(r,o=1){return(0,n.e)({color:r,opacity:o})}},22948:(r,o,e)=>{function n(r,o,e){const n=r/255,t=o/255,a=e/255,i=Math.max(n,t,a),l=Math.min(n,t,a);let c=0,d=0,s=(i+l)/2;if(i!==l){const r=i-l;switch(d=s>.5?r/(2-i-l):r/(i+l),i){case n:c=(t-a)/r+(t<a?6:0);break;case t:c=(a-n)/r+2;break;case a:c=(n-t)/r+4}c/=6}return c=Math.round(360*c),d=Math.round(100*d),s=Math.round(100*s),[c,d,s]}e.d(o,{K:()=>n})},93145:(r,o,e)=>{if(e.d(o,{z:()=>a}),4871==e.j)var n=e(69387);if(4871==e.j)var t=e(22948);function a(r){return(0,t.K)(...(0,n.p)(r))}},69412:(r,o,e)=>{function n(r){return`hsl(${r[0]}, ${r[1]}%, ${r[2]}%)`}e.d(o,{k:()=>n})},94995:(r,o,e)=>{e.d(o,{J:()=>n});const n=function(r,o){return`rgba(${r.join(", ")}, ${o})`}},84544:(r,o,e)=>{e.d(o,{e:()=>n});const n=function(r){return`rgb(${r.join(", ")})`}},83972:(r,o,e)=>{e.d(o,{l:()=>t});const n=new Set;function t(r,o){n.has(r)||(n.add(r),console.warn(`%c ${r} `,"font-style: italic; border: 1px solid orange; border-radius: 5px","is deprecated and will not be supported in the next breaking release of Atoti UI.",o))}}}]);