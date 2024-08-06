export const id=4114;export const ids=[4114];export const modules={58636:(e,t,a)=>{a.d(t,{PE:()=>o});var i=a(67319),s=a(76415);const n=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],o=e=>e.first_weekday===s.zt.language?"weekInfo"in Intl.Locale.prototype?new Intl.Locale(e.language).weekInfo.firstDay%7:(0,i.S)(e.language)%7:n.includes(e.first_weekday)?n.indexOf(e.first_weekday):1},13634:(e,t,a)=>{a.d(t,{LW:()=>u,Xs:()=>c,fU:()=>o,ie:()=>l});var i=a(45081),s=a(84656),n=a(49655);const o=(e,t,a)=>r(t,a.time_zone).format(e),r=(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{hour:"numeric",minute:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,s.w)(e.time_zone,t)}))),l=(e,t,a)=>d(t,a.time_zone).format(e),d=(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{hour:(0,n.J)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,s.w)(e.time_zone,t)}))),c=(e,t,a)=>h(t,a.time_zone).format(e),h=(0,i.A)(((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",hour:(0,n.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,s.w)(e.time_zone,t)}))),u=(e,t,a)=>m(t,a.time_zone).format(e),m=(0,i.A)(((e,t)=>new Intl.DateTimeFormat("en-GB",{hour:"numeric",minute:"2-digit",hour12:!1,timeZone:(0,s.w)(e.time_zone,t)})))},84656:(e,t,a)=>{a.d(t,{w:()=>n});var i=a(76415);const s=Intl.DateTimeFormat?.().resolvedOptions?.().timeZone??"UTC",n=(e,t)=>e===i.Wj.local&&"UTC"!==s?s:t},49655:(e,t,a)=>{a.d(t,{J:()=>n});var i=a(45081),s=a(76415);const n=(0,i.A)((e=>{if(e.time_format===s.Hg.language||e.time_format===s.Hg.system){const t=e.time_format===s.Hg.language?e.language:void 0;return new Date("January 1, 2023 22:00:00").toLocaleString(t).includes("10")}return e.time_format===s.Hg.am_pm}))},76415:(e,t,a)=>{a.d(t,{Hg:()=>s,Wj:()=>n,jG:()=>i,ow:()=>o,zt:()=>r});let i=function(e){return e.language="language",e.system="system",e.comma_decimal="comma_decimal",e.decimal_comma="decimal_comma",e.space_comma="space_comma",e.none="none",e}({}),s=function(e){return e.language="language",e.system="system",e.am_pm="12",e.twenty_four="24",e}({}),n=function(e){return e.local="local",e.server="server",e}({}),o=function(e){return e.language="language",e.system="system",e.DMY="DMY",e.MDY="MDY",e.YMD="YMD",e}({}),r=function(e){return e.language="language",e.monday="monday",e.tuesday="tuesday",e.wednesday="wednesday",e.thursday="thursday",e.friday="friday",e.saturday="saturday",e.sunday="sunday",e}({})},44114:(e,t,a)=>{a.r(t);var i=a(85461),s=a(69534),n=a(52345),o=a(20068),r=a(73330),l=a(63759),d=a(56138),c=a(21513),h=a(94061),u=a(51561),m=a(98597),y=a(196),v=a(58636),f=a(13634),g=a(49655),_=a(33167),k=(a(59373),a(61399)),p=a(76415),w=a(31447),b=a(43799);const D={plugins:[l.A,r.Ay],headerToolbar:!1,initialView:"timeGridWeek",editable:!0,selectable:!0,selectMirror:!0,selectOverlap:!1,eventOverlap:!1,allDaySlot:!1,height:"parent",locales:o.A,firstDay:1,dayHeaderFormat:{weekday:"short",month:void 0,day:void 0}};(0,i.A)([(0,y.EM)("ha-schedule-form")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,y.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,y.MZ)({type:Boolean})],key:"new",value(){return!1}},{kind:"field",decorators:[(0,y.wk)()],key:"_name",value:void 0},{kind:"field",decorators:[(0,y.wk)()],key:"_icon",value:void 0},{kind:"field",decorators:[(0,y.wk)()],key:"_monday",value:void 0},{kind:"field",decorators:[(0,y.wk)()],key:"_tuesday",value:void 0},{kind:"field",decorators:[(0,y.wk)()],key:"_wednesday",value:void 0},{kind:"field",decorators:[(0,y.wk)()],key:"_thursday",value:void 0},{kind:"field",decorators:[(0,y.wk)()],key:"_friday",value:void 0},{kind:"field",decorators:[(0,y.wk)()],key:"_saturday",value:void 0},{kind:"field",decorators:[(0,y.wk)()],key:"_sunday",value:void 0},{kind:"field",decorators:[(0,y.wk)()],key:"calendar",value:void 0},{kind:"field",key:"_item",value:void 0},{kind:"set",key:"item",value:function(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._monday=e.monday||[],this._tuesday=e.tuesday||[],this._wednesday=e.wednesday||[],this._thursday=e.thursday||[],this._friday=e.friday||[],this._saturday=e.saturday||[],this._sunday=e.sunday||[]):(this._name="",this._icon="",this._monday=[],this._tuesday=[],this._wednesday=[],this._thursday=[],this._friday=[],this._saturday=[],this._sunday=[])}},{kind:"method",key:"disconnectedCallback",value:function(){(0,s.A)(a,"disconnectedCallback",this,3)([]),this.calendar?.destroy(),this.calendar=void 0,this.renderRoot.querySelector("style[data-fullcalendar]")?.remove()}},{kind:"method",key:"connectedCallback",value:function(){(0,s.A)(a,"connectedCallback",this,3)([]),this.hasUpdated&&!this.calendar&&this.setupCalendar()}},{kind:"method",key:"focus",value:function(){this.updateComplete.then((()=>this.shadowRoot?.querySelector("[dialogInitialFocus]")?.focus()))}},{kind:"method",key:"render",value:function(){return this.hass?m.qy`
      <div class="form">
        <ha-textfield
          .value=${this._name}
          .configValue=${"name"}
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.name")}
          autoValidate
          required
          .validationMessage=${this.hass.localize("ui.dialogs.helper_settings.required_error_msg")}
          dialogInitialFocus
        ></ha-textfield>
        <ha-icon-picker
          .hass=${this.hass}
          .value=${this._icon}
          .configValue=${"icon"}
          @value-changed=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.icon")}
        ></ha-icon-picker>
        <div id="calendar"></div>
      </div>
    `:m.s6}},{kind:"method",key:"willUpdate",value:function(e){if((0,s.A)(a,"willUpdate",this,3)([e]),!this.calendar)return;(e.has("_sunday")||e.has("_monday")||e.has("_tuesday")||e.has("_wednesday")||e.has("_thursday")||e.has("_friday")||e.has("_saturday")||e.has("calendar"))&&(this.calendar.removeAllEventSources(),this.calendar.addEventSource(this._events));const t=e.get("hass");t&&t.language!==this.hass.language&&this.calendar.setOption("locale",this.hass.language)}},{kind:"method",key:"firstUpdated",value:function(){this.setupCalendar()}},{kind:"method",key:"setupCalendar",value:function(){const e={...D,locale:this.hass.language,firstDay:(0,v.PE)(this.hass.locale),slotLabelFormat:{hour:"numeric",minute:void 0,hour12:(0,g.J)(this.hass.locale),meridiem:!!(0,g.J)(this.hass.locale)&&"narrow"},eventTimeFormat:{hour:(0,g.J)(this.hass.locale)?"numeric":"2-digit",minute:(0,g.J)(this.hass.locale)?"numeric":"2-digit",hour12:(0,g.J)(this.hass.locale),meridiem:!!(0,g.J)(this.hass.locale)&&"narrow"}};e.eventClick=e=>this._handleEventClick(e),e.select=e=>this._handleSelect(e),e.eventResize=e=>this._handleEventResize(e),e.eventDrop=e=>this._handleEventDrop(e),this.calendar=new n.Vv(this.shadowRoot.getElementById("calendar"),e),this.calendar.render()}},{kind:"get",key:"_events",value:function(){const e=[];for(const[t,a]of k.mx.entries())this[`_${a}`].length&&this[`_${a}`].forEach(((i,s)=>{let n=(0,d.s)(new Date,t);(0,c.R)(n,new Date,{weekStartsOn:(0,v.PE)(this.hass.locale)})||(n=(0,h.f)(n,-7));const o=new Date(n),r=i.from.split(":");o.setHours(parseInt(r[0]),parseInt(r[1]),0,0);const l=new Date(n),u=i.to.split(":");l.setHours(parseInt(u[0]),parseInt(u[1]),0,0),e.push({id:`${a}-${s}`,start:o.toISOString(),end:l.toISOString()})}));return e}},{kind:"method",key:"_handleSelect",value:function(e){const{start:t,end:a}=e,i=k.mx[t.getDay()],s=[...this[`_${i}`]],n={...this._item},o=(0,f.LW)(a,{...this.hass.locale,time_zone:p.Wj.local},this.hass.config);s.push({from:(0,f.LW)(t,{...this.hass.locale,time_zone:p.Wj.local},this.hass.config),to:(0,u.r)(t,a)&&"0:00"!==o?o:"24:00"}),n[i]=s,(0,_.r)(this,"value-changed",{value:n}),(0,u.r)(t,a)||this.calendar.unselect()}},{kind:"method",key:"_handleEventResize",value:function(e){const{id:t,start:a,end:i}=e.event,[s,n]=t.split("-"),o=this[`_${s}`][parseInt(n)],r={...this._item},l=(0,f.LW)(i,this.hass.locale,this.hass.config);r[s][n]={from:o.from,to:(0,u.r)(a,i)&&"0:00"!==l?l:"24:00"},(0,_.r)(this,"value-changed",{value:r}),(0,u.r)(a,i)||(this.requestUpdate(`_${s}`),e.revert())}},{kind:"method",key:"_handleEventDrop",value:function(e){const{id:t,start:a,end:i}=e.event,[s,n]=t.split("-"),o=k.mx[a.getDay()],r={...this._item},l=(0,f.LW)(i,this.hass.locale,this.hass.config),d={from:(0,f.LW)(a,this.hass.locale,this.hass.config),to:(0,u.r)(a,i)&&"0:00"!==l?l:"24:00"};if(o===s)r[s][n]=d;else{r[s].splice(n,1);const e=[...this[`_${o}`]];e.push(d),r[o]=e}(0,_.r)(this,"value-changed",{value:r}),(0,u.r)(a,i)||(this.requestUpdate(`_${s}`),e.revert())}},{kind:"method",key:"_handleEventClick",value:async function(e){if(!(await(0,w.dk)(this,{title:this.hass.localize("ui.dialogs.helper_settings.schedule.delete"),text:this.hass.localize("ui.dialogs.helper_settings.schedule.confirm_delete"),destructive:!0,confirmText:this.hass.localize("ui.common.delete")})))return;const[t,a]=e.event.id.split("-"),i=[...this[`_${t}`]],s={...this._item};i.splice(parseInt(a),1),s[t]=i,(0,_.r)(this,"value-changed",{value:s})}},{kind:"method",key:"_valueChanged",value:function(e){if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target.configValue,a=e.detail?.value||e.target.value;if(this[`_${t}`]===a)return;const i={...this._item};a?i[t]=a:delete i[t],(0,_.r)(this,"value-changed",{value:i})}},{kind:"get",static:!0,key:"styles",value:function(){return[b.RF,m.AH`
        .form {
          color: var(--primary-text-color);
        }

        ha-textfield {
          display: block;
          margin: 8px 0;
        }

        #calendar {
          margin: 8px 0;
          height: 450px;
          width: 100%;
          -webkit-user-select: none;
          -ms-user-select: none;
          user-select: none;
          --fc-border-color: var(--divider-color);
          --fc-event-border-color: var(--divider-color);
        }

        .fc-v-event .fc-event-time {
          white-space: inherit;
        }
        .fc-theme-standard .fc-scrollgrid {
          border: 1px solid var(--divider-color);
          border-radius: var(--mdc-shape-small, 4px);
        }

        .fc-scrollgrid-section-header td {
          border: none;
        }
        :host([narrow]) .fc-scrollgrid-sync-table {
          overflow: hidden;
        }
        table.fc-scrollgrid-sync-table
          tbody
          tr:first-child
          .fc-daygrid-day-top {
          padding-top: 0;
        }
        .fc-scroller::-webkit-scrollbar {
          width: 0.4rem;
          height: 0.4rem;
        }
        .fc-scroller::-webkit-scrollbar-thumb {
          -webkit-border-radius: 4px;
          border-radius: 4px;
          background: var(--scrollbar-thumb-color);
        }
        .fc-scroller {
          overflow-y: auto;
          scrollbar-color: var(--scrollbar-thumb-color) transparent;
          scrollbar-width: thin;
        }

        .fc-timegrid-event-short .fc-event-time:after {
          content: ""; /* prevent trailing dash in half hour events since we do not have event titles */
        }

        a {
          color: inherit !important;
        }

        th.fc-col-header-cell.fc-day {
          background-color: var(--table-header-background-color);
          color: var(--primary-text-color);
          font-size: 11px;
          font-weight: bold;
          text-transform: uppercase;
        }
      `]}}]}}),m.WF)}};
//# sourceMappingURL=6923H_lP.js.map