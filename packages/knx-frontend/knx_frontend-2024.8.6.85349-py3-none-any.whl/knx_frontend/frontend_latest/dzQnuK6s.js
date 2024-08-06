export const id=9184;export const ids=[9184];export const modules={80106:(e,t,i)=>{i.d(t,{d:()=>a});const a=e=>{switch(e.language){case"cz":case"de":case"fi":case"fr":case"sk":case"sv":return" ";default:return""}}},94392:(e,t,i)=>{var a=i(85461),o=i(98597),r=i(196);(0,a.A)([(0,r.EM)("ha-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)()],key:"header",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"raised",value(){return!1}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      :host {
        background: var(
          --ha-card-background,
          var(--card-background-color, white)
        );
        -webkit-backdrop-filter: var(--ha-card-backdrop-filter, none);
        backdrop-filter: var(--ha-card-backdrop-filter, none);
        box-shadow: var(--ha-card-box-shadow, none);
        box-sizing: border-box;
        border-radius: var(--ha-card-border-radius, 12px);
        border-width: var(--ha-card-border-width, 1px);
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        position: relative;
      }

      :host([raised]) {
        border: none;
        box-shadow: var(
          --ha-card-box-shadow,
          0px 2px 1px -1px rgba(0, 0, 0, 0.2),
          0px 1px 1px 0px rgba(0, 0, 0, 0.14),
          0px 1px 3px 0px rgba(0, 0, 0, 0.12)
        );
      }

      .card-header,
      :host ::slotted(.card-header) {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 48px;
        padding: 12px 16px 16px;
        display: block;
        margin-block-start: 0px;
        margin-block-end: 0px;
        font-weight: normal;
      }

      :host ::slotted(.card-content:not(:first-child)),
      slot:not(:first-child)::slotted(.card-content) {
        padding-top: 0px;
        margin-top: -8px;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid var(--divider-color, #e8e8e8);
        padding: 5px 16px;
      }
    `}},{kind:"method",key:"render",value:function(){return o.qy`
      ${this.header?o.qy`<h1 class="card-header">${this.header}</h1>`:o.s6}
      <slot></slot>
    `}}]}}),o.WF)},73279:(e,t,i)=>{var a=i(85461),o=i(69534),r=i(57305),n=i(98597),s=i(196);(0,a.A)([(0,s.EM)("ha-circular-progress")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.MZ)({attribute:"aria-label",type:String})],key:"ariaLabel",value(){return"Loading"}},{kind:"field",decorators:[(0,s.MZ)()],key:"size",value(){return"medium"}},{kind:"method",key:"updated",value:function(e){if((0,o.A)(i,"updated",this,3)([e]),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"field",static:!0,key:"styles",value(){return[...(0,o.A)(i,"styles",this),n.AH`
      :host {
        --md-sys-color-primary: var(--primary-color);
        --md-circular-progress-size: 48px;
      }
    `]}}]}}),r.U)},96287:(e,t,i)=>{var a=i(85461),o=i(69534),r=(i(8774),i(98597)),n=i(196),s=i(69760),d=i(33167),l=(i(66494),i(89874),i(80106)),c=i(96041);const h="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",p="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z";(0,a.A)([(0,n.EM)("ha-file-upload")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.MZ)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"accept",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"icon",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"label",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"secondary",value:void 0},{kind:"field",decorators:[(0,n.MZ)()],key:"supports",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Object})],key:"value",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"multiple",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Boolean})],key:"uploading",value(){return!1}},{kind:"field",decorators:[(0,n.MZ)({type:Number})],key:"progress",value:void 0},{kind:"field",decorators:[(0,n.MZ)({type:Boolean,attribute:"auto-open-file-dialog"})],key:"autoOpenFileDialog",value(){return!1}},{kind:"field",decorators:[(0,n.wk)()],key:"_drag",value(){return!1}},{kind:"field",decorators:[(0,n.P)("#input")],key:"_input",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,o.A)(i,"firstUpdated",this,3)([e]),this.autoOpenFileDialog&&this._openFilePicker()}},{kind:"method",key:"render",value:function(){return r.qy`
      ${this.uploading?r.qy`<div class="container">
            <div class="row">
              <span class="header"
                >${this.value?this.hass?.localize("ui.components.file-upload.uploading_name",{name:this.value.toString()}):this.hass?.localize("ui.components.file-upload.uploading")}</span
              >
              ${this.progress?r.qy`<span class="progress"
                    >${this.progress}${(0,l.d)(this.hass.locale)}%</span
                  >`:""}
            </div>
            <mwc-linear-progress
              .indeterminate=${!this.progress}
              .progress=${this.progress?this.progress/100:void 0}
            ></mwc-linear-progress>
          </div>`:r.qy`<label
            for=${this.value?"":"input"}
            class="container ${(0,s.H)({dragged:this._drag,multiple:this.multiple,value:Boolean(this.value)})}"
            @drop=${this._handleDrop}
            @dragenter=${this._handleDragStart}
            @dragover=${this._handleDragStart}
            @dragleave=${this._handleDragEnd}
            @dragend=${this._handleDragEnd}
            >${this.value?"string"==typeof this.value?r.qy`<div class="row">
                    <div class="value" @click=${this._openFilePicker}>
                      <ha-svg-icon
                        .path=${this.icon||p}
                      ></ha-svg-icon>
                      ${this.value}
                    </div>
                    <ha-icon-button
                      @click=${this._clearValue}
                      .label=${this.hass?.localize("ui.common.delete")||"Delete"}
                      .path=${h}
                    ></ha-icon-button>
                  </div>`:(this.value instanceof FileList?Array.from(this.value):(0,c.e)(this.value)).map((e=>r.qy`<div class="row">
                        <div class="value" @click=${this._openFilePicker}>
                          <ha-svg-icon
                            .path=${this.icon||p}
                          ></ha-svg-icon>
                          ${e.name} - ${((e=0,t=2)=>{if(0===e)return"0 Bytes";t=t<0?0:t;const i=Math.floor(Math.log(e)/Math.log(1024));return`${parseFloat((e/1024**i).toFixed(t))} ${["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"][i]}`})(e.size)}
                        </div>
                        <ha-icon-button
                          @click=${this._clearValue}
                          .label=${this.hass?.localize("ui.common.delete")||"Delete"}
                          .path=${h}
                        ></ha-icon-button>
                      </div>`)):r.qy`<ha-svg-icon
                    class="big-icon"
                    .path=${this.icon||p}
                  ></ha-svg-icon>
                  <ha-button unelevated @click=${this._openFilePicker}>
                    ${this.label||this.hass?.localize("ui.components.file-upload.label")}
                  </ha-button>
                  <span class="secondary"
                    >${this.secondary||this.hass?.localize("ui.components.file-upload.secondary")}</span
                  >
                  <span class="supports">${this.supports}</span>`}
            <input
              id="input"
              type="file"
              class="file"
              .accept=${this.accept}
              .multiple=${this.multiple}
              @change=${this._handleFilePicked}
          /></label>`}
    `}},{kind:"method",key:"_openFilePicker",value:function(){this._input?.click()}},{kind:"method",key:"_handleDrop",value:function(e){e.preventDefault(),e.stopPropagation(),e.dataTransfer?.files&&(0,d.r)(this,"file-picked",{files:this.multiple||1===e.dataTransfer.files.length?Array.from(e.dataTransfer.files):[e.dataTransfer.files[0]]}),this._drag=!1}},{kind:"method",key:"_handleDragStart",value:function(e){e.preventDefault(),e.stopPropagation(),this._drag=!0}},{kind:"method",key:"_handleDragEnd",value:function(e){e.preventDefault(),e.stopPropagation(),this._drag=!1}},{kind:"method",key:"_handleFilePicked",value:function(e){0!==e.target.files.length&&(this.value=e.target.files,(0,d.r)(this,"file-picked",{files:e.target.files}))}},{kind:"method",key:"_clearValue",value:function(e){e.preventDefault(),this._input.value="",this.value=void 0,(0,d.r)(this,"change")}},{kind:"get",static:!0,key:"styles",value:function(){return r.AH`
      :host {
        display: block;
        height: 240px;
      }
      :host([disabled]) {
        pointer-events: none;
        color: var(--disabled-text-color);
      }
      .container {
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: solid 1px
          var(--mdc-text-field-idle-line-color, rgba(0, 0, 0, 0.42));
        border-radius: var(--mdc-shape-small, 4px);
        height: 100%;
      }
      label.container {
        border: dashed 1px
          var(--mdc-text-field-idle-line-color, rgba(0, 0, 0, 0.42));
        cursor: pointer;
      }
      :host([disabled]) .container {
        border-color: var(--disabled-color);
      }
      label.dragged {
        border-color: var(--primary-color);
      }
      .dragged:before {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background-color: var(--primary-color);
        content: "";
        opacity: var(--dark-divider-opacity);
        pointer-events: none;
        border-radius: var(--mdc-shape-small, 4px);
      }
      label.value {
        cursor: default;
      }
      label.value.multiple {
        justify-content: unset;
        overflow: auto;
      }
      .highlight {
        color: var(--primary-color);
      }
      .row {
        display: flex;
        width: 100%;
        align-items: center;
        justify-content: space-between;
        padding: 0 16px;
        box-sizing: border-box;
      }
      ha-button {
        margin-bottom: 4px;
      }
      .supports {
        color: var(--secondary-text-color);
        font-size: 12px;
      }
      :host([disabled]) .secondary {
        color: var(--disabled-text-color);
      }
      input.file {
        display: none;
      }
      .value {
        cursor: pointer;
      }
      .value ha-svg-icon {
        margin-right: 8px;
        margin-inline-end: 8px;
        margin-inline-start: initial;
      }
      .big-icon {
        --mdc-icon-size: 48px;
        margin-bottom: 8px;
      }
      ha-button {
        --mdc-button-outline-color: var(--primary-color);
        --mdc-icon-button-size: 24px;
      }
      mwc-linear-progress {
        width: 100%;
        padding: 16px;
        box-sizing: border-box;
      }
      .header {
        font-weight: 500;
      }
      .progress {
        color: var(--secondary-text-color);
      }
    `}}]}}),r.WF)},18966:(e,t,i)=>{i.d(t,{Q:()=>a,n:()=>o});const a=async(e,t)=>{const i=new FormData;i.append("file",t);const a=await e.fetchWithAuth("/api/file_upload",{method:"POST",body:i});if(413===a.status)throw new Error(`Uploaded file is too large (${t.name})`);if(200!==a.status)throw new Error("Unknown error");return(await a.json()).file_id},o=async(e,t)=>e.callApi("DELETE","file_upload",{file_id:t})},12263:(e,t,i)=>{i.d(t,{PS:()=>a,VR:()=>o});const a=e=>e.data,o=e=>"object"==typeof e?"object"==typeof e.body?e.body.message||"Unknown error, see supervisor logs":e.body||e.message||"Unknown error, see supervisor logs":e;new Set([502,503,504])},31447:(e,t,i)=>{i.d(t,{K$:()=>n,an:()=>d,dk:()=>s});var a=i(33167);const o=()=>Promise.all([i.e(7847),i.e(4475)]).then(i.bind(i,94475)),r=(e,t,i)=>new Promise((r=>{const n=t.cancel,s=t.confirm;(0,a.r)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:o,dialogParams:{...t,...i,cancel:()=>{r(!!i?.prompt&&null),n&&n()},confirm:e=>{r(!i?.prompt||e),s&&s(e)}}})})),n=(e,t)=>r(e,t),s=(e,t)=>r(e,t,{confirmation:!0}),d=(e,t)=>r(e,t,{prompt:!0})},69184:(e,t,i)=>{i.r(t),i.d(t,{KNXInfo:()=>u});var a=i(85461),o=i(98597),r=i(196),n=i(13314),s=(i(94392),i(7341),i(66494),i(96287),i(74259),i(73279),i(18966)),d=i(12263),l=i(31447),c=i(39987),h=i(61328);const p=new h.Q("info");let u=(0,a.A)([(0,r.EM)("knx-info")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.MZ)({type:Object})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.MZ)({attribute:!1})],key:"knx",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,r.MZ)({type:Array,reflect:!1})],key:"tabs",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"knxInfoData",value(){return null}},{kind:"field",decorators:[(0,r.wk)()],key:"_projectPassword",value:void 0},{kind:"field",decorators:[(0,r.wk)()],key:"_uploading",value(){return!1}},{kind:"field",decorators:[(0,r.wk)()],key:"_projectFile",value:void 0},{kind:"method",key:"firstUpdated",value:function(){this.loadKnxInfo()}},{kind:"method",key:"render",value:function(){return o.qy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${this.tabs}
        .localizeFunc=${this.knx.localize}
      >
        <div class="columns">
          ${this.knxInfoData?o.qy`
                ${this._renderInfoCard()}
                ${this.knxInfoData?.project?this._renderProjectDataCard(this.knxInfoData.project):o.s6}
                ${this._renderProjectUploadCard()}
              `:o.qy`
                <ha-circular-progress alt="Loading..." size="large" active></ha-circular-progress>
              `}
        </div>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_renderInfoCard",value:function(){return o.qy` <ha-card class="knx-info">
      <div class="card-content knx-info-section">
        <div class="knx-content-row header">${this.knx.localize("info_information_header")}</div>

        <div class="knx-content-row">
          <div>XKNX Version</div>
          <div>${this.knxInfoData?.version}</div>
        </div>

        <div class="knx-content-row">
          <div>KNX-Frontend Version</div>
          <div>${"2024.8.6.85349"}</div>
        </div>

        <div class="knx-content-row">
          <div>${this.knx.localize("info_connected_to_bus")}</div>
          <div>
            ${this.hass.localize(this.knxInfoData?.connected?"ui.common.yes":"ui.common.no")}
          </div>
        </div>

        <div class="knx-content-row">
          <div>${this.knx.localize("info_individual_address")}</div>
          <div>${this.knxInfoData?.current_address}</div>
        </div>

        <div class="knx-bug-report">
          <div>${this.knx.localize("info_issue_tracker")}</div>
          <ul>
            <li>
              <a href="https://github.com/XKNX/knx-frontend/issues" target="_blank"
                >${this.knx.localize("info_issue_tracker_knx_frontend")}</a
              >
            </li>
            <li>
              <a href="https://github.com/XKNX/xknxproject/issues" target="_blank"
                >${this.knx.localize("info_issue_tracker_xknxproject")}</a
              >
            </li>
            <li>
              <a href="https://github.com/XKNX/xknx/issues" target="_blank"
                >${this.knx.localize("info_issue_tracker_xknx")}</a
              >
            </li>
          </ul>
        </div>
      </div>
    </ha-card>`}},{kind:"method",key:"_renderProjectDataCard",value:function(e){return o.qy`
      <ha-card class="knx-info">
          <div class="card-content knx-content">
            <div class="header knx-content-row">
              ${this.knx.localize("info_project_data_header")}
            </div>
            <div class="knx-content-row">
              <div>${this.knx.localize("info_project_data_name")}</div>
              <div>${e.name}</div>
            </div>
            <div class="knx-content-row">
              <div>${this.knx.localize("info_project_data_last_modified")}</div>
              <div>${new Date(e.last_modified).toUTCString()}</div>
            </div>
            <div class="knx-content-row">
              <div>${this.knx.localize("info_project_data_tool_version")}</div>
              <div>${e.tool_version}</div>
            </div>
            <div class="knx-content-row">
              <div>${this.knx.localize("info_project_data_xknxproject_version")}</div>
              <div>${e.xknxproject_version}</div>
            </div>
            <div class="knx-button-row">
              <ha-button
                class="knx-warning push-right"
                @click=${this._removeProject}
                .disabled=${this._uploading||!this.knxInfoData?.project}
                >
                ${this.knx.localize("info_project_delete")}
              </ha-button>
            </div>
          </div>
        </div>
      </ha-card>
    `}},{kind:"method",key:"_renderProjectUploadCard",value:function(){return o.qy` <ha-card class="knx-info">
      <div class="card-content knx-content">
        <div class="knx-content-row header">${this.knx.localize("info_project_file_header")}</div>
        <div class="knx-content-row">${this.knx.localize("info_project_upload_description")}</div>
        <div class="knx-content-row">
          <ha-file-upload
            .hass=${this.hass}
            accept=".knxproj, .knxprojarchive"
            .icon=${"M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z"}
            .label=${this.knx.localize("info_project_file")}
            .value=${this._projectFile?.name}
            .uploading=${this._uploading}
            @file-picked=${this._filePicked}
          ></ha-file-upload>
        </div>
        <div class="knx-content-row">
          <ha-selector-text
            .hass=${this.hass}
            .value=${this._projectPassword||""}
            .label=${this.hass.localize("ui.login-form.password")}
            .selector=${{text:{multiline:!1,type:"password"}}}
            .required=${!1}
            @value-changed=${this._passwordChanged}
          >
          </ha-selector-text>
        </div>
        <div class="knx-button-row">
          <ha-button
            class="push-right"
            @click=${this._uploadFile}
            .disabled=${this._uploading||!this._projectFile}
            >${this.hass.localize("ui.common.submit")}</ha-button
          >
        </div>
      </div>
    </ha-card>`}},{kind:"method",key:"loadKnxInfo",value:function(){(0,c.qn)(this.hass).then((e=>{this.knxInfoData=e,this.requestUpdate()}),(e=>{p.error("getKnxInfoData",e),(0,n.o)("/knx/error",{replace:!0,data:e})}))}},{kind:"method",key:"_filePicked",value:function(e){this._projectFile=e.detail.files[0]}},{kind:"method",key:"_passwordChanged",value:function(e){this._projectPassword=e.detail.value}},{kind:"method",key:"_uploadFile",value:async function(e){const t=this._projectFile;if(void 0===t)return;let i;this._uploading=!0;try{const e=await(0,s.Q)(this.hass,t);await(0,c.dc)(this.hass,e,this._projectPassword||"")}catch(a){i=a,(0,l.K$)(this,{title:"Upload failed",text:(0,d.VR)(a)})}finally{i||(this._projectFile=void 0,this._projectPassword=void 0),this._uploading=!1,this.loadKnxInfo()}}},{kind:"method",key:"_removeProject",value:async function(e){if(await(0,l.dk)(this,{text:this.knx.localize("info_project_delete")}))try{await(0,c.gV)(this.hass)}catch(t){(0,l.K$)(this,{title:"Deletion failed",text:(0,d.VR)(t)})}finally{this.loadKnxInfo()}else p.debug("User cancelled deletion")}},{kind:"get",static:!0,key:"styles",value:function(){return o.AH`
      .columns {
        display: flex;
        justify-content: center;
      }

      @media screen and (max-width: 1232px) {
        .columns {
          flex-direction: column;
        }

        .knx-button-row {
          margin-top: 20px;
        }

        .knx-info {
          margin-right: 8px;
        }
      }

      @media screen and (min-width: 1233px) {
        .knx-button-row {
          margin-top: auto;
        }

        .knx-info {
          width: 400px;
        }
      }

      .knx-info {
        margin-left: 8px;
        margin-top: 8px;
      }

      .knx-content {
        display: flex;
        flex-direction: column;
        height: 100%;
        box-sizing: border-box;
      }

      .knx-content-row {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
      }

      .knx-content-row > div:nth-child(2) {
        margin-left: 1rem;
      }

      .knx-button-row {
        display: flex;
        flex-direction: row;
        vertical-align: bottom;
        padding-top: 16px;
      }

      .push-left {
        margin-right: auto;
      }

      .push-right {
        margin-left: auto;
      }

      .knx-warning {
        --mdc-theme-primary: var(--error-color);
      }

      .knx-project-description {
        margin-top: -8px;
        padding: 0px 16px 16px;
      }

      .knx-delete-project-button {
        position: absolute;
        bottom: 0;
        right: 0;
      }

      .knx-bug-report {
        margin-top: 20px;
      }

      .knx-bug-report > ul > li > a {
        text-decoration: none;
        color: var(--mdc-theme-primary);
      }

      .header {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 48px;
        padding: -4px 16px 16px;
        display: inline-block;
        margin-block-start: 0px;
        margin-block-end: 4px;
        font-weight: normal;
      }

      ha-file-upload,
      ha-selector-text {
        width: 100%;
        margin-top: 8px;
      }

      ha-circular-progress {
        margin-top: 32px;
      }
    `}}]}}),o.WF)}};
//# sourceMappingURL=dzQnuK6s.js.map