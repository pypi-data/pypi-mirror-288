export const id=1546;export const ids=[1546];export const modules={31546:(e,t,i)=>{i.r(t),i.d(t,{HaSTTSelector:()=>v});var s=i(85461),a=i(98597),n=i(196),d=i(69534),l=i(33167),u=i(24517),r=i(91330),o=i(11355);i(9484),i(96334);const h="__NONE_OPTION__",c={cloud:"Home Assistant Cloud"};(0,s.A)([(0,n.EM)("ha-stt-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"language",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_engines",value:void 0},{kind:"method",key:"render",value:function(){if(!this._engines)return a.s6;const e=this.value??(this.required?this._engines.find((e=>0!==e.supported_languages?.length)):h);return a.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.stt-picker.stt")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${u.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?a.s6:a.qy`<ha-list-item .value=${h}>
              ${this.hass.localize("ui.components.stt-picker.none")}
            </ha-list-item>`}
        ${this._engines.map((e=>{let t=e.engine_id;if(e.engine_id.includes(".")){const i=this.hass.states[e.engine_id];t=i?(0,r.u)(i):e.engine_id}else e.engine_id in c&&(t=c[e.engine_id]);return a.qy`<ha-list-item
            .value=${e.engine_id}
            .disabled=${0===e.supported_languages?.length}
          >
            ${t}
          </ha-list-item>`}))}
      </ha-select>
    `}},{kind:"method",key:"willUpdate",value:function(e){(0,d.A)(i,"willUpdate",this,3)([e]),this.hasUpdated?e.has("language")&&this._debouncedUpdateEngines():this._updateEngines()}},{kind:"field",key:"_debouncedUpdateEngines",value(){return(0,o.s)((()=>this._updateEngines()),500)}},{kind:"method",key:"_updateEngines",value:async function(){var e,t,i;if(this._engines=(await(e=this.hass,t=this.language,i=this.hass.config.country||void 0,e.callWS({type:"stt/engine/list",language:t,country:i}))).providers,!this.value)return;const s=this._engines.find((e=>e.engine_id===this.value));(0,l.r)(this,"supported-languages-changed",{value:s?.supported_languages}),s&&0!==s.supported_languages?.length||(this.value=void 0,(0,l.r)(this,"value-changed",{value:this.value}))}},{kind:"get",static:!0,key:"styles",value:function(){return a.AH`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===h||(this.value=t.value===h?void 0:t.value,(0,l.r)(this,"value-changed",{value:this.value}),(0,l.r)(this,"supported-languages-changed",{value:this._engines.find((e=>e.engine_id===this.value))?.supported_languages}))}}]}}),a.WF);let v=(0,s.A)([(0,n.EM)("ha-selector-stt")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"selector",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"required",value(){return!0}},{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"context",value:void 0},{kind:"method",key:"render",value:function(){return a.qy`<ha-stt-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .language=${this.selector.stt?.language||this.context?.language}
      .disabled=${this.disabled}
      .required=${this.required}
    ></ha-stt-picker>`}},{kind:"field",static:!0,key:"styles",value(){return a.AH`
    ha-stt-picker {
      width: 100%;
    }
  `}}]}}),a.WF)}};
//# sourceMappingURL=91a5c_4l.js.map