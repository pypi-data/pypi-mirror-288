export const id=2808;export const ids=[2808];export const modules={62808:(e,t,i)=>{i.r(t),i.d(t,{HaTTSSelector:()=>v});var s=i(85461),a=i(98597),n=i(196),d=i(69534),l=i(33167),u=i(24517),r=i(91330),o=i(11355),h=i(6933);i(9484),i(96334);const c="__NONE_OPTION__",g={cloud:"Home Assistant Cloud",google_translate:"Google Translate"};(0,s.A)([(0,n.EM)("ha-tts-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"language",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_engines",value:void 0},{kind:"method",key:"render",value:function(){if(!this._engines)return a.s6;const e=this.value??(this.required?this._engines.find((e=>0!==e.supported_languages?.length)):c);return a.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.tts-picker.tts")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${u.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?a.s6:a.qy`<ha-list-item .value=${c}>
              ${this.hass.localize("ui.components.tts-picker.none")}
            </ha-list-item>`}
        ${this._engines.map((e=>{let t=e.engine_id;if(e.engine_id.includes(".")){const i=this.hass.states[e.engine_id];t=i?(0,r.u)(i):e.engine_id}else e.engine_id in g&&(t=g[e.engine_id]);return a.qy`<ha-list-item
            .value=${e.engine_id}
            .disabled=${0===e.supported_languages?.length}
          >
            ${t}
          </ha-list-item>`}))}
      </ha-select>
    `}},{kind:"method",key:"willUpdate",value:function(e){(0,d.A)(i,"willUpdate",this,3)([e]),this.hasUpdated?e.has("language")&&this._debouncedUpdateEngines():this._updateEngines()}},{kind:"field",key:"_debouncedUpdateEngines",value(){return(0,o.s)((()=>this._updateEngines()),500)}},{kind:"method",key:"_updateEngines",value:async function(){if(this._engines=(await(0,h.Xv)(this.hass,this.language,this.hass.config.country||void 0)).providers,!this.value)return;const e=this._engines.find((e=>e.engine_id===this.value));(0,l.r)(this,"supported-languages-changed",{value:e?.supported_languages}),e&&0!==e.supported_languages?.length||(this.value=void 0,(0,l.r)(this,"value-changed",{value:this.value}))}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===c||(this.value=t.value===c?void 0:t.value,(0,l.r)(this,"value-changed",{value:this.value}),(0,l.r)(this,"supported-languages-changed",{value:this._engines.find((e=>e.engine_id===this.value))?.supported_languages}))}}]}}),a.WF);let v=(0,s.A)([(0,n.EM)("ha-selector-tts")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){return a.qy`<ha-tts-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .language=${this.selector.tts?.language||this.context?.language}
      .disabled=${this.disabled}
      .required=${this.required}
    ></ha-tts-picker>`}},{kind:"field",static:!0,key:"styles",value(){return a.AH`
    ha-tts-picker {
      width: 100%;
    }
  `}}]}}),a.WF)},6933:(e,t,i)=>{i.d(t,{EF:()=>n,Xv:()=>d,ni:()=>a,u1:()=>l,z3:()=>u});const s="media-source://tts/",a=e=>e.startsWith(s),n=e=>e.substring(19),d=(e,t,i)=>e.callWS({type:"tts/engine/list",language:t,country:i}),l=(e,t)=>e.callWS({type:"tts/engine/get",engine_id:t}),u=(e,t,i)=>e.callWS({type:"tts/engine/voices",engine_id:t,language:i})}};
//# sourceMappingURL=XV2iBZOV.js.map