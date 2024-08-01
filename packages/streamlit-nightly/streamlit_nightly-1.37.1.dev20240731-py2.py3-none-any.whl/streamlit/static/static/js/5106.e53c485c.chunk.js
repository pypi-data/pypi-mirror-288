"use strict";(self.webpackChunk_streamlit_app=self.webpackChunk_streamlit_app||[]).push([[5106],{87814:(e,t,i)=>{i.d(t,{K:()=>n});var s=i(50641);class n{constructor(){this.formClearListener=void 0,this.lastWidgetMgr=void 0,this.lastFormId=void 0}manageFormClearListener(e,t,i){(0,s.bb)(this.formClearListener)&&this.lastWidgetMgr===e&&this.lastFormId===t||(this.disconnect(),(0,s.bM)(t)&&(this.formClearListener=e.addFormClearedListener(t,i),this.lastWidgetMgr=e,this.lastFormId=t))}disconnect(){var e;null===(e=this.formClearListener)||void 0===e||e.disconnect(),this.formClearListener=void 0,this.lastWidgetMgr=void 0,this.lastFormId=void 0}}},5106:(e,t,i)=>{i.r(t),i.d(t,{default:()=>F});var s=i(66845),n=i(1866),o=i.n(n),a=i(70461),r=i(25621),l=i(52347),d=i(53608),h=i.n(d),m=i(87814),u=i(16295),c=i(50641),g=i(98478),p=i(86659),f=i(8879),b=i(68411),v=i(1515),T=i(35704);const y=(0,v.Z)("div",{target:"ew7r33m3"})((e=>{let{disabled:t,theme:i}=e;return{alignItems:"center",backgroundColor:t?i.colors.gray:i.colors.primary,borderTopLeftRadius:"100%",borderTopRightRadius:"100%",borderBottomLeftRadius:"100%",borderBottomRightRadius:"100%",borderTopStyle:"none",borderBottomStyle:"none",borderRightStyle:"none",borderLeftStyle:"none",boxShadow:"none",display:"flex",height:i.radii.xl,justifyContent:"center",width:i.radii.xl,":focus":{outline:"none"},":focus-visible":{boxShadow:"0 0 0 0.2rem ".concat((0,T.DZ)(i.colors.primary,.5))}}}),""),R=(0,v.Z)("div",{target:"ew7r33m2"})((e=>{let{disabled:t,theme:i}=e;return{fontFamily:i.genericFonts.codeFont,fontSize:i.fontSizes.sm,paddingBottom:i.spacing.twoThirdsSmFont,color:t?i.colors.gray:i.colors.primary,top:"-22px",position:"absolute",whiteSpace:"nowrap",backgroundColor:i.colors.transparent,lineHeight:i.lineHeights.base,fontWeight:"normal"}}),""),V=(0,v.Z)("div",{target:"ew7r33m1"})((e=>{let{theme:t}=e;return{paddingBottom:t.spacing.none,paddingLeft:t.spacing.none,paddingRight:t.spacing.none,paddingTop:t.spacing.twoThirdsSmFont,justifyContent:"space-between",alignItems:"center",display:"flex"}}),""),x=(0,v.Z)("div",{target:"ew7r33m0"})((e=>{let{disabled:t,theme:i}=e;return{lineHeight:i.lineHeights.base,fontWeight:"normal",fontSize:i.fontSizes.sm,fontFamily:i.genericFonts.codeFont,color:t?i.colors.fadedText40:"inherit"}}),"");var C=i(40864);class w extends s.PureComponent{constructor(e){super(e),this.formClearHelper=new m.K,this.state=void 0,this.sliderRef=s.createRef(),this.thumbRef=[],this.thumbValueRef=[],this.commitWidgetValueDebounced=void 0,this.commitWidgetValue=e=>{const{widgetMgr:t,element:i,fragmentId:s}=this.props;t.setDoubleArrayValue(i,this.state.value,e,s)},this.onFormCleared=()=>{this.setState(((e,t)=>({value:t.element.default})),(()=>this.commitWidgetValue({fromUi:!0})))},this.handleChange=e=>{let{value:t}=e;this.setState({value:t},(()=>this.commitWidgetValueDebounced({fromUi:!0})))},this.renderThumb=s.forwardRef(((e,t)=>{var i;const{$value:n,$thumbIndex:a}=e,r=a||0;this.thumbRef[r]=t,(i=this.thumbValueRef)[r]||(i[r]=s.createRef());const l=n?this.formatValue(n[a]):"",d=o()(e,["role","style","aria-valuemax","aria-valuemin","aria-valuenow","tabIndex","onKeyUp","onKeyDown","onMouseEnter","onMouseLeave","draggable"]),h={};return(this.props.element.options.length>0||this.isDateTimeType())&&(h["aria-valuetext"]=l),(0,C.jsx)(y,{...d,disabled:!0===e.$disabled,ref:this.thumbRef[r],"aria-valuetext":l,"aria-label":this.props.element.label,children:(0,C.jsx)(R,{className:"StyledThumbValue","data-testid":"stThumbValue",disabled:!0===e.$disabled,ref:this.thumbValueRef[r],children:l})})})),this.renderTickBar=()=>{const{disabled:e,element:t}=this.props,{max:i,min:s}=t;return(0,C.jsxs)(V,{"data-testid":"stTickBar",children:[(0,C.jsx)(x,{disabled:e,"data-testid":"stTickBarMin",children:this.formatValue(s)}),(0,C.jsx)(x,{disabled:e,"data-testid":"stTickBarMax",children:this.formatValue(i)})]})},this.commitWidgetValueDebounced=(0,c.Ds)(200,this.commitWidgetValue.bind(this)),this.state={value:this.initialValue}}get initialValue(){const e=this.props.widgetMgr.getDoubleArrayValue(this.props.element);return void 0!==e?e:this.props.element.default}componentDidMount(){setTimeout((()=>{this.thumbValueAlignment()}),0),this.props.element.setValue?this.updateFromProtobuf():this.commitWidgetValue({fromUi:!1})}componentDidUpdate(){this.maybeUpdateFromProtobuf()}componentWillUnmount(){this.formClearHelper.disconnect()}maybeUpdateFromProtobuf(){const{setValue:e}=this.props.element;e&&this.updateFromProtobuf()}updateFromProtobuf(){const{value:e}=this.props.element;this.props.element.setValue=!1,this.setState({value:e},(()=>{this.commitWidgetValue({fromUi:!1})}))}get value(){const{min:e,max:t}=this.props.element,{value:i}=this.state;let s=i[0],n=i.length>1?i[1]:i[0];return s>n&&(s=n),s<e&&(s=e),s>t&&(s=t),n<e&&(n=e),n>t&&(n=t),i.length>1?[s,n]:[s]}isDateTimeType(){const{dataType:e}=this.props.element;return e===u.iR.DataType.DATETIME||e===u.iR.DataType.DATE||e===u.iR.DataType.TIME}formatValue(e){const{format:t,options:i}=this.props.element;return this.isDateTimeType()?h().utc(e/1e3).format(t):i.length>0?(0,l.sprintf)(t,i[e]):(0,l.sprintf)(t,e)}alignValueOnThumb(e,t,i){if(e&&t&&i){const s=e.getBoundingClientRect(),n=t.getBoundingClientRect(),o=i.getBoundingClientRect(),a=n.left+n.width/2,r=a-o.width/2<s.left,l=a+o.width/2>s.right;i.style.left=r?"0":"",i.style.right=l?"0":""}}thumbValueAlignment(){var e,t,i,s;const n=this.sliderRef.current,o=null===(e=this.thumbRef[0])||void 0===e?void 0:e.current,a=null===(t=this.thumbRef[1])||void 0===t?void 0:t.current,r=null===(i=this.thumbValueRef[0])||void 0===i?void 0:i.current,l=null===(s=this.thumbValueRef[1])||void 0===s?void 0:s.current;if(this.alignValueOnThumb(n,o,r),this.alignValueOnThumb(n,a,l),n&&o&&a&&r&&l){const e=n.getBoundingClientRect(),t=o.getBoundingClientRect(),i=a.getBoundingClientRect(),s=r.getBoundingClientRect(),d=l.getBoundingClientRect();if(s.right+16>d.left){d.left-16-s.width>e.left?r.style.right="".concat(d.width+16-(i.right-t.right),"px"):l.style.left="".concat(s.width+16-(i.left-t.left),"px")}}}render(){var e;const{disabled:t,element:i,theme:s,width:n,widgetMgr:o}=this.props,{colors:r,fonts:l,fontSizes:d,spacing:h}=s,m={width:n};return this.formClearHelper.manageFormClearListener(o,i.formId,this.onFormCleared),this.thumbValueAlignment(),(0,C.jsxs)("div",{ref:this.sliderRef,className:"stSlider","data-testid":"stSlider",style:m,children:[(0,C.jsx)(g.O,{label:i.label,disabled:t,labelVisibility:(0,c.iF)(null===(e=i.labelVisibility)||void 0===e?void 0:e.value),children:i.help&&(0,C.jsx)(p.dT,{children:(0,C.jsx)(f.Z,{content:i.help,placement:b.u.TOP_RIGHT})})}),(0,C.jsx)(a.Z,{min:i.min,max:i.max,step:i.step,value:this.value,onChange:this.handleChange,disabled:t,overrides:{Root:{style:{paddingTop:h.twoThirdsSmFont}},Thumb:this.renderThumb,Tick:{style:{fontFamily:l.monospace,fontSize:d.sm}},Track:{style:{backgroundColor:"none !important",paddingBottom:0,paddingLeft:0,paddingRight:0,paddingTop:h.twoThirdsSmFont}},InnerTrack:{style:e=>{let{$disabled:t}=e;return{height:"4px",...t?{background:r.darkenedBgMix25}:{}}}},TickBar:this.renderTickBar}})]})}}const F=(0,r.b)(w)}}]);