"use strict";(self.webpackChunk_streamlit_app=self.webpackChunk_streamlit_app||[]).push([[1116],{81116:(e,t,r)=>{r.r(t),r.d(t,{default:()=>M});var n=r(66845),o=r(25621),i=r(62813),c=r.n(i),a=Object.freeze({radio:"radio",checkbox:"checkbox"}),l=(Object.freeze({change:"change"}),"default"),u=r(80318),s=r(99282),f=(0,r(80745).zo)("div",(function(e){var t=e.$shape,r=e.$length,n=e.$theme,o=1===r?void 0:t!==l?"-".concat(n.sizing.scale100):"-0.5px";return{display:"flex",marginLeft:o,marginRight:o}}));function d(e){return d="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},d(e)}function p(){return p=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},p.apply(this,arguments)}function h(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function y(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?h(Object(r),!0).forEach((function(t){C(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):h(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function b(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!==typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var n,o,i=[],c=!0,a=!1;try{for(r=r.call(e);!(c=(n=r.next()).done)&&(i.push(n.value),!t||i.length!==t);c=!0);}catch(l){a=!0,o=l}finally{try{c||null==r.return||r.return()}finally{if(a)throw o}}return i}(e,t)||function(e,t){if(!e)return;if("string"===typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return m(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function v(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function g(e,t){return g=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},g(e,t)}function O(e){var t=function(){if("undefined"===typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"===typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=w(e);if(t){var o=w(this).constructor;r=Reflect.construct(n,arguments,o)}else r=n.apply(this,arguments);return function(e,t){if(t&&("object"===d(t)||"function"===typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return E(e)}(this,r)}}function E(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function w(e){return w=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},w(e)}function C(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}f.displayName="StyledRoot",f.displayName="StyledRoot";var j=function(e){!function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),t&&g(e,t)}(c,e);var t,r,o,i=O(c);function c(){var e;!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,c);for(var t=arguments.length,r=new Array(t),n=0;n<t;n++)r[n]=arguments[n];return C(E(e=i.call.apply(i,[this].concat(r))),"childRefs",{}),e}return t=c,r=[{key:"render",value:function(){var e=this,t=this.props,r=t.overrides,o=void 0===r?{}:r,i=t.mode,c=void 0===i?a.checkbox:i,d=t.children,h=t.selected,m=t.disabled,v=t.onClick,g=t.kind,O=t.shape,E=t.size,w=b((0,u.jb)(o.Root,f),2),C=w[0],j=w[1],S=this.props["aria-label"]||this.props.ariaLabel,k=c===a.radio,L=n.Children.count(d);return n.createElement(s.R.Consumer,null,(function(t){return n.createElement(C,p({"aria-label":S||t.buttongroup.ariaLabel,"data-baseweb":"button-group",role:k?"radiogroup":"group",$shape:O,$length:d.length},j),n.Children.map(d,(function(t,r){if(!n.isValidElement(t))return null;var o=t.props.isSelected?t.props.isSelected:function(e,t){return!(!Array.isArray(e)&&"number"!==typeof e)&&(Array.isArray(e)?e.includes(t):e===t)}(h,r);return k&&(e.childRefs[r]=n.createRef()),n.cloneElement(t,{disabled:m||t.props.disabled,isSelected:o,ref:k?e.childRefs[r]:void 0,tabIndex:!k||o||k&&(!h||-1===h)&&0===r?0:-1,onKeyDown:function(t){if(k){var r=Number(h)?Number(h):0;if("ArrowUp"===t.key||"ArrowLeft"===t.key){t.preventDefault&&t.preventDefault();var n=r-1<0?L-1:r-1;v&&v(t,n),e.childRefs[n].current&&e.childRefs[n].current.focus()}if("ArrowDown"===t.key||"ArrowRight"===t.key){t.preventDefault&&t.preventDefault();var o=r+1>L-1?0:r+1;v&&v(t,o),e.childRefs[o].current&&e.childRefs[o].current.focus()}}},kind:g,onClick:function(e){m||(t.props.onClick&&t.props.onClick(e),v&&v(e,r))},shape:O,size:E,overrides:y({BaseButton:{style:function(e){var t=e.$theme;return 1===d.length?{}:O!==l?{marginLeft:t.sizing.scale100,marginRight:t.sizing.scale100}:{marginLeft:"0.5px",marginRight:"0.5px"}},props:{"aria-checked":o,role:k?"radio":"checkbox"}}},t.props.overrides)})})))}))}}],r&&v(t.prototype,r),o&&v(t,o),Object.defineProperty(t,"prototype",{writable:!1}),c}(n.Component);C(j,"defaultProps",{disabled:!1,onClick:function(){},shape:l,size:"default",kind:"secondary"});var S=r(81354),k=r(9003),L=r(22704),R=r(16295),_=r(87814),I=r(40864);function P(e,t,r,n){let o=!(arguments.length>4&&void 0!==arguments[4])||arguments[4];r.setIntArrayValue(t,e,{fromUi:o},n)}function A(e){return(0,I.jsx)(L.p,{size:"lg",iconValue:e})}function x(e,t,r,o,i){var c;const a=function(e,t,r,n){return r.indexOf(n)>-1||t===R.hE.ClickMode.SINGLE_SELECT&&e===R.hE.SelectionVisualization.ALL_UP_TO_SELECTED&&r.length>0&&n<r[0]}(r,o,i,t),l=function(e,t,r){return e&&r?r:t}(a,null!==(c=e.content)&&void 0!==c?c:"",e.selectedContent),u=!a||e.selectedContent?S.nW.BORDERLESS_ICON:S.nW.BORDERLESS_ICON_ACTIVE;return(0,n.forwardRef)((function(e,t){return(0,I.jsx)(k.ZP,{...e,size:S.V5.XSMALL,kind:u,children:A(l)})}))}const M=function(e){const{disabled:t,element:r,fragmentId:i,widgetMgr:l}=e,{clickMode:u,default:s,options:f,value:d,selectionVisualization:p}=r,h=(0,o.u)(),[y,b]=(0,n.useState)(function(e,t){const r=e.getIntArrayValue(t);return null!==r&&void 0!==r?r:t.default}(l,r)||[]),m=n.useRef(r),v=n.useRef(void 0);(0,n.useEffect)((()=>{if(!r.formId)return;const e=new _.K;return e.manageFormClearListener(l,r.formId,(()=>{b(s)})),()=>{e.disconnect()}}),[r.formId,l,s]);const g=(0,n.useMemo)((()=>JSON.stringify(d)),[d]);let O;(0,n.useEffect)((()=>{const e=JSON.parse(g);if(m.current.setValue)b(e),P(y,m.current,l,i,!1),m.current.setValue=!1;else{if(c()(y,v.current))return;const e=void 0!==v.current;P(y,m.current,l,i,e)}v.current=y}),[y,l,i,g]),u===R.hE.ClickMode.SINGLE_SELECT?O=a.radio:u===R.hE.ClickMode.MULTI_SELECT&&(O=a.checkbox);const E=f.map(((e,t)=>{const r=x(e,t,p,u,y);return(0,I.jsx)(r,{},"".concat(e.content,"-").concat(t))}));return(0,I.jsx)(j,{disabled:t,mode:O,onClick:(e,t)=>{const r=function(e,t,r){return e==R.hE.ClickMode.MULTI_SELECT?function(e,t){return t.includes(e)?t.filter((t=>t!==e)):[...t,e]}(t,null!==r&&void 0!==r?r:[]):[t]}(u,t,y);b(r)},selected:u===R.hE.ClickMode.MULTI_SELECT?y:(w=y,0===w.length?-1:w[0]),overrides:{Root:{style:{flexWrap:"wrap",gap:h.spacing.threeXS},props:{"data-testid":"stButtonGroup"}}},children:E});var w}},87814:(e,t,r)=>{r.d(t,{K:()=>o});var n=r(50641);class o{constructor(){this.formClearListener=void 0,this.lastWidgetMgr=void 0,this.lastFormId=void 0}manageFormClearListener(e,t,r){(0,n.bb)(this.formClearListener)&&this.lastWidgetMgr===e&&this.lastFormId===t||(this.disconnect(),(0,n.bM)(t)&&(this.formClearListener=e.addFormClearedListener(t,r),this.lastWidgetMgr=e,this.lastFormId=t))}disconnect(){var e;null===(e=this.formClearListener)||void 0===e||e.disconnect(),this.formClearListener=void 0,this.lastWidgetMgr=void 0,this.lastFormId=void 0}}}}]);